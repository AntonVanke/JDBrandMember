 [返回 README](../README.md) 

# 如何获取COOKIE？

### 通过电脑浏览器获取京东`COOKIE`

1.  打开`Chrome`浏览器，打开开发者工具

    ![浏览器示例](/docs/_images/20210528150201.png)

2.  切换设备为手机模式，并转至`NetWork`标签页

3.  访问 [https://home.m.jd.com/myJd/newhome.action](https://home.m.jd.com/myJd/newhome.action) 输入手机号验证码登录，

4.  **登录成功后**在右边的网络框里找到第一个点击，在`Headers`的`Requsets Headers`找到`pt_key=******;pt_pin=******`复制即可

    或者到`Application`标签下的`Storage->Cookie->https://home.m.jd.com`查看`pt_key`和`pt_pin`

### 通过手机获取京东COOKIE

1.  使用黄鸟(`Httpcanary`)或者锤子(`Thor`)抓包获取`COOKIES`；
2.  如果你用过京东的脚本(`像jd助手`， `圈X脚本`)，那么你同样可以用里面的`Cookie`；

### 待补充
