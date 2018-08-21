import none
import none.command
from none import on_command,CommandSession

@on_command('test')
async def test(session:CommandSession):
    ctx = {'message_type': 'private', 'post_type': 'message', 'raw_message': 'weather', 'self_id': 3316564517, 'sub_type': 'friend', 'time': 1534834232, 'user_id': 937734121}
    await none.command.call_command(none.get_bot(),ctx,)


