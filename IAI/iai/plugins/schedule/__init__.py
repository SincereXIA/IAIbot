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
        classInfo = data_source.getRecentClassInfo(now,group,20)
        if not classInfo:
            return
        if classInfo.last_notify_date is None or classInfo.last_notify_date.day != now.day:
            ctx = {'message_type': 'group', 'self_id': ROBOT_ID, 'group_id':group}
            await none.command.call_command(none.get_bot(), ctx, "kcb", args={"next_class": True})
            notify_date = date(now.year, now.month, now.day)
            classInfo.last_notify_date = notify_date
            session = DBdriver.DBSession()
            session.merge(classInfo)
            session.commit()
            session.close()



scheduler = AsyncIOScheduler()
scheduler.add_job(Curriculum, 'interval', seconds=1)
scheduler.start()
