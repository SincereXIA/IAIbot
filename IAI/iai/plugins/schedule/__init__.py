from apscheduler.schedulers.asyncio import AsyncIOScheduler
from IAI.iai.plugins.CurriculumSchedule import data_source
from datetime import datetime,date
from IAI.setup import *
import none
import none.command
from IAI import DBdriver

times = 0
async def Curriculum():
    now = datetime.now()
    global  times
    times += 1
    for group in CURRICULUM_ENABLE_GROUP_LIST:
        classInfos = data_source.getRecentClassInfo(now,group,20)
        if not classInfos:
            return
        should_notify = False
        for classInfo in classInfos:
            if classInfo.last_notify_date is None or classInfo.last_notify_date.day != now.day:
                should_notify = True
                notify_date = date(now.year, now.month, now.day)
                classInfo.last_notify_date = notify_date
                session = DBdriver.DBSession()
                session.merge(classInfo)
                session.commit()
                session.close()
        if should_notify:
            ctx = {'message_type': 'group', 'self_id': ROBOT_ID, 'group_id': group}
            await none.command.call_command(none.get_bot(), ctx, "kcb",
                                            args={"next_class": True, 'from_schedule':True})


async def MorningCall():
    for group in MORNING_CALL_ENABLE_GROUP_LIST:
        ctx = {'message_type': 'group', 'self_id': ROBOT_ID, 'group_id': group}
        await none.command.call_command(none.get_bot(), ctx, "morning_call", )


scheduler = AsyncIOScheduler()
scheduler.add_job(Curriculum, 'interval', minutes=1)
scheduler.add_job(MorningCall, 'cron', day_of_week='mon-fri', hour=7, minute=00,)
scheduler.start()
