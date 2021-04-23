import json

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

from main import get_browser, get_config, get_file, print_log

if __name__ == '__main__':
    """
    用于获取`cookie`
    """
    config = get_config()
    config['headless'] = False
    browser = get_browser(config)
    browser.get("https://passport.jd.com/new/login.aspx")
    try:
        wait = WebDriverWait(browser, 35)
        username = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'nickname'))).text
        user = {
            "userName": username,
            "cookie": browser.get_cookies()
        }
        config['users'].append(user)
        config['headless'] = True
        json.dump(config, open(get_file("./config.json"), "w"), indent=4, ensure_ascii=False)
        print_log("INFO", "成功添加", username)
    except WebDriverException:
        print_log("ERROR", "添加失败")
    finally:
        browser.close()
