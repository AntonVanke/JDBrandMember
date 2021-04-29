import json
import os
import sys

import threading
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

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
    if not os.path.exists(get_file("./logs")):
        os.mkdir(get_file("./logs/"))
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log = now + "  " + info_type + "  " + title + "  " + info
    # 暂时屏蔽了输出
    if info_type == "ERROR":
        print("\n\033[0;31m" + log + "\033[0m\n")
    elif info_type == "INFO":
        print("\n" + log)
    with open(get_file("./logs/jdbm.log"), "a", encoding="utf-8") as log_a_file_io:
        log_a_file_io.write(log + "\n")


def get_file(file_name=""):
    """
    获取文件绝对路径, 防止在某些情况下报错
    :param file_name: 文件名
    :return:
    """
    return os.path.join(os.path.split(sys.argv[0])[0], file_name)


def get_config():
    """
    获取配置
    :return:
    """
    return json.load(open(get_file("config.json")))


def get_browser(_config):
    """
    获取浏览器对象
    :return:
    """
    browser_type = _config['browserType']
    headless = _config['headless']
    binary = _config['binary']

    try:
        if browser_type == 'Chrome':
            chrome_options = webdriver.ChromeOptions()
            # 防止在某些情况下报错`
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
            if binary != "":
                # 当找不到浏览器时需要在 config 里配置路径
                chrome_options.binary_location = binary
            if headless:
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
            if sys.platform == 'linux':
                _browser = webdriver.Chrome(executable_path=get_file("./drivers/chromedriver"), desired_capabilities={},
                                            options=chrome_options)
            elif sys.platform == 'darwin':
                _browser = webdriver.Chrome(executable_path=get_file("./drivers/chromedriver"), desired_capabilities={},
                                            options=chrome_options)
            elif sys.platform == 'win32':
                _browser = webdriver.Chrome(executable_path=get_file("./drivers/chromedriver"), desired_capabilities={},
                                            options=chrome_options)

        elif browser_type == 'Edge':
            from msedge.selenium_tools import Edge, EdgeOptions
            edge_options = EdgeOptions()
            edge_options.use_chromium = True
            edge_options.add_argument('--no-sandbox')
            edge_options.add_argument('--disable-dev-shm-usage')
            edge_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
            if binary != "":
                edge_options.binary_location = binary
            if headless:
                edge_options.add_argument('--headless')
                edge_options.add_argument('--disable-gpu')
            if sys.platform == 'linux':
                _browser = Edge(executable_path=get_file("./drivers/msedgedriver"), options=edge_options,
                                capabilities={})
            elif sys.platform == 'darwin':
                _browser = Edge(executable_path=get_file("./drivers/msedgedriver"), capabilities={},
                                options=edge_options)
            elif sys.platform == 'win32':
                _browser = Edge(executable_path=get_file("./drivers/msedgedriver"), capabilities={},
                                options=edge_options)

        elif browser_type == 'Firefox':
            # 先清除上次的日志
            if not os.path.exists(get_file("./logs")):
                os.mkdir(get_file("./logs/"))
            open(get_file("./logs/geckodriver.log"), "w").close()

            firefox_options = webdriver.FirefoxOptions()
            firefox_options.log.level = "fatal"
            if binary != "":
                firefox_options.binary_location = binary
            if headless:
                firefox_options.add_argument('--headless')
                firefox_options.add_argument('--disable-gpu')
            if sys.platform == 'linux':
                _browser = webdriver.Firefox(executable_path=get_file('./drivers/geckodriver'), options=firefox_options,
                                             service_log_path=get_file("./logs/geckodriver.log"))
            elif sys.platform == 'darwin':
                _browser = webdriver.Firefox(executable_path=get_file('./drivers/geckodriver'), options=firefox_options)
            elif sys.platform == 'win32':
                _browser = webdriver.Firefox(executable_path=get_file('./drivers/geckodriver'), options=firefox_options)
        else:
            raise WebDriverException
        return _browser
    except WebDriverException:
        # 驱动问题
        print_log("ERROR", "浏览器错误", "请检查你的驱动和配置")


def visit(shopid, _browser, _wait):
    """
    :param shopid: 店铺编号
    :param _browser: 浏览器对象
    :param _wait: 等待
    :return:
    """
    try:
        # 访问页面
        _browser.get("https://mall.jd.com/shopBrandMember-" + str(shopid) + ".html")
        gift_info = _browser.find_element_by_xpath('//*[@id="J_brandMember"]/div[3]/div/ul')
        # 替换掉正则表达式
        if "豆" in list(gift_info.text):
            jd = ""
            for gift in gift_info.text.split("\n"):
                if "豆" in gift:
                    jd = gift.replace("京豆", "")
            # 入会
            _browser.find_element_by_xpath('//*[@id="J_brandMember"]/div[2]/div/div[3]/p/span[1]').click()
            # 通过class找到按钮并点击成为会员
            _wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="J_brandMember"]/div[2]/div/div[4]'))).click()
            # 添加到最后
            global shopID
            shopID.append(str(shopid) + '\n')
            # 获取的京豆
            global get_jd
            get_jd += int(jd)
            print_log("INFO", str(shopid) + "入会成功", "获得" + str(jd) + "京豆")
            # 写入
            with open(get_file("shopid.txt"), "w") as f:
                newid = list(dict.fromkeys(shopID[::-1]))[::-1]
                for _ in newid:
                    if newid[-1] == _:
                        f.write(_[0:-1])
                    else:
                        f.write(_)

    except WebDriverException:
        pass
    except AttributeError:
        # fixme:
        pass


def traversals(start: int, end: int, step: int = 1):
    """
    遍历
    :param start: 开始的位置
    :param end: 结束的位置
    :param step: step
    :return:
    """
    try:
        browser = get_browser(config)
        wait = WebDriverWait(browser, 8)
        browser.get("https://www.jd.com/")
        # 写入 cookie
        for cookie in config['users'][config['useUser']]['cookie']:
            # 在某些网络环境下可能会登录异常
            cookie['domain'] = ".jd.com"
            browser.add_cookie(cookie)
        browser.get("https://home.jd.com/")
        browser.refresh()
        # 验证是否登录成功
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'nickname')))
        # 开始遍历
        for _id in shopID[start:end:step]:
            visit(int(_id), _browser=browser, _wait=wait)
            add_completed()
    except WebDriverException:
        traceback.print_exc()
        print_log("ERROR", "登录失败", "请使用‘add_cookie.py’添加cookie")
    except ValueError:
        print_log("ERROR", "可能是shopid损坏", "请到github上下载最新的")
    except IndexError:
        print_log("ERROR", "请先登录", "请检查config的'useUser'")


def main():
    """
    :return:
    """
    # fixme: 在某些情况下线程不能完全停止
    for i in range(THREAD):
        if i == THREAD - 1:
            # t(start=-1, end=-THREAD_LEN)
            t = threading.Thread(target=traversals, args=(-1, -THREAD_LEN, -1,))
            # t.setDaemon(True)
            t.start()
            # thread_list.append(t)
        else:
            # 优先执行上次送豆的
            # t(start=i * THREAD_LEN, end=(i + 1) * THREAD_LEN)
            t = threading.Thread(target=traversals, args=(i * THREAD_LEN, (i + 1) * THREAD_LEN, 1,))
            # t.setDaemon(True)
            t.start()
            # thread_list.append(t)


    # 所有结束时才会结束
    while threading.active_count() != 1:
        time.sleep(3)
        print_process()


def add_completed():
    """
    增加进度
    :return:
    """
    global completed
    completed += 1


def print_process():
    """
    打印进度
    :return:
    """
    # print("\r {:.5f}%".format(completed / ID_LEN), end="")
    print("\r正在执行：{:^5.3f}%[{}->{}]此次运行获得{}京豆".format((completed / ID_LEN) * 100, "=" * int(50 * (completed / ID_LEN)),
                                            "*" * (50 - int(50 * (completed / ID_LEN))), get_jd), end="")


if __name__ == '__main__':
    try:
        config = get_config()
        # 线程数
        THREAD = config['thread']
        # 店铺数
        shopID = open(get_file("shopid.txt"), "r").readlines()

        # 修复了去重的问题
        if shopID[-1][-1] != "\n":
            shopID[-1] = shopID[-1] + "\n"

        ID_LEN = len(shopID)
        completed = 0
        # 每个线程的店铺数
        THREAD_LEN = int(ID_LEN / THREAD)
        # 获得京豆数
        get_jd = 0
        # main
        main()
    except Exception as e:
        print_log("ERROR", "运行错误", str(e.args))
    finally:
        print("运行结束")
