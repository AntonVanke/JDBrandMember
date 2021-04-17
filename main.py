import json
import os
import re
import sys
import time
import threading
from selenium import webdriver

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
    with open(os.path.join(os.path.split(sys.argv[0])[0], "log.txt"), "a", encoding="utf-8") as log_a_file_io:
        log_a_file_io.write(log + "\n")


def getShopID():
    try:
        with open(os.path.join(os.path.split(sys.argv[0])[0], "shopId.txt"), "r", encoding="utf-8") as id_file_io:
            return id_file_io.readlines()
    except Exception as _e:
        printLog("ERROR", "获取店铺失败", str(_e.args))


def setCookie(cookies=None):
    """
    设置 cookie
    :param cookies: cookie列表
    :return:
    """
    if cookies is None:
        if os.path.exists(os.path.join(os.path.split(sys.argv[0])[0], "cookie.json")):
            with open(os.path.join(os.path.split(sys.argv[0])[0], "cookie.json"), "r", encoding="utf-8") as cookies_file:
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
            username = browser.find_element_by_class_name('nickname').text
            # 保存到 cookie.json
            json.dump(browser.get_cookies(), open("cookie.json", "w", encoding="utf-8"))

            # 获取当前有多少京豆
            browser.get("http://bean.jd.com/myJingBean/list")
            my_beans = int(browser.find_element_by_xpath('//*[@id="main"]/div[3]/div[1]/div[3]').text)

            printLog("INFO", "登录成功", "用户名：" + username + "京豆数：" + str(my_beans))

            return
        except:
            if _ == 0:
                browser.get("https://passport.jd.com/new/login.aspx")
                printLog("INFO", "未登录", "请在15s内扫码登录")
                time.sleep(20)

    printLog("ERROR", "未登录", "请检查你的账号")
    raise Exception("未登录账号")


def visit(shopID, _browser, url=None):
    try:
        # 设置等待时间
        wait = WebDriverWait(_browser, 3)
        if url is None:
            url = "https://mall.jd.com/shopBrandMember-" + str(shopID) + ".html"
        _browser.get(url)
        # printLog("DEBUG", "访问店铺链接", url)        # DEBUG: 截屏
        # _browser.get_screenshot_as_file("./ss.png")
        gift_info = _browser.find_element_by_xpath('//*[@id="J_brandMember"]/div[3]/div/ul')
        # 判断入会是否赠送京豆
        if len(re.findall("京豆", gift_info.text)):
            jd = int(re.match(r'(\d+)京豆', gift_info.text, re.M | re.I).group(1))
            url_info = [{'url': url, 'gift': jd}]
            if shopID != 10000:
                with open(os.path.join(os.path.split(sys.argv[0])[0], "url.txt"), "a", encoding="utf-8") as url_txt_io:
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


def fast_traversals():
    """
    利用之前遍历过的`url.txt`快速获取京豆
    :return:
    """
    # 读取 url.txt
    try:
        with open(os.path.join(os.path.split(sys.argv[0])[0], "url.txt"), "r", encoding="utf-8") as url_txt_io:
            url_lists = url_txt_io.readlines()
            for url_list in url_lists:
                url = json.loads(url_list.split("\n")[0].replace("'", '"'))[0]['url']
                visit(shopID=10000, _browser=browser, url=url)
    except:
        printLog("ERROR", "错误", "快速遍历问题")
        pass


def traversals(shop_list: list):
    global shopID_index
    # 获取浏览器对象
    _browser = getBrowser(headless=True)
    _browser.get("http://www.jd.com")

    # 设置浏览器 cookie
    with open(os.path.join(os.path.split(sys.argv[0])[0], "cookie.json"), "r", encoding="utf-8") as ck:
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
    for shopID in shop_list:
        visit(int(shopID), _browser=_browser)
        shopID_index += 1


def task(cookies=None):
    """
    任务进程函数
    :param cookies: cookies 如果没有的话需要使用`cookie.json`登录
    :return:
    """
    setCookie(cookies)
    fast_traversals()
    # 由于获取了 cookie, 并且执行完了快速刷分，会开启无头模式快速刷分
    browser.close()
    try:
        shopID = getShopID()
        # 设置进度 TODO 一些关于进度方面的东西
        global shopID_len
        shopID_len = len(shopID)

        def progress():
            while True:
                time.sleep(1)
                # FIXME: 在某些终端用 \r 会导致不显示
                print("当前进度: %f%%   \r" % (shopID_index / shopID_len))
                sys.stdout.flush()

        threading.Thread(target=progress).start()
        ran = int(len(shopID) / THREAD)
        for i in range(THREAD):
            r = shopID[i * ran: (i + 1) * ran]
            threading.Thread(target=traversals, args=(r,)).start()
    except Exception as e:
        print(e)


def getBrowser(headless: bool = False):
    """
    获取 browser 对象
    :param headless: 是否开启无头模式
    :return:
    """
    # FIXME：在这设置你的浏览器
    # 由于我用的是 Mac 的 Chrome ，如果你用的是其它的请你下载对应的驱动并修改下面的驱动路径

    # 用其它浏览器可能以下的代码并不合适
    chrome_options = webdriver.ChromeOptions()
    if headless:
        # 无头模式
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    _browser = webdriver.Chrome(executable_path=os.path.join(os.path.split(sys.argv[0])[0], "drivers/chromedriver"), options=chrome_options)

    # 这里提供一些其它浏览器的样例代码
    # # 如果 browser_type == "Edge":
    #     # Fixme: Edge 的无头模式在 Mac 下会报错
    #     # 需要`from msedge.selenium_tools import Edge, EdgeOptions`/`pip3 install msedge-selenium-tools`
    #     _browser = Edge(executable_path="drivers/msedgedriver", capabilities={})

    # # 如果 browser_type == "Firefox":
    #     # Firefox
    #     # 需要`from selenium.webdriver.firefox.options import Options as FirefoxOptions`
    #     firefox_options = FirefoxOptions()
    #
    #     if headless:
    #         # 无头模式
    #         firefox_options.add_argument('-headless')
    #         firefox_options.add_argument('--disable-gpu')
    #
    #     _browser = webdriver.Firefox(executable_path="drivers/geckodriver", options=firefox_options)

    return _browser


if __name__ == '__main__':
    # 线程数量：同时在后台运行几个浏览器推荐在4-16个，**如果同时跑的线程过多可能反而效率有所降低**
    # 如果你的电脑运行后过于卡顿请适当降低线程数量
    THREAD = 8
    # 一些关于进度方面的东西
    shopID_len = shopID_index = 0
    # 在上面设置你的浏览器
    browser = getBrowser(headless=False)
    try:
        browser.get("http://www.jd.com")
        task()

    except Exception as e:
        print(e)
