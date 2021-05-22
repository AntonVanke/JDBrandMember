import ctypes
import inspect
import sys
import os
import time
import traceback
import json
import atexit
import threading

import urllib3
from selenium import webdriver

from selenium.common.exceptions import WebDriverException, InvalidSessionIdException, NoSuchElementException

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def stop_thread(tid):
    """
    停止线程
    :param tid: 线程
    :return:
    """
    tid = ctypes.c_long(tid.ident)
    exc_type = SystemExit
    if not inspect.isclass(SystemExit):
        exc_type = type(SystemExit)
    ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))


def print_log(info_type="", title="", info=""):
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
    # 默认不显示
    # if info_type == "ERROR":
    #     print("\n\033[0;31m" + log + "\033[0m\n")
    # elif info_type == "INFO":
    #     print("\n" + log)
    with open(get_file_path("logs/jdbm.log"), "a", encoding="utf-8") as log_a_file_io:
        log_a_file_io.write(log + "\n")
    return log


def get_file_path(file_name="") -> str:
    """
    获取文件绝对路径, 防止在某些情况下报错
    :param file_name: 文件名
    :return:
    """
    return os.path.join(os.path.split(sys.argv[0])[0], file_name)


def get_browser(_headless=None):
    """
    获取浏览器对象
    :param _headless: 是否无头模式
    :return:
    """
    if _headless is None:
        _headless = headless

    try:
        options = webdriver.ChromeOptions()
        # 防止在某些情况下报错
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

        if binary != "":
            # 当找不到浏览器时需要在 config 里配置路径
            options.binary_location = binary

        if _headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

        return webdriver.Chrome(executable_path=get_file_path("drivers/chromedriver"), desired_capabilities={},
                                options=options)

    except WebDriverException:
        # TODO
        raise WebDriverException


def add_cookie():
    """
    添加浏览器
    :return:
    """
    browser = get_browser(False)
    browser.get("https://passport.jd.com/new/login.aspx")
    try:
        wait = WebDriverWait(browser, 35)
        username = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'nickname'))).text
        user = {
            "userName": username,
            "bean": 0,
            "timeStamp": 1000000000,
            "cookie": browser.get_cookies()
        }

        # 如果是重复账号则替换
        for _ in range(len(users)):
            if users[_]['userName'] == username:
                print_log("INFO", "重复账号", "已经替换")
                users[_] = user
                browser.close()
                return True

        users.append(user)
        # 为了隐私在日志中用户名并不会保存完整
        print_log("INFO", "添加成功", username[0:-1])
        browser.close()
        return True

    except WebDriverException:
        print_log("ERROR", "添加失败", "请检查是否扫码成功？")
        browser.close()
        return False


def visit(shopid, _browser, _wait):
    """
    :param shopid: 店铺编号
    :param _browser: 浏览器对象
    :param _wait: 等待
    :return:
    """
    try:
        global message
        global shopID
        # 访问页面
        _browser.get("https://mall.jd.com/shopBrandMember-" + str(shopid) + ".html")
        # //*[@id="J_brandMember"]/div[3]/div/ul
        gift_info = _browser.find_element_by_xpath('//*[@id="J_brandMember"]/div[3]/div/ul')
        try:
            shop_name = _browser.find_element_by_xpath('//*[@class="shop-name"]').text
        except NoSuchElementException:
            shop_name = str(shopid) + "号店铺"
        # print(gift_info.text)
        # 替换掉正则表达式
        if "豆" in list(gift_info.text) or "红" in list(gift_info.text):

            # 添加到 shopid.txt
            shopID.append(str(shopid) + "\n")

            for gift in gift_info.text.split("\n"):
                if "豆" in gift:
                    # 判断是否达到阈值
                    if int(gift.replace("京豆", "")) <= threshold:
                        return
                    break

                if "红" in gift:
                    # 判断是否获取红包
                    if not is_get_voucher:
                        return
                    break

            # 入会
            _browser.find_element_by_xpath('//*[@id="J_brandMember"]/div[2]/div/div[3]/p/span[1]').click()
            # 通过class找到按钮并点击成为会员
            _wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="J_brandMember"]/div[2]/div/div[4]'))).click()

            # 实时信息
            message = "在" + shop_name + "获得" + gift

            print_log("INFO", str(shopid) + "入会成功" + gift)

    except WebDriverException:
        pass


def traversals(user: dict, start: int, end: int, step: int = 1):
    """
    遍历
    :param user: 账号
    :param start: shopid 开始的位置
    :param end: shopid 结束的位置
    :param step: step
    :return:
    """
    browser = get_browser(headless)
    try:
        wait = WebDriverWait(browser, 5)
        browser.get("https://www.jd.com/")
        # 写入 cookie
        for cookie in user['cookie']:
            browser.add_cookie(cookie)

        browser.refresh()
        # 验证是否登录成功
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'nickname')))
        # 开始遍历
        for _id in shopID[start:end:step]:
            visit(int(_id), _browser=browser, _wait=wait)
            global process
            process += 1
            # print(_id)
            # add_completed()
    except WebDriverException:
        traceback.print_exc()
        print_log("ERROR", "登录失败", "请使用‘add_cookie.py’添加cookie")
    except ValueError:
        print_log("ERROR", "可能是shopid损坏", "请到github上下载最新的")
    except:
        pass


def distributor():
    """
    分配任务
    :return:
    """
    # TODO: 先遍历指定账号
    for i in range(thread):
        if i == thread - 1:
            threading.Thread(target=traversals, args=(users[use_user - 1], -1, -thread_len, -1,)).start()
        else:
            threading.Thread(target=traversals,
                             args=(users[use_user - 1], i * thread_len, (i + 1) * thread_len, 1,)).start()
    print("当前账号：" + users[use_user - 1]['userName'])
    while threading.active_count() != 1:
        # print(f"\r{process / shopID_len:^5.5f}", end="")
        print(
            "\r正在执行：{:^5.5f}%[{}->{}]状态：{}".format((process / shopID_len) * 100, "=" * int(40 * (process / shopID_len)),
                                                   "*" * (40 - int(40 * (process / shopID_len))), message), end="")
        time.sleep(0.5)
    # 写入 shopID -> shopid.txt
    with open(get_file_path("shopid.txt"), "w") as f:
        newid = list(dict.fromkeys(shopID[::-1]))[::-1]
        for _ in newid:
            if newid[-1] == _:
                f.write(_[0:-1])
            else:
                f.write(_)

    if not use_user:
        # TODO: 如果为 0 则再遍历其它账号
        for _user in range(len(users)):
            if _user != 0:
                print("当前账号：" + users[_user - 1]['userName'])
                threading.Thread(target=traversals, args=(users[_user - 1], -1, int(-thread_len / 10), -1,)).start()
            while threading.active_count() != 1:
                print("\r 等待其它账号执行完成", end=str(message))
                time.sleep(0.47)


def select():
    """
    选择功能
    :return:
    """
    # wfa = True
    while True:
        try:
            # 等待
            time.sleep(1)
            if threading.active_count() == 1:
                #
                # if wfa:
                #     wfa = False
                print(
                    f"\n{'-' * 20}\n如果需要退出，请 ctrl + c 输入 3 退出，否则可能本次运行的结果不会保存\n{'-' * 20}\n{'用户列表':<8}{'用户名':<20}{'京豆数量':<10}{'是否在执行列表':>5}")
                for _user in range(len(users)):
                    print_log("INFO", f"账户名:{users[_user]['userName'][0:-1]}\t\t京豆数量{users[_user].get('bean', 0)}")
                    print(
                        f"{_user + 1:<11}{users[_user]['userName']:<20}{users[_user].get('bean', 0):<10}{not use_user or use_user == _user + 1:>5}")
                choice = int(input("选择\n\t1. 开始执行\n\t2. 添加账号\n\t3. 退出 \n\t>  "))
                if choice == 1:
                    print_log("INFO", "开始执行")
                    distributor()
                elif choice == 2:
                    print_log("INFO", "添加账号")
                    add_cookie()
                elif choice == 3:
                    return
        except ValueError:
            pass
        except KeyboardInterrupt:
            pass


def check_user():
    """
    检查账号是否正常
    :return:
    """
    _browser = get_browser()
    wait = WebDriverWait(_browser, 5)

    # 判断 配置 是否正确
    if use_user > len(users):
        traceback.print_exc()
        print_log("ERROR", "配置错误", "请检查 config>useUser")
        sys.exit()

    # 删除过期的账号
    for _user in range(len(users)):
        print(f"验证账号{_user + 1}中，中途退出可能会误认为账号失效而删除")
        _browser.get("http://www.jd.com")
        for cookie in users[_user]['cookie']:
            _browser.add_cookie(cookie)
        _browser.refresh()
        _browser.get("http://home.jd.com")
        _browser.refresh()

        # 获取京豆数量：可能会随时改变 xpath 路径
        try:
            bean = int(wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/div[1]/div[2]/div[2]/ul/li[2]/div[1]/a'))).text)
            users[_user]['bean'] = bean
        except WebDriverException:
            print_log("ERROR", "获取京豆数量失败")
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'nickname')))
        except WebDriverException:
            # Fixme: 如果中途退出可能会误认为是过期账号
            print_log("INFO", "移除过期账号", users[_user]['userName'][0:-1])
            users.remove(users[_user])
    _browser.close()


def main():
    # 如果没有账号的话直接添加
    if not len(users):
        add_cookie()
    if len(users):
        check_user()
    select()


if __name__ == '__main__':
    if not os.path.exists(get_file_path("config.json")):
        open(get_file_path("config.json"), "w").write("{}")
    if not os.path.exists(get_file_path("shopid.txt")):
        print_log("ERROR", "缺少关键文件", "请到 https://github.com/AntonVanke/JDBrandMember 下载 shopid.txt")
        sys.exit()

    try:
        config = json.load(open(get_file_path("config.json"), "r"))
    except json.decoder.JSONDecodeError:
        traceback.print_exc()
        print_log("ERROR", "CONFIG错误", "请重新打开程序")
        os.remove(get_file_path("config.json"))
        sys.exit()

    # 线程数
    thread = config.get("thread", 6)
    # Chrome 可执行路径
    binary = config.get("binary", "")
    # 刷豆时是否开启 headless
    headless = config.get("headless", True)
    # 默认用户: 0 表示所有用户, 其它代表第几个
    use_user = config.get("useUser", 0)
    # 阈值: 小于等于此阈值的不会入会
    threshold = config.get("threshold", 0)
    # 是否获得红包？: 因为红包的有效期只有十天，所以暂时不想买的不要开启
    is_get_voucher = config.get("isGetVoucher", True)
    # 用户 cookie 列表
    users = config.get("users", [])
    if use_user > len(users):
        use_user = 0

    # 店铺数
    shopID = open(get_file_path("shopid.txt"), "r").readlines()
    shopID_len = len(shopID)
    thread_len = int(shopID_len / thread)

    process = 0
    message = "正在运行"
    # 修复了去重的问题
    if shopID[-1][-1] != "\n":
        shopID[-1] = shopID[-1] + "\n"

    try:
        main()
    finally:

        # 存入 config -> config.json
        config['thread'] = thread
        config['binary'] = binary
        config['headless'] = headless
        config['useUser'] = use_user
        config['threshold'] = threshold
        config['isGetVoucher'] = is_get_voucher
        config['users'] = users
        json.dump(config, open(get_file_path("config.json"), "w"), indent=4, ensure_ascii=False)
        print_log("INFO", "结束运行", traceback.format_exc())
        print("日志已生成，查看./logs/", "Some log data is being generated: ./log/ ...正在关闭，不要退出")
        if os.path.getsize(get_file_path('logs/jdbm.log')) > 10240000:
            print("日志大小过大，建议及时清理")
        # 结束所有进程
        for _ in threading.enumerate()[::-1]:
            stop_thread(_)
