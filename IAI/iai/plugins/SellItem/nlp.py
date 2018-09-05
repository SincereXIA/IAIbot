from none import natural_language,NLPSession,NLPResult,on_natural_language
from IAI.nlp.sellitem_nlp import get_item_nlp
@on_natural_language('有谁想要',)
async def _(session:NLPSession):
    if '有谁想要' not in session.msg_text:
        return
    if session.msg_text.strip() == '有谁想要':
        return NLPResult(90,'find_item',{'type':'want','key_word':None})
    elif ' ' in session.msg_text.strip():
        key_words = session.msg_text.strip().split()
        key_words.pop(0)
        return NLPResult(90, 'find_item', {'type': 'want', 'key_word': key_words})
    else:
        key_words  = await get_item_nlp(session.msg_text)
        return NLPResult(90, 'find_item', {'type': 'want', 'key_word':key_words})

@on_natural_language('出')
async def _(session:NLPSession):
    if session.msg_text.strip()[0] == '出':
        if session.msg_text.strip() == '出':
            return NLPResult(90,'add_item',)
        else:
            item_name = session.msg_text.strip()[1:]
            return NLPResult(90,'add_item',{'item_name':item_name})

@on_natural_language('我想要')
async def _(session:NLPSession):
    if '我想要' not in session.msg_text:
        return
    if session.msg_text.strip() == '我想要':
        return NLPResult(90,'find_item',{'type':'sell','key_word':None})
    else:
        key_words  = await get_item_nlp(session.msg_text)
        return NLPResult(90,'find_item', {'type': 'sell', 'key_word':key_words})

@on_natural_language('收')
async def _(session:NLPSession):
    if session.msg_text.strip()[0] == '收':
        if session.msg_text.strip() == '收':
            return NLPResult(90,'want_item',)
        else:
            item_name = session.msg_text.strip()[1:]
            return NLPResult(90,'want_item',{'item_name':item_name})