class add_homework_msg:
    get_content = '''
请输入作业内容：

---
tips：可输入文字/单张图片/文字+图片/
    '''
    confirm = '''
科目: {subject_name}
作业: {content}
DDL: {end_date}

----
以上信息确认无误吗？
添加到数据库请回复: 'y'
添加并即刻推送请回复: 't'
删除此作业请回复: 'n'
    '''