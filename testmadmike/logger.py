# -*- coding: utf-8 -*-
from datetime import datetime
import colors, sys

class Logger():
    def __init__(self):
        pass

    timeformat = '%Y-%m-%d %H:%M:%S'
    def info(self, msg='Information'):
        line = 'INFORMATION: {} - {}'.format(datetime.now().strftime(self.timeformat), msg)
        print(colors.yellow(line))
        self.write_('log', line)

    def success(self, msg='Success'):
        line = 'SUCCESS: {} - {}'.format(datetime.now().strftime(self.timeformat), msg)
        print(colors.green(line))
        self.write_('log', line)

    def error(self, msg='Error'):
        line = 'ERROR: {} - {}'.format(datetime.now().strftime(self.timeformat), msg)
        print >> sys.stderr, colors.red(line)
        self.write_('error', line)
        self.write_('log', line)

    def write_(self, type, line):
        open('{}.log'.format(type), 'a').write('{}\n'.format(line))