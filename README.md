## 京东入会领京豆

1. ### 要求

   1. `Python 3.7+`
   2. 需要 `Chrome`、`Edge(Chromium)`、`FireFox` 等支持`Selenium`的浏览器
   3. 系统支持`Mac`、`Linux`、`Windows`支持`webdriver`的版本

2. ### 安装方式

   脚本采用`Python Selenium`爬取京东入会有礼页面，由于遍历了超过50万个页面，所以运行的时间会比较长，建议挂在服务器上运行

   1. 克隆到本地
      ```shell
      git clone https://github.com/AntonVanke/JDBrandMember.git
      ```

   2. 安装所需的包

      ```shell
      pip3 install -r requirements.txt
      ```

   3. 下载相应的浏览器驱动

      - Chrome
        - 首先访问`chrome://version/`查看浏览器的版本
        - 去访问<http://chromedriver.storage.googleapis.com/index.html>下载对应的`webdriver`放到`drivers`下
      - Edge
        - 访问`edge://version/`查看浏览器的版本
        - <https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/>下载对应的`webdriver`放到`drivers`下
      - Firefox
        - 访问`about:version`查看浏览器的版本
        - <https://github.com/mozilla/geckodriver/releases/>下载对应的`webdriver`放到`drivers`下

   4. 运行

       1. 在本目录下打开终端运行`python main.py`

           >   第一次打开时会生成几个文件，都是可以删除的。第一次登录会提示你扫码登录，以后的登录都可以通过`cookie.json`登录，所以请妥善保管你的`cookies`

3. ### 一些问题

    -   为什么我的积分没有增加呢？

        >   由于京东的店铺比较多，程序是通过遍历所有店铺，选择赠送京豆的店铺加入，所以进程会很缓慢。
        >
        >   在你以前没有用过同类软件的情况下是可以在 10 个小时获得大约 2000 京豆的（具体以各个店铺活动为准），
        >
        >   如果你以前用过此类软件，可能京豆**回报率会很低**

    -   为什么我运行报错了？

        >   可能有以下原因
        >
        >   1.  没有下载驱动放到`drivers`文件夹里，驱动的版本不对
        >
        >       >   请查看文档的第 2 部分安装相应的驱动
        >
        >   2.  你的浏览器版本过低
        >
        >       >   过低的浏览器版本可能并不支持`selenium 3`或者`headless`模式请你升级到最新版本，并使用对应版本的驱动
        >
        >   3.  程序设计的问题
        >
        >       >   很抱歉，由于我是匆忙的写完这个爬虫，可能有很多的不足之处，欢迎提交`issues`和`pull requests`

    -   运行后生成了几个文件，都是什么？

        >   -   url.txt: 是遍历的具有入会送豆的页面 `url`
        >   -   cookie.json: 是你登录京东的`Cookie`**请不要泄露給其他人**
        >   -   log.txt: 日志文件


