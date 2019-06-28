"""
自然语言处理-datetime
对用户语言中的时间信息进行解析和提取

author: 16030199025 张俊华
"""
from IAI.nlp import client
from datetime import datetime, timedelta
import jieba.posseg as pseg

async def date_nlp(text:str):
    localtime = datetime.now()
    text = text.strip()
    if '月' in text and '日' in text:
        month = int(text[0:text.find('月')].strip())
        day = int(text[text.find('月')+1:text.find('日')].strip())
        time = datetime(year=localtime.year,month=month,day=day)
    else:
        nrs = client.lexer(text)
        time = localtime
        result = {}
        result['debug_info'] = ""
        if '下周' in nrs['text'] or '下星期' in nrs['text']:
            time = time + timedelta(days=7)
        for item in nrs['items']:
            if item['ne'] == 'TIME':
                result['debug_info'] += str(item)
                for word in item['basic_words']:
                    if '明' in word:
                        time = time + timedelta(days=1)
                    if '后' in word:
                        time = time + timedelta(days=2)
                    weekdaynum = [1, 2, 3, 4, 5, 6, 7]
                    weekdayhz = ['一', '二', '三', '四', '五', '六', '日', ]
                    weekday = [0, 1, 2, 3, 4, 5, 6]
                    for num, hz, d in zip(weekdaynum,weekdayhz, weekday):
                        if str(hz) in word or str(num) in word:
                            time = time - timedelta(days=time.weekday() - d)
                            break
    return time

async def date_nlp_jb(text:str):
    localtime = datetime.now()
    text = text.strip()
    if '月' in text and '日' in text:
        month = int(text[0:text.find('月')].strip())
        day = int(text[text.find('月') + 1:text.find('日')].strip())
        time = datetime(year=localtime.year, month=month, day=day)
    else:
        nrs = pseg.cut(text)
        time = localtime
        result = {}
        result['debug_info'] = ""
        for item in nrs:
            if item.flag == 't':
                result['debug_info'] += str(item)
                if '明' in item.word:
                    time = time + timedelta(days=1)
                if '后' in item.word:
                    time = time + timedelta(days=2)
                if '下周' in item.word or '下星期' in item.word:
                    time = time + timedelta(days=7)
                weekdaynum = [1, 2, 3, 4, 5, 6, 7]
                weekdayhz = ['一', '二', '三', '四', '五', '六', '日', ]
                weekday = [0, 1, 2, 3, 4, 5, 6]
                for num, hz, d in zip(weekdaynum, weekdayhz, weekday):
                    if str(hz) in item.word or str(num) in item.word:
                        time = time - timedelta(days=time.weekday() - d)
                        break
            else:
                if '下' in item.word:
                    time = time + timedelta(days=7)
    return time
