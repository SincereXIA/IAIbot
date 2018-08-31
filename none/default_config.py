"""
Default configurations.

Any derived configurations must import everything from this module
at the very beginning of their code, and then set their own value
to override the default one.

For example:

>>> from none.default_config import *
>>> PORT = 9090
>>> DEBUG = False
>>> SUPERUSERS.add(123456)
>>> NICKNAME = '小明'
"""

from datetime import timedelta

API_ROOT = ''
SECRET = ''
ACCESS_TOKEN = ''
HOST = '127.0.0.1'
IP_ADDRESS = '127.0.0.1'
IP_PORT = '5700'
PORT = 8080
DEBUG = True

SUPERUSERS = set()
NICKNAME = ''
COMMAND_START = {'/', '!', '／', '！'}
COMMAND_SEP = {'/', '.'}
SESSION_EXPIRE_TIMEOUT = timedelta(minutes=2)
SESSION_RUNNING_EXPRESSION = ''
SHORT_MESSAGE_MAX_LENGTH = 50
DEFAULT_CITY = '西安'
APSCHEDULER_CONFIG = {
    'apscheduler.timezone': 'Asia/Shanghai'
}

HOMEWORK_EVERYDAY_ENABLE_GROUP_LIST = [645785939,]
CURRICULUM_ENABLE_GROUP_LIST = [645785939,]
MORNING_CALL_ENABLE_GROUP_LIST = [645785939,]