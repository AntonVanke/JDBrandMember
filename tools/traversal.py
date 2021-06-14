"""
用于遍历 `shopid.yaml`

---
>docs/HOW_TO_UPDATE_SHOPID.md

"""
import datetime
import os
import sys
import threading
import atexit
import re
import requests
import yaml

THREAD = 8
# 这里填写遍历的 cookie， 如果你想分享 shopid.yaml 给他人使用，那么建议你不要使用刷过京豆的账号，否则会有遗漏
COOKIE = "" or "pt_key=" + sys.argv[1] + ";pt_pin=" + sys.argv[2]
SHOP_ID = []


def get_file_path(file_name=""):
    """
    获取文件绝对路径, 防止在某些情况下报错
    :param file_name: 文件名
    :return:
    """
    return os.path.join(os.path.split(sys.argv[0])[0], file_name)


def _get_headers(cookie, host):
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
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; COR-AL00) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/77.0.3865.116 Mobile Safari/537.36 EdgA/46.03.4.5155 "
    }


def _get_venderId(shop_id):
    """
    将 `shop_id` 转换为 `venderId`
    :param shop_id:
    :return:
    """
    res = requests.get("https://shop.m.jd.com/?shopId=" + str(shop_id))
    _res = re.compile("venderId: '(\\d*)'").findall(res.text)
    if res.status_code == 200 and len(_res):
        return True, re.compile("venderId: '(\\d*)'").findall(res.text)[0]
    else:
        return False, None


def _get_shop_open_card_info(cookie, shop_id):
    """
    获取店铺会员信息
    :param cookie:
    :param shop_id:
    :return:
    """
    try:
        status, venderId = _get_venderId(shop_id)
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
        res = requests.get(url, params=params, headers=_get_headers(cookie, host))
        if res.status_code == 200 and res.json()['success']:
            if res.json()['result']['interestsRuleList'] is not None:
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
        return False, None, None, None


@atexit.register
def over():
    print("\n共遍历{}个店铺，其中包含{}京豆和{}元红包的入会奖励，结果保存至`./shopid.yaml`".format(process[0], process[1], process[2]))
    res = {
        "update_time": str(datetime.date.today()),
        "shop_id": list(set(SHOP_ID))
    }
    yaml.safe_dump(res, open(get_file_path("shopid.yaml"), "w", encoding="utf-8"))


if __name__ == '__main__':
    shop_ids = yaml.safe_load(open(get_file_path("all_shopid.yaml"), "r", encoding="utf-8"))['shop_id']

    process = [0, 0, 0]

    print(COOKIE)


    # print(_get_shop_open_card_info(COOKIE, 1000090370))
    def a(thread, threads):
        global process
        for _ in shop_ids[thread::threads]:
            process[0] += 1
            print("\r已遍历{}个店铺".format(process[0]), end="")
            info = _get_shop_open_card_info(COOKIE, str(int(_)))
            if info[0]:
                SHOP_ID.append(str(int(_)))
                print(str(int(_)), info[2], info[1])


    for thread in range(THREAD):
        threading.Thread(target=a, args=(thread, THREAD,)).start()
