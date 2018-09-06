from IAI.nlp import client
async def get_item_nlp(text):
    nrs = client.lexer(text)
    result = []
    for word in nrs['items']:
        if word['pos'] == 'n':
            result.append(word['item'])

    return result