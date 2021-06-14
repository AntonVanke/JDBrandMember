import atexit
import os
import re
import sys
import threading

import time
import traceback

import yaml
import requests
import datetime


@atexit.register
def _end():
    end_time = time.time()
    print(to_log("INFO", "执行结束", "执行耗时{:.3f}s".format(end_time - start_time)))


def get_shopid():
    """
    获取 shopid, 如果网络上的更新时间比本地早则使用本地的，其它则使用网络上的
    """
    use_file = CONFIG["screening"].get("use", "shopid.yaml")
    try:
        net_res = requests.get(CONFIG['shop_id_url'], timeout=30)
        if net_res.status_code != 200:
            raise Exception
    except:
        print(to_log("ERROR", "获取线上 shopid 失败"))

    if os.path.exists(get_file_path(use_file)):
        try:
            res = yaml.safe_load(open(get_file_path(use_file), "r", encoding="utf-8"))
        except:
            os.remove(get_file_path(use_file))
            print(to_log("ERROR", "shopid.yaml损坏", "已经删除损坏文件，请重新打开"))
            sys.exit()
    try:
        if (datetime.datetime.strptime(str(yaml.safe_load(net_res.text)['update_time']),
                                       '%Y-%m-%d') - datetime.datetime.strptime(str(res['update_time']),
                                                                                '%Y-%m-%d')).days > 0:
            print(to_log("INFO", "已更新 shopid"))
            res = yaml.safe_load(net_res.text)
            open(get_file_path(use_file), "w", encoding="utf-8").write(net_res.text)
    except:
        pass
    print(to_log("INFO", "shopid更新时间", str(res['update_time'])))
    return True, res['shop_id']


def get_timestamp():
    """
    获取毫秒时间戳
    :return:
    """
    return str(int(time.time() * 1000))


def get_file_path(file_name=""):
    """
    获取文件绝对路径, 防止在某些情况下报错
    :param file_name: 文件名
    :return:
    """
    return os.path.join(os.path.split(sys.argv[0])[0], file_name)


def to_log(info_type="", title="", info=""):
    """
    :param info_type: 日志的等级
    :param title: 日志的标题
    :param info: 日志的信息
    :return:
    """
    if not os.path.exists(get_file_path("logs")):
        os.mkdir(get_file_path("logs/"))
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log = now + "  " + info_type + "  " + title + "  " + info
    with open(get_file_path("logs/jdbm.log"), "a", encoding="utf-8") as log_a_file_io:
        log_a_file_io.write(log + "\n")
    return log


def get_headers(cookie, host):
    """
    返回请求头
    :param cookie:
    :param host:
    :return:
    """
    return {
        "Cookie": cookie,
        "Host": host,
        "Referer": "https://m.jd.com",
        "User-Agent": CONFIG['user-agent'][0]
    }


def get_user_info(cookie):
    """
    获取用户信息
    :type cookie: str
    :return: bool: 是否成功, str: 用户名, str: 用户金豆数量
    """
    try:
        url = "https://me-api.jd.com/user_new/info/GetJDUserInfoUnion"
        res = requests.get(url, headers=get_headers(cookie, "me-api.jd.com"), verify=False)
        if res.status_code == 200 and res.json()["msg"] == "success":
            return True, res.json()["data"]["userInfo"]["baseInfo"]["nickname"], res.json()["data"]["assetInfo"][
                "beanNum"]
        else:
            return False, None, None
    except:
        to_log("ERROR", "获取用户信息错误", traceback.format_exc())
        return False, None, None


def get_venderId(shop_id):
    """
    将 `shop_id` 转换为 `venderId`
    :param shop_id:
    :return: bool: 是否成功, str: venderID
    """
    try:
        res = requests.get("https://shop.m.jd.com/?shopId=" + str(shop_id), verify=False)
        _res = re.compile("venderId: '(\\d*)'").findall(res.text)
        if res.status_code == 200 and len(_res):
            return True, re.compile("venderId: '(\\d*)'").findall(res.text)[0]
        else:
            # TODO: 如果获取不到 venderID 的错误
            return False, None
    except:
        to_log("ERROR", "获取 venderId 错误", traceback.format_exc())
        return False, None


def get_shop_open_card_info(cookie, shop_id):
    """
    获取店铺会员信息
    :param cookie:
    :param shop_id:
    :return: bool: 是否成功, str: 奖励名称, str: 奖励数量, str: activityId
    """
    try:
        status, venderId = get_venderId(shop_id)
        if not status:
            return False, None, None, None
        params = {
            "appid": "jd_shop_member",
            "functionId": "getShopOpenCardInfo",
            "body": '{"venderId":"' + venderId + '","channel":406}',
            "client": "H5",
            "clientVersion": "9.2.0",
            "uuid": "88888"
        }
        host = "api.m.jd.com"
        url = "https://api.m.jd.com/client.action"
        res = requests.get(url, params=params, headers=get_headers(cookie, host), verify=False)

        if res.status_code == 200 and res.json()['success']:
            if not res.json()['result']['userInfo']['openCardStatus'] and res.json()['result']['interestsRuleList'] \
                    is not None:
                for interests_info in res.json()['result']['interestsRuleList']:
                    if interests_info['prizeName'] == "京豆":
                        process[1] += int(interests_info['discountString'])
                        return True, interests_info['prizeName'], interests_info['discountString'], \
                               interests_info['interestsInfo']['activityId']
                    elif interests_info['prizeName'] == "元红包":
                        process[2] += int(interests_info['discountString'])
                        return True, interests_info['prizeName'], interests_info['discountString'], \
                               interests_info['interestsInfo']['activityId']
        return False, None, None, None
    except:
        print(to_log("ERROR", "获取店铺信息错误", traceback.format_exc()))
        return False, None, None, None


def bind_with_vender(cookie, shop_id, activity_id):
    """
    入会
    :param cookie: 用户cookie
    :param shop_id: 店铺 id
    :param activity_id: 活动 id 重要!(如果没有这个就不能获得奖励)
    :return:
    """
    try:
        status, venderId = get_venderId(shop_id)
        if not status:
            return False
        # 请到 config.yaml 更改配置
        params = {
            "appid": "jd_shop_member",
            "functionId": "bindWithVender",
            "body": '{"venderId":"' + venderId + '","shopId":"' + str(
                shop_id) + '","bindByVerifyCodeFlag":1,"registerExtend":{"v_sex":"' + CONFIG['register'][
                        'v_sex'] + '","v_birthday":"' + str(CONFIG['register']['v_birthday']) + '","v_name":"' +
                    CONFIG['register']['v_name'] + '"},"writeChildFlag":0,"activityId":' + str(
                activity_id) + ',"channel":406}',
            "client": "H5",
            "clientVersion": "9.2.0",
            "uuid": "88888"
        }
        host = "api.m.jd.com"
        url = "https://api.m.jd.com/client.action"
        res = requests.get(url, params=params, headers=get_headers(cookie, host), verify=False)
        # TODO:
        #  {"code":0,"success":true,"busiCode":"210","message":"您的账户已经是本店会员","result":null}
        #  {"code":0,"success":true,"busiCode":"0","message":"加入店铺会员成功","result":{"headLine":"您已成功加入店铺会员","giftInfo":null,"interactActivityDTO":null}}
        if res.json()["success"] and res.json()["result"]["giftInfo"] is not None:
            return True
        else:
            # TODO: 记录没有入会成功的日志
            return False
    except:
        to_log("ERROR", "入会错误", traceback.format_exc())
        return False


def bind(cookie, thread):
    global process
    for _ in shop_id_list[thread::CONFIG['thread']]:
        status, prize_name, discount, activity_id = get_shop_open_card_info(cookie, _)
        process[0] += 1
        if status:
            # 筛选条件
            if prize_name == "京豆" and int(discount) < int(CONFIG['screening']['bean']):
                return
            if prize_name == "元红包" and not CONFIG['screening']['voucher']:
                return

            if bind_with_vender(cookie, _, activity_id):
                print(to_log("INFO", "开卡成功", "在" + str(_) + "获得 " + str(discount) + prize_name))
            time.sleep(int(CONFIG.get("sleep-time", 0)))


def main():
    try:
        global process
        for _ in CONFIG['cookies']:
            process = [0, 0, 0]
            status, username, bean_num = get_user_info(_)
            if status:
                print(to_log("INFO", "账号名称: " + str(username) + " 现有京豆数量: " + str(bean_num)))
                for thread in range(CONFIG['thread']):
                    # xxx(cookie=_, shop_id_list=shop_id_list, thread=thread)
                    threading.Thread(target=bind, args=(_, thread,)).start()
                while threading.active_count() != 1:
                    print("\r 账号:{}, 已尝试{}个店铺，获得{}京豆和{}元红包".format(username, process[0], process[1], process[2]),
                          end="")
                    time.sleep(0.5)
            else:
                print(to_log("ERROR", "cookie失效", _[-15:]))
            print(to_log("INFO", "账号{}".format(username),
                         "共尝试{}个店铺，共获得{}京豆和{}元红包\n".format(process[0], process[1], process[2])))
    except:
        print(to_log("ERROR", "运行错误", "在" + traceback.format_exc()))


if __name__ == '__main__':
    start_time = time.time()
    # 忽略警告
    requests.packages.urllib3.disable_warnings()
    if not os.path.exists(get_file_path("config.yaml")):
        print(to_log("ERROR", "未找到配置`config.yaml`", "请查看 https://github.com/AntonVanke/JDBrandMember"))
        sys.exit()
    CONFIG = yaml.safe_load(open(get_file_path("config.yaml"), "r", encoding="utf-8"))

    process = [0, 0, 0]
    # 获取 shopid 列表
    shopid_status, shop_id_list = get_shopid()
    if not shopid_status:
        print(to_log("ERROR", "未找到关键文件", "请查看 https://github.com/AntonVanke/JDBrandMember"))
        sys.exit()

    main()
