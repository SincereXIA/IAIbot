from os import path
import sys
import setup
import os

import nonebot as none



if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    none.init(setup)
    none.load_builtin_plugins()
    none.load_plugins(path.join(path.dirname(__file__),'iai','plugins'),
                      'iai.plugins')
    none.run()