import none
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def test():
    ctx = {'message_type': 'private', 'self_id': 3316564517, 'user_id': 937734121}
    await none.command.call_command(none.get_bot(),ctx,"weather", args={"city":"西安"})


scheduler = AsyncIOScheduler()
#scheduler.add_job(test, 'interval', seconds=15)
#scheduler.start()
