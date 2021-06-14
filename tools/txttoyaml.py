import datetime

'''
将shopid.txt文件的内容格式化到shopid.yaml并保存
'''
with open('./all_shopid.yaml', 'a', encoding='utf-8') as f:
    with open('shopid.txt', "r", encoding="utf-8") as file_obj:
        f.write("shop_id:")
        content = file_obj.read()
        a = content.split("\n")
        print(a)
        for index in a:
            text = f'\n- \'{index}\''
            f.write(text)
        f.write(f"\nupdate_time: {str(datetime.date.today())}")
