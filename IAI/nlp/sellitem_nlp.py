from IAI.nlp import client
async def get_item_nlp(text):
    nrs = client.lexer(text)
    result = []
    for word in nrs['items']:
        if word['pos'] == 'n':
            for i in word['basic_words']:
                result.append(i)

    return result