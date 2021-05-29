 [返回 README](../README.md) 

##  怎么生成shopid.yaml

假设你的`Cookie`是`pt_key=123465abc;pt_pin=jd_123987`

运行`python3 traversal.py [cookie.pt_key] [cookie.pt_pin]`例：

````bash
python3 traversal.py 123465abc jd_123987
````

或者在`tools/traversal.py`里编辑

```python
COOKIE = "" or "pt_key=" + sys.argv[1] + ";pt_pin=" + sys.argv[2]
```

两个引号之间添加你的`cookie`，例：

```python
COOKIE = "pt_key=123465abc;pt_pin=jd_123987" or "pt_key=" + sys.argv[1] + ";pt_pin=" + sys.argv[2]
```

那么就会在同级目录生成`shopid.yaml`，你可以将这个用于遍历。一般来说`https://antonvanke.github.io/JDBrandMember/shopid.yaml`是更新日最全的

**注**：生成的`shopid.yaml`在`tools`目录下，你可能需要移动到项目根目录才能用于遍历

