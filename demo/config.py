import re

from none.default_config import *

HOST = '127.0.0.1'
PORT = '8084'
SECRET = 'abc'

SUPERUSERS = {1002647525}
NICKNAME = {'奶茶', '小奶茶'}
COMMAND_START = {'', '/', '!', '／', '！', re.compile(r'^>+\s*')}
COMMAND_SEP = {'/', '.', re.compile(r'#|::?')}
