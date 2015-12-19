# -*- coding: utf-8 -*-

__author__ = 'mark'

from datetime import datetime
import colors, time

class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        log = Logger()
        log.info("Elapsed time: {:.3f} sec".format(time.time() - self._startTime))
        log.separator()

class Logger():
    def __init__(self):
        pass

    timeformat = '%Y-%m-%d %H:%M:%S'
    def info(self, msg='Information'):
        line = 'INFORMATION: {} - {}\n'.format(datetime.now().strftime(self.timeformat), msg)
        print(colors.yellow(line))
        self.write_('log', line)

    def success(self, msg='Success'):
        line = 'SUCCESS: {} - {}\n'.format(datetime.now().strftime(self.timeformat), msg)
        print(colors.green(line))
        self.write_('log', line)

    def error(self, msg='Error'):
        line = 'ERROR: {} - {}\n'.format(datetime.now().strftime(self.timeformat), msg)
        print(colors.red(line))
        self.write_('error', line)
        self.write_('log', line)

    def separator(self):
        line = '---------------------------------------------------------------\n'
        print(colors.blue(line))

    def write_(self, type, line):
        open('{}.log'.format(type), 'a').write('{}\n'.format(line))