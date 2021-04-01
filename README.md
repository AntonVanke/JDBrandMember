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
        - 去访问`http://chromedriver.storage.googleapis.com/index.html`下载对应的`webdriver`放到`drivers`下
      - Edge
        - 访问`edge://version/`查看浏览器的版本
        - `https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/`下载对应的`webdriver`放到`drivers`下
      - Firefox
        - 访问`about:version`查看浏览器的版本
        - `https://github.com/mozilla/geckodriver/releases/`下载对应的`webdriver`放到`drivers`下

