"""
获取已经入会的 venderID
---
user_shop_venderId.txt
"""
import os
import sys

import requests
import re
import threading

# 这里填写遍历的 cookie
COOKIE = "" or "pt_key=" + sys.argv[1] + ";pt_pin=" + sys.argv[2]
THREAD = 8


def get_file_path(file_name=""):
    """
    获取文件绝对路径, 防止在某些情况下报错
    :param file_name: 文件名
    :return:
    """
    return os.path.join(os.path.split(sys.argv[0])[0], file_name)


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
            return False, None
    except:
        return False, None


def _get_shop_open_card_info(cookie, venderId):
    params = {
        "appid": "jd_shop_member",
        "functionId": "getShopOpenCardInfo",
        "body": '{"venderId":"' + str(venderId) + '","channel":406}',
        "client": "H5",
        "clientVersion": "9.2.0",
        "uuid": "88888"
    }
    host = "api.m.jd.com"
    url = "https://api.m.jd.com/client.action"
    headers = {
        "Cookie": cookie,
        "Host": host,
        "Referer": "https://m.jd.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; COR-AL00) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/77.0.3865.116 Mobile Safari/537.36 EdgA/46.03.4.5155 "
    }
    try:
        res = requests.get(url, params=params, headers=headers, verify=False)
        # print(res.json())
        if res.status_code == 200 and res.json()['success']:
            return True, str(venderId), bool(res.json()['result']['userInfo']['openCardStatus'])
        else:
            return False, str(venderId), False
    except:
        return False, str(venderId), False


def get_user_brand_member(thread):
    global process
    for _ in shop_ids[thread::THREAD]:
        process[0] += 1
        info = _get_shop_open_card_info(COOKIE, get_venderId(int(_))[1])
        if info[0] and info[2]:
            process[1] += 1
            open(get_file_path("user_shop_venderId.txt"), "a", encoding="utf-8").write(info[1] + "\n")
        print("\r已遍历{}个店铺，其中你已入会{}个， 结果保存在`user_shop_venderId.txt`".format(process[0], process[1]), end="")


if __name__ == '__main__':
    process = [0, 0]

    # 忽略警告
    requests.packages.urllib3.disable_warnings()
    open(get_file_path("user_shop_venderId.txt"), "w").close()

    shop_ids = open(get_file_path("shopid.txt"), "r").readlines()
    for thread in range(THREAD):
        threading.Thread(target=get_user_brand_member, args=(thread,)).start()
