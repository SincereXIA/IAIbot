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
PORT = 8080
DEBUG = True

SUPERUSERS = set()
NICKNAME = ''
COMMAND_START = {'/', '!', '／', '！'}
COMMAND_SEP = {'/', '.'}
SESSION_EXPIRE_TIMEOUT = timedelta(minutes=5)
SESSION_RUNNING_EXPRESSION = '您有命令正在执行，请稍后再试'
SHORT_MESSAGE_MAX_LENGTH = 50
BD_API_KEY = ''
BD_SECRET_KEY = ''

DB_TABLE = 'iaibot'
DB_USER = 'root'
DB_PASSWORD = ''
DB_PORT = 3306
DB_ADDRESS = '127.0.0.1'
DEFAULT_GROUP = None
ROBOT_ID = None

CURRICULUM_ENABLE_GROUP_LIST = []
DEFAULT_CITY = '西安'
