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
from IAI.iai.common.GroupInfo import get_all_group_info


@scheduler.scheduled_job('interval', minutes=5)
async def Curriculum():
    now = datetime.now()
    for group in await get_all_group_info():
        if group.is_curriculumschedule_on:
            classInfos = await data_source.getRecentClassInfo(now, group.group_id, 30)
            if not classInfos:
                continue
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
                ctx = {'message_type': 'group', 'self_id': ROBOT_ID, 'group_id': group.group_id}
                await none.command.call_command(none.get_bot(), ctx, "kcb",
                                                args={"next_class": True, 'from_schedule': True})
                time.sleep(random.randint(2, 6))


@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=7, minute=00, )
async def MorningCall():
    for group in await get_all_group_info():
        if group.is_morningcall_on:
            time.sleep(random.randint(2, 6))
            ctx = {'message_type': 'group', 'self_id': ROBOT_ID, 'group_id': group.group_id}
            await none.command.call_command(none.get_bot(), ctx, "morning_call", )


@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=19, minute=00, )
async def HomeworkEveryday():
    for group in await get_all_group_info():
        if group.is_homework_daily_on:
            time.sleep(random.randint(2, 6))
            ctx = {'message_type': 'group', 'self_id': ROBOT_ID, 'group_id': group.group_id}
            await none.command.call_command(none.get_bot(), ctx, "homework", args={'from_schedule': True})


@scheduler.scheduled_job('interval', minutes=18)
async def weather_notify():
    for group in await get_all_group_info():
        if group.is_weather_notify_on:
            time.sleep(random.randint(2, 6))
            ctx = {'message_type': 'group', 'self_id': ROBOT_ID, 'group_id': group.group_id}
            await none.command.call_command(none.get_bot(), ctx, "weather_forecast_hourly")
