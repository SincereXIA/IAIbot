from os import path

import none

import setup

if __name__ == '__main__':
    none.init(setup)
    none.load_builtin_plugins()
    none.load_plugins(path.join(path.dirname(__file__),'iai','plugins'),
                      'iai.plugins')
    none.run(host='127.0.0.1', port=8082)