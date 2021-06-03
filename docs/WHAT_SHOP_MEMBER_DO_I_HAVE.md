 [返回 README](../README.md) 

# 我有哪些店铺的会员？

或者应该说我加入的店铺的`VenderId`是多少？或许`tools/get_user_brand_member.py`可以帮助到你。

假设你的`Cookie`是`pt_key=123465abc;pt_pin=jd_123987`

运行`python3 get_user_brand_member.py [cookie.pt_key] [cookie.pt_pin]`例：

````bash
python3 get_user_brand_member.py 123465abc jd_123987
````

或者在`tools/get_user_brand_member.py`里编辑

```python
COOKIE = "" or "pt_key=" + sys.argv[1] + ";pt_pin=" + sys.argv[2]
```

两个引号之间添加你的`cookie`，例：

```python
COOKIE = "pt_key=123465abc;pt_pin=jd_123987" or "pt_key=" + sys.argv[1] + ";pt_pin=" + sys.argv[2]
```

那么就会在同级目录生成`user_shop_venderId.txt`，你可以将这个用于退会。

### 怎么退会？

>   访问`https://shopmember.m.jd.com/member/memberCloseAccount?venderId=[venderId]`就可以了
>
>   你也可以使用 @yqchilde 大佬的[JDMemberCloseAccount](https://github.com/yqchilde/JDMemberCloseAccount)来退会。

注意`venderID`和退会需要的`brandId`有时相同功效有时不同，这个不太清楚为什么。`user_shop_venderId.txt`生成会覆盖以前生成的。
