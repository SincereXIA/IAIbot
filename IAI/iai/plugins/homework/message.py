class add_homework_msg:
    subject_name_msg = '''
请输入要布置作业的科目：
    '''
    get_content = '''
请输入作业内容：

---
tips：可输入文字/单张图片/文字+图片/
    '''
    confirm = '''
科目: {subject_name}
作业: {content}
收取：{assign_for}
DDL: {end_date}

----
>> 以上信息确认无误吗？
添加到数据库请回复: 'y'
添加并即刻推送请回复: 't'
删除此作业请回复: 'n'
    '''
    end_date_msg = '''
什么时候收？

---
tips：可以输入：明天、后天、下周三、星期4 等
如果对自然语言处理结果不满意，请输入：「10月7日」这样的格式
    '''
    assign_for_msg = '''
收哪些人的？

---
tips：单号、双号、所有人 etc.
    '''

class get_homework_msg:
    no_homework_msg = '''
未获取到任何作业信息

有没有好心人来告诉我作业[CQ:face,id=32]
@我 或 私聊我：「添加作业」 试试吧
    '''
    subject_homework_msg = '''
关于 {subject} 有以下作业信息：
    '''
    homework_msg = '''
【{subject_name}】
作业: {content}
收取：{assign_for}
DDL: {end_date}
    '''