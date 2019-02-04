from none import natural_language,NLPSession,NLPResult,on_natural_language,get_bot
from IAI.nlp.sellitem_nlp import get_item_nlp
@on_natural_language('谁想要',only_to_me=False)
async def _(session:NLPSession):
    if not session.ctx['to_me']:
        if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in get_bot().config.SELL_GROUP:
            return
    if '谁想要' not in session.msg_text:
        return
    if session.msg_text.strip() == '谁想要':
        return NLPResult(90,'find_item',{'type':'want','key_word':None})
    elif ' ' in session.msg_text.strip():
        key_words = session.msg_text.strip().split()
        key_words.pop(0)
        return NLPResult(90, 'find_item', {'type': 'want', 'key_word': key_words})
    else:
        key_words  = await get_item_nlp(session.msg_text)
        return NLPResult(90, 'find_item', {'type': 'want', 'key_word':key_words})

@on_natural_language('出',only_to_me=False)
async def _(session:NLPSession):
    if not session.ctx['to_me']:
        if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in get_bot().config.SELL_GROUP:
            return
    if session.msg_text.strip()[0] == '出':
        if session.msg_text.strip() == '出':
            return NLPResult(90,'add_item',)
        else:
            item_name = session.msg_text.strip()[1:]
            return NLPResult(90,'add_item',{'item_name':item_name})

@on_natural_language('我想要')
async def _(session:NLPSession):
    if not session.ctx['to_me']:
        if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in get_bot().config.SELL_GROUP:
            return
    if '我想要' not in session.msg_text:
        return
    if session.msg_text.strip() == '我想要':
        return NLPResult(90,'find_item',{'type':'sell','key_word':None})
    elif ' ' in session.msg_text.strip():
        key_words = session.msg_text.strip().split()
        key_words.pop(0)
        return NLPResult(90, 'find_item', {'type': 'sell', 'key_word': key_words})
    else:
        key_words  = await get_item_nlp(session.msg_text)
        return NLPResult(90,'find_item', {'type': 'sell', 'key_word':key_words})
@on_natural_language('收')
async def _(session:NLPSession):
    if not session.ctx['to_me']:
        if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in get_bot().config.SELL_GROUP:
            return
    if session.msg_text.strip()[0] != '收':
        return
    if session.msg_text.strip() == '收':
        return NLPResult(90,'find_item',{'type':'sell','key_word':None})
    elif ' ' in session.msg_text.strip():
        key_words = session.msg_text.strip().split()
        key_words.pop(0)
        return NLPResult(90, 'find_item', {'type': 'sell', 'key_word': key_words})
    else:
        key_words  = await get_item_nlp(session.msg_text)
        return NLPResult(90,'find_item', {'type': 'sell', 'key_word':key_words})

@on_natural_language('收',only_to_me=True)
async def _(session:NLPSession):
    if not session.ctx['to_me']:
        if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in get_bot().config.SELL_GROUP:
            return
    if session.msg_text.strip()[0] == '收':
        if session.msg_text.strip() == '收':
            return NLPResult(92,'want_item',)
        else:
            item_name = session.msg_text.strip()[1:]
            return NLPResult(92,'want_item',{'item_name':item_name})
@on_natural_language('求',only_to_me=True)
async def _(session:NLPSession):
    if not session.ctx['to_me']:
        if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in get_bot().config.SELL_GROUP:
            return
    if session.msg_text.strip()[0] == '求':
        if session.msg_text.strip() == '求':
            return NLPResult(90,'want_item',)
        else:
            item_name = session.msg_text.strip()[1:]
            return NLPResult(90,'want_item',{'item_name':item_name})

@on_natural_language('删',only_to_me=False)
async def _(session:NLPSession):
    if not session.ctx['to_me']:
        if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in get_bot().config.SELL_GROUP:
            return
    if session.msg_text.strip()[0] == '删':
        id = session.msg_text.strip()[1:]
        try:
            int(id)
            return NLPResult(90,'del_item',{'id':id})
        except Exception:
            pass
@on_natural_language('改',only_to_me=False)
async def _(session:NLPSession):
    if not session.ctx['to_me']:
        if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in get_bot().config.SELL_GROUP:
            return
    if session.msg_text.strip()[0] == '改':
        id = session.msg_text.strip()[1:]
        try:
            int(id)
            return NLPResult(90,'update_item',{'id':id})
        except Exception:
            pass