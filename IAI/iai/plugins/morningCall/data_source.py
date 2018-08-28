import requests
import json
import random
from IAI.iai.plugins.CurriculumSchedule.data_source import getClassInfoFromTime
from datetime import datetime

async def get_one_content():
    idlist = requests.get('http://v3.wufazhuce.com:8000/api/onelist/idlist')
    idlist = json.loads(idlist.text)
    id = int(idlist['data'][0])
    content = requests.get(f'http://v3.wufazhuce.com:8000/api/onelist/{id-random.randint(0,300)}/0')
    content = json.loads(content.text)
    result = {}
    result['text'] = content['data']['content_list'][0]['forward']
    result['info'] = content['data']['content_list'][0]['words_info']
    return result




async def get_today_class_info(group_id):
    localtime = datetime.now()
    full_infos = getClassInfoFromTime(localtime,group_id)
    info = []
    class_num = ['1-2','3-4','5-6','7-8','9-10']
    for full_info in full_infos:
        i = {}
        i['class_num'] = class_num[full_info.class_num-1]
        i['class_name'] = full_info.class_name
        info.append(i)

    return info

