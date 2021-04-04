import re
import os
import time
import json

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def print_log(info_type="", title="", info=""):
    """
    :param info_type: 日志的等级
    :param title: 日志的标题
    :param info: 日志的信息
    :return:
    """
    try:
        current_url = browser.current_url
    except:
        current_url = "浏览器已关闭"

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
        log_a_file_io.write(log + "  " + current_url + "\n")


def check_login():
    """
    判断当前是否正确登录
    :return: False: 没有登录成功, True: 登录成功
    """
    try:
        # 如果有用户名了就输出
        nickname = browser.find_element_by_class_name('nickname')
        print_log("INFO", "登陆成功", "用户名" + nickname.text)
        # 保存到 cookie.json
        with open("cookie.json", "w", encoding="utf-8") as cookie_file_io:
            cookie_file_io.write(json.dumps(browser.get_cookies()))
            cookie_file_io.close()
        return True
    except:
        # 如果没有用户名就判定为登录失败
        return False


def login_by_user():
    """
    用户手动登录
    :return: True: 登录成功, False: 登录失败
    """
    # 手动登录提示
    print_log("ERROR", "COOKIE信息不正确", "请手动登录")
    # 打开登录页面
    browser.get("https://passport.jd.com/new/login.aspx")
    # 等待登录成功
    for _ in range(10):
        time.sleep(3)
        if check_login():
            return True
    print_log("ERROR", "登录超时", "请在 30s 内登录京东")
    return False


def brand_member(shop_ID=10000, url=None):
    """
    自动入会
    :param url: 传入的url，默认为空
    :param shop_ID: 店铺ID
    :return:
    """
    try:
        if url is None:
            url = "https://mall.jd.com/shopBrandMember-" + str(shop_ID) + ".html"
        browser.get(url)
        print_log("DEBUG", "访问店铺链接", url)
        gift_info = browser.find_element_by_xpath('//*[@id="J_brandMember"]/div[3]/div/ul')

        # 判断入会是否赠送京豆
        if len(re.findall("京豆", gift_info.text)):
            # re.match(r'(\d+)京豆', gift_info.text, re.M | re.I).group(1)
            jd = int(re.match(r'(\d+)京豆', gift_info.text, re.M | re.I).group(1))
            url_info = [{'url': url, 'gift': jd}]
            if shop_ID != 10000:
                with open("url.txt", "a", encoding="utf-8") as url_txt_io:
                    url_txt_io.write(str(url_info) + "\n")
                    url_txt_io.close()
            # 入会
            checkbox = browser.find_element_by_xpath('//*[@id="J_brandMember"]/div[2]/div/div[3]/p/span[1]')
            if not checkbox.is_selected():
                checkbox.click()
                # 通过class找到按钮并点击成为会员
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="J_brandMember"]/div[2]/div/div[4]'))).click()
                # 计算获取的京豆
                global get_jd
                get_jd += jd
                print_log("INFO", "入会成功", "获得" + str(jd) + "京豆")


    except Exception as e:
        # print_log("ERROR", "入会失败", str(e.args))
        pass


def fast_task_main():
    """
    利用之前遍历过的`url.txt`快速获取京豆
    :return:
    """
    # 读取 url.txt
    try:
        with open("url.txt", "r", encoding="utf-8") as url_txt_io:
            url_lists = url_txt_io.readlines()
            for url_list in url_lists:
                url = json.loads(url_list.split("\n")[0].replace("'", '"'))[0]['url']
                brand_member(url=url)
    except:
        pass


def task_main():
    """
    自动入会主任务
    :return: None
    """
    # 读取店铺ID
    try:
        with open("shopId.txt", "r", encoding="utf-8") as id_file_io:
            shop_IDs = id_file_io.readlines()
            for shop_ID in shop_IDs:
                brand_member(int(shop_ID))
    except Exception as e:
        print_log("ERROR", "遍历错误", str(e.args))


def login_by_file():
    """
    通过 cookie.json 登录京东
    """
    if os.path.exists("cookie.json"):
        with open("cookie.json", "r", encoding="utf-8") as config_file_io:
            try:
                config_cookies = json.loads(config_file_io.read())
                # 首先删除旧有的 Cookies
                browser.delete_all_cookies()
                # 在浏览器写入新的 Cookies
                for config_cookie in config_cookies:
                    browser.add_cookie(config_cookie)
                # 刷新页面
                browser.refresh()
                config_file_io.close()
                # 如果判断登录成功
                if check_login():
                    return True
            except json.decoder.JSONDecodeError:
                # cookie 文件不正确
                print_log("ERROR", "Cookie文件损坏", "自动跳转到手动登录")
            finally:
                config_file_io.close()
    # 如果没有登录成功就需要用户手动登录
    return login_by_user()


if __name__ == '__main__':
    # 初始化生成文件
    # cookie.json: 用于记录登录信息
    # log.txt: 用于记录日志
    # url.json: 用于记录 url 链接
    if not os.path.exists("log.txt"):
        with open("log.txt", "a", encoding="utf-8") as log_file_io:
            log_file_io.close()
    if not os.path.exists("url.json"):
        with open("url.txt", "a", encoding="utf-8") as url_file_io:
            url_file_io.close()

    # 如果你安装了相应的浏览器请把相应的注释取消，并将其他注释添加，记得修改文件名字
    # #### Windows  #####
    # Edge 浏览器
    # browser = webdriver.Edge("./drivers/msedgedriver.exe")
    # Chrome 浏览器
    # browser = webdriver.Chrome("./drivers/chromedriver.exe")
    # #### MAC OS   #####
    # Edge 浏览器
    browser = webdriver.Edge(executable_path="./drivers/msedgedriver", capabilities={})
    # Chrome 浏览器
    # browser = webdriver.Chrome("./drivers/chromedriver")

    # 设置等待时间
    wait = WebDriverWait(browser, 3)
    # 访问京东页面
    browser.get("http://www.jd.com")
    # 计算获得的京豆数
    get_jd = 0
    print_log("INFO", "开始运行", "--------------------------")
    # 登录
    try:
        if login_by_file():
            # 首先使用 url.txt 快速刷一遍
            fast_task_main()
            print_log("INFO", "获得" + str(get_jd), "快速刷分结束，将进行遍历刷分")
            # 再逐个遍历
            task_main()
    except Exception as e:
        print_log("ERROR", "错误", str(e.args))
    finally:
        # 退出浏览器
        print_log("INFO", "本次运行", "获得" + str(get_jd) + "京豆")
        print_log("INFO", "运行结束", "--------------------------")
        try:
            browser.close()
        except:
            pass
