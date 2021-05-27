>   这是一个未完成的文档！

[![GitHub all releases](https://img.shields.io/github/downloads/AntonVanke/JDBrandMember/total?style=for-the-badge)](https://github.com/AntonVanke/JDBrandMember/releases/)[![GitHub release (latest by date)](https://img.shields.io/github/v/release/AntonVanke/JDBrandMember?style=for-the-badge)](https://github.com/AntonVanke/JDBrandMember/releases/latest)

## 开始之前

### 风险

1.  京东账号有被黑号的风险，即一定时间内不能参与活动
2.  入会（开卡）有礼会将你的个人信息授权给店铺，所以你可能会收到店铺的推广信息
3.  退会比较麻烦

### 你需要

1.  电脑知道如何安装`Python`环境，手机知道该如何在`Termux`上安装`Python`环境，或者在`ios`上安装`Pythonista`
2.  <u>待补充</u>

>   如果你不能满足条件，你可以去[Release]([Releases · AntonVanke/JDBrandMember (github.com)](https://github.com/AntonVanke/JDBrandMember/releases))查看已经打包好的程序

## 快速开始

1.  下载本项目

    `git clone https://github.com/AntonVanke/JDBrandMember.git`

    或者下载 zip 压缩包

2.  安装所需的包

    `pip install -r requirements.txt`

3.  配置`config.yaml`

    一般你只需要配置好`cookies`字段就行了像是这样：

    ```yam
    cookies:
      - pt_key=******;pt_pin=******
      - pt_key=******;pt_pin=******
    ```

    每个账号占用一行，`-`前面有两个空格而不是<kbd>Tab</kbd>， 后面有一个空格与`cookie`隔开，如果你不知道怎么获取手机京东`cookie`你可以查看这个：<u>待补充</u>

