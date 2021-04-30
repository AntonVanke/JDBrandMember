### 京东入会领京豆

#### 要求

1.  有一定的电脑知识 or 有耐心爱折腾
2.  需要`Chrome(推荐)`、`Edge(Chromium)`、`Firefox`
3.  操作系统需是 Mac([@zc-nju-med](https://github.com/AntonVanke/JDBrandMember/issues/18#issuecomment-830028426)在m1上测试正常)、Linux(在deepin上测试过)、Windows

#### 安装方法

脚本采用`Selenium`遍历京东入会有礼界面，由于遍历了`20000+`个店铺，可能所需要的时间比较长(视电脑情况30min-5h)

1.  克隆到本地

    ```shell
    git clone https://github.com/AntonVanke/JDBrandMember.git
    ```

2.  安装所需要的包

    ```shell
    pip3 install -r requirements.txt
    ```

3.  下载对应的浏览器驱动放到项目的`drivers`文件夹下面

    1.  `chrome`请访问`chrome://version/`查看浏览器的版本，然后去[ChromeDriver Mirror (taobao.org)](https://npm.taobao.org/mirrors/chromedriver/)下载对应的版本/系统驱动

        >   例如 <https://npm.taobao.org/mirrors/chromedriver/90.0.4430.24/>

    2.  `edge`请访问`edge://version/`查看浏览器的版本，[Microsoft Edge - Webdriver (windows.net)](https://msedgewebdriverstorage.z22.web.core.windows.net/)下载

    3.  `Firefox`请访问[Releases · mozilla/geckodriver (github.com)](https://github.com/mozilla/geckodriver/releases/)下载

4.  配置`config.json`

    ```json
    {
        "thread": 6,  # 线程数， 推荐4-8线程
        "browserType": "Chrome",  # Chrome/Edge/Firefox
        "headless": true,  # 无头模式 请保持开启否则多线程情况下窗口比较多
        "binary": "",  # 可执行路径，如果驱动没有找到浏览器的话需要你手动配置
        "useUser": 0,  # 用户下标，默认是0(users[0]第一个用户)
        "users": []  # 用户列表可以通过 add_cookie.py 添加
    }
    ```

5.  添加`cookie`

    请在项目目录下执行`python3 add_cookie.py`， 在打开的浏览器界面登录你的京东，此时你可以看到`config.json`已经有了你的用户信息（**请不要随意泄露你的cookie**）

6.  执行主程序

    在项目目录下执行`python3 main.py`，等待执行完毕即可，你可以访问项目下的`logs/jdbm.log`查看你的日志

####  LICENSE

>  
>   MIT License
>   
>   Copyright (c) 2021 Vanke Anton
>   
>   Permission is hereby granted, free of charge, to any person obtaining a copy
>   of this software and associated documentation files (the "Software"), to deal
>   in the Software without restriction, including without limitation the rights
>   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
>   copies of the Software, and to permit persons to whom the Software is
>   furnished to do so, subject to the following conditions:
>   
>   The above copyright notice and this permission notice shall be included in all
>   copies or substantial portions of the Software.
>   
>   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
>   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
>   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
>   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
>   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
>   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
>   SOFTWARE.
>   