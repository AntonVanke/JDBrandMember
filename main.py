import json
import os
import re
import time
import threading
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def printLog(info_type="", title="", info=""):
    """
    :param info_type: 日志的等级
    :param title: 日志的标题
    :param info: 日志的信息
    :return:
    """
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log = now + "  " + info_type + "  " + title + "  " + info
    if info_type == "ERROR":
        print("\033[0;31m" + log + "\033[0m\n")
    elif info_type == "INFO":
        print(log)
    else:
        print(log)
        return
    with open("log.txt", "a", encoding="utf-8") as log_a_file_io:
        log_a_file_io.write(log + "\n")


def getShopID():
    try:
        with open("shopId.txt", "r", encoding="utf-8") as id_file_io:
            return id_file_io.readlines()
    except Exception as _e:
        printLog("ERROR", "获取店铺失败", str(_e.args))


def getBrowser(headless: bool = False, browser_type: str = 'Chrome'):
    """
    获取 browser 对象
    :param browser_type: Chrome, Edge(Chromium), Firefox 浏览器种类，默认为Chrome
    :param headless: 是否开启无头模式，如果开启的话就不能扫码登录
    :return:
    """
    if browser_type == "Chrome":
        # Chrome
        chrome_options = webdriver.ChromeOptions()

        if headless:
            # 无头模式
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')

        _browser = webdriver.Chrome(executable_path="drivers/chromedriver", options=chrome_options)

    elif browser_type == "Edge":
        # Fixme: Edge 的无头模式在 Mac 下会报错
        _browser = Edge(executable_path="drivers/msedgedriver", capabilities={})

    elif browser_type == "Firefox":
        # Firefox
        firefox_options = FirefoxOptions()

        if headless:
            # 无头模式
            firefox_options.add_argument('-headless')
            firefox_options.add_argument('--disable-gpu')

        _browser = webdriver.Firefox(executable_path="drivers/geckodriver", options=firefox_options)

    else:
        _browser = getBrowser(headless=headless, browser_type="Chrome")

    return _browser


def setCookie(cookies=None):
    """
    设置 cookie
    :param cookies: cookie列表
    :return:
    """
    if cookies is None:
        if os.path.exists("cookie.json"):
            with open("cookie.json", "r", encoding="utf-8") as cookies_file:
                cookies = json.loads(cookies_file.read())

                # 首先删除浏览器缓存 Cookie
                browser.delete_all_cookies()
                # 先写入新的 Cookie
                for cookie in cookies:
                    browser.add_cookie(cookie)

                # 刷新页面
                browser.refresh()
                cookies_file.close()
        else:
            # 如果没有 cookie 只能自己登录了
            pass
    else:
        # 首先删除浏览器缓存 Cookie
        browser.delete_all_cookies()
        # 先写入新的 Cookie
        for cookie in cookies:
            browser.add_cookie(cookie)

        # 刷新页面
        browser.refresh()

    # 检测是否需要手动登录
    for _ in range(2):
        try:
            username = browser.find_element_by_class_name('nickname')
            # 保存到 cookie.json
            json.dump(browser.get_cookies(), open("cookie.json", "w", encoding="utf-8"))
            printLog("INFO", "登录成功", "用户名：" + username.text)
            return
        except:
            if _ == 0:
                browser.get("https://passport.jd.com/new/login.aspx")
                printLog("INFO", "未登录", "请在15s内扫码登录")
                time.sleep(20)

    printLog("ERROR", "未登录", "请检查你的账号")
    raise Exception("未登录账号")


def traversals(shop_range):
    # 获取浏览器对象
    _browser = getBrowser(headless=True, browser_type="Chrome")
    _browser.get("http://www.jd.com")
    # 设置等待时间
    wait = WebDriverWait(_browser, 3)
    # 设置浏览器 cookie
    with open("cookie.json", "r", encoding="utf-8") as ck:
        cookies = json.loads(ck.read())

        # 首先删除浏览器缓存 Cookie
        _browser.delete_all_cookies()
        # 先写入新的 Cookie
        for cookie in cookies:
            _browser.add_cookie(cookie)

        # 刷新页面
        _browser.refresh()
        ck.close()
    # 遍历
    for shopID in shop_range:
        shopID = int(shopID)
        try:
            url = "https://mall.jd.com/shopBrandMember-" + str(shopID) + ".html"
            _browser.get(url)
            printLog("DEBUG", "访问店铺链接", url)
            gift_info = _browser.find_element_by_xpath('//*[@id="J_brandMember"]/div[3]/div/ul')

            # 判断入会是否赠送京豆
            if len(re.findall("京豆", gift_info.text)):
                # re.match(r'(\d+)京豆', gift_info.text, re.M | re.I).group(1)
                jd = int(re.match(r'(\d+)京豆', gift_info.text, re.M | re.I).group(1))
                url_info = [{'url': url, 'gift': jd}]
                if shopID != 10000:
                    with open("url.txt", "a", encoding="utf-8") as url_txt_io:
                        url_txt_io.write(str(url_info) + "\n")
                        url_txt_io.close()
                # 入会
                _browser.find_element_by_xpath('//*[@id="J_brandMember"]/div[2]/div/div[3]/p/span[1]').click()
                # 通过class找到按钮并点击成为会员
                wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="J_brandMember"]/div[2]/div/div[4]'))).click()
                # 获取的京豆
                printLog("INFO", "入会成功", "获得" + str(jd) + "京豆")


        except Exception as e:
            # printLog("ERROR", "入会失败", str(e.args))
            pass


def task(shop_range=None, cookies=None):
    """
    任务进程函数
    :param shop_range: 店铺 ID 的范围， 如果没有则默认是所有的店铺 ID
    :param cookies: cookies 如果没有的话需要使用`cookie.json`登录
    :return:
    """
    setCookie(cookies)
    browser.close()
    # 设置进度
    progress = 100
    try:
        shopID = getShopID()
        ran = int(len(shopID) / THREAD)
        for i in range(THREAD):
            r = shopID[i * ran: (i+1) * ran]
            threading.Thread(target=traversals, args=(r, )).start()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    browser = getBrowser(headless=False, browser_type="Chrome")
    THREAD = 2
    try:
        browser.get("http://www.jd.com")
        task()

    except Exception as e:
        print(e)

