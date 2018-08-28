import requests
import json
import random
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