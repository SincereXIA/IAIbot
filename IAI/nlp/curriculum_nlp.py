from IAI.nlp import client
from datetime import datetime
from . import datetime_nlp
async def curriculum_nlp(text):
    nrs = client.lexer(text)
    curriculumStart = datetime(2018, 9, 3)  # todo 自定义设置
    result ={}
    time = await datetime_nlp.date_nlp(text)
    result['week'] = (int(time.strftime("%j")) - int(curriculumStart.strftime("%j")))//7 + 1
    result['weekday'] = time.weekday()
    result['classnums'] = []
    result['next_class'] = False
    result['debug_info'] = ""
    for item in nrs['items']:
        if item['ne'] == 'TIME':
            result['debug_info'] += str(item)
            for word in item['basic_words']:
                if '早' in word or '上午' in word:
                    result['classnums'].extend([1,2])
                if '下午' in word :
                    result['classnums'].extend([3,4])
    if not result['classnums']:
        if '下' in text:
            result['next_class'] = True
        result['classnums'] = [1,2,3,4,5]

    result['score'] = client.simnet(text,"要上什么课")['score']
    print(result['score'])
    return result

