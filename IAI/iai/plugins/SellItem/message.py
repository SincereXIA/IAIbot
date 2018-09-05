class add_item:
    item_name_msg = '''
请输入你要发布的物品名称：
    '''
    item_info_msg = '''
你要发布：{item_name}
简单的介绍一下它吧：

---
tips：可输入文字/单张图片/文字+图片/
    '''
    item_add_confirm = '''
物品名称：{item_name}
{item_info}

联系方式：{seller_id}

----
>> 以上信息确认无误吗？
确认发布请回复: y
发布并即刻推送到旧物群请回复: t
删除此信息请回复: n
    '''

class find_item:
    item_name_msg = '''
请输入你要查询的关键字：

---
要查看全部信息，请回复 「全部」
    '''
    item_msg = '''
{id}:【{item_name}】
{item_info}
    '''
    item_detail = '''
【{item_name}】
详细信息：
{item_info}

联系：{seller_id}
发布日期：{add_time}
'''
    item_detail_more = '''
---
查看其它物品，请直接回复物品前编号
寻找更多物品？回复 「下一页」
退出会话，请回复 「q」
    '''
    item_list_msg = '''
---
回复 「下一页」 查看更多条目，
回复物品前的数字编号，查看该物品的详细信息和图片
    '''
class user_center:
    item_list_msg = '''
---
回复 「下一页」 查看更多条目，
回复物品前的数字编号，查看该物品的详细信息
    '''
    del_confirm_msg = '''
---
回复「y」确认删除
回复「n」取消操作
    '''
    update_item_name_msg = '''
物品名称：
【{item_name}】

---
请输入新的名称：
不修改请回复 「n」
    '''
    update_item_info_msg = '''
详细信息：
{item_info}

---
请输入新的详细信息：
不修改请回复 「n」
    '''

class want_item:
    item_name_msg = '''
请输入你想收购的物品名称：
        '''
    item_info_msg = '''
你要收购：{item_name}
你还可以提一些更详细的要求：

---
tips：可输入文字/单张图片/文字+图片/
回复 「空格」 跳过
        '''
    item_add_confirm = '''
收购物品：{item_name}
{item_info}

联系方式：{seller_id}

----
>> 以上信息确认无误吗？
确认发布请回复: y
发布并即刻推送到旧物群请回复: t
删除此信息请回复: n
        '''