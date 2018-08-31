from apscheduler.schedulers.asyncio import AsyncIOScheduler
from IAI.iai.plugins.CurriculumSchedule import data_source
from datetime import datetime, date
from IAI.setup import *
import none
import none.command
from IAI import DBdriver
import time
import random
from none import scheduler


@scheduler.scheduled_job('interval', minutes=5)
async def Curriculum():
    now = datetime.now()
    for group in CURRICULUM_ENABLE_GROUP_LIST:
        time.sleep(random.randint(2,6))
        classInfos = await data_source.getRecentClassInfo(now, group, 30)
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
                                            args={"next_class": True, 'from_schedule': True})


@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=7, minute=00,)
async def MorningCall():
    for group in MORNING_CALL_ENABLE_GROUP_LIST:
        time.sleep(random.randint(2, 6))
        ctx = {'message_type': 'group', 'self_id': ROBOT_ID, 'group_id': group}
        await none.command.call_command(none.get_bot(), ctx, "morning_call", )


