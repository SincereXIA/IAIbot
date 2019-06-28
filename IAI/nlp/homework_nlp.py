"""
对作业查询功能的自然语言理解

author: 16030199025 张俊华
"""
from IAI.nlp import client
def get_subject_name(text):
    score = client.simnet(text,'作业是什么')
    print(score['score'])

    text = text.replace('的','').replace('是','').replace('啥','').replace('有','').replace('什么','')
    nrs = client.lexer(text)
    subjects = []
    for item in nrs['items']:
        if 'n' in item['pos'] and item['item'] != '作业':
            subjects.append(item['item'])
    result = {'score': score['score'],'subjects':subjects}
    return result


if __name__ == '__main__':
    print(get_subject_name('数据库作业是啥'))
    print(get_subject_name('微原有啥作业'))
    print(get_subject_name('c++有啥作业'))