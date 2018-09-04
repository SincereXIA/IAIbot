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
确认发布请回复: 'y'
发布并即刻推送到交易群请回复: 't'
删除此信息请回复: 'n'
    '''

class find_item:
    item_name_msg = '''
请输入你要查询的关键字：
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