[![GitHub all releases](https://img.shields.io/github/downloads/AntonVanke/JDBrandMember/total?style=for-the-badge)](https://github.com/AntonVanke/JDBrandMember/releases/)[![GitHub release (latest by date)](https://img.shields.io/github/v/release/AntonVanke/JDBrandMember?style=for-the-badge)](https://github.com/AntonVanke/JDBrandMember/releases/latest)

### 京东入会领京豆

#### 要求

1.  有一定的电脑知识 or 有耐心爱折腾
2.  需要`Chrome(推荐)`
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

        >   `/drivers/`目录默认的驱动是`chromedriver`(如下)，其它需要替换
        >
        >   | Google Chrome | 90.0.4430.212 (正式版本) (x86_64) |
        >   | ------------- | --------------------------------- |
        >   | **操作系统**  | macOS 版本11.4（版号20F5055c）    |
        >
        >   例如 <https://npm.taobao.org/mirrors/chromedriver/90.0.4430.24/>，不要下载成了`LATEST_RELEASE_*`开头的文件了[案例](https://github.com/AntonVanke/JDBrandMember/issues/19#issuecomment-832664967)

    2.  由于增加了兼容性，所以代码默认不提供`Edge(Chromium)`、`Firefox`。如果你想要运行在这些浏览器上请修改`get_browser`函数并在下面的网站获取驱动：
        1.  `edge`请访问`edge://version/`查看浏览器的版本，[Microsoft Edge - Webdriver (windows.net)](https://msedgewebdriverstorage.z22.web.core.windows.net/)下载
        2.  `Firefox`请访问[Releases · mozilla/geckodriver (github.com)](https://github.com/mozilla/geckodriver/releases/)下载


#### 运行

如果你以上步骤执行的没有错误的话，你的文件下会有这些文件：

```floder
-JDBrandMember
|
|- drivers
|	|- chromedriver
|
|- main.py
|- shopid.txt
|
|- requirements.txt
|- README.md & LICENSE
```

##### 首次运行

1.  运行`python3 main.py`，如果没有报错的话，会弹出浏览器页面，此时需要你登录京东

2.  运行之后输入`3`退出，这时你会看到生成了`logs`文件夹和`config.json`

    ```python
    {
        "thread": 6,  # 运行的线程数
        "binary": "",  # 如果驱动没有找到浏览器的话，需要手动配置路径
        "headless": true,  # 是否开启无头模式？建议打开
        "useUser": 0,  # 使用的用户: 0 表示所有、1 代表第 1 个，以此类推
        "threshold": 0,  # 最小京豆数量，小于此的不会入会
        "is_get_voucher": false,  # 是否获取红包，因为红包的有有效期，所以暂时不用的不要开启
        "users": []  # 用户列表
    }
    ```

##### 配置

按照上面的配置你的`config.json`, 执行`python3 main.py`，等待执行完毕即可，你可以访问项目下的`logs/jdbm.log`查看你的日志

##### 注意

不要泄露你的`config.json`

退出时请使用<kbd>Ctrl</kbd>+<kbd>C</kbd>输入 3 退出，否则可能本次运行的结果不会保存， 并且可能会遗留大部分线程[ Issue #23](https://github.com/AntonVanke/JDBrandMember/issues/23#issue-886555670)

#### 较上次更新的内容

1.  京豆阈值([ Issue #23 ](https://github.com/AntonVanke/JDBrandMember/issues/23#issue-886555670)、[ Issue #13](https://github.com/AntonVanke/JDBrandMember/issues/13#issue-869470525))

2.  多账号执行([Issue #20](https://github.com/AntonVanke/JDBrandMember/issues/20#issue-871837264))

3.  突然发现还能领红包？？

    [![红包](https://z3.ax1x.com/2021/05/15/gy373q.jpg)](https://imgtu.com/i/gy373q)

####  LICENSE

>  
>   MIT License
>   
>   Copyright (c) 2021 Vanke Anton
>   

