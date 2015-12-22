# -*- coding: utf-8 -*-

__author__ = 'mark'

import json, sys
from classes import Tester
from logger import Profiler, Logger

params = sys.argv
ownparams = {
    'first': [
        '--create-users',
    ],
    'second': [
        '--create-businesses',
        '--test-users',
    ],
    'third': [
        '--test-businesses',
        '--create-appoinments'
    ],
    'fourth': [
        '--test-appoinments'
    ]
}
funcsstack = {
    'first': [],
    'second': [],
    'third': [],
    'fourth': []
}

for i in range(0, len(params)):
    param = params[i]
    if param in ownparams['first']:
        if isinstance(params[i + 1], int):
            pass

host = 'http://localhost:8080'

with open('paths.json', 'r') as fp, Profiler() as p:
    log = Logger()
    log.info('Starting tests...')
    paths = json.load(fp)
    tester = Tester()
    # tester.createDemo()
    tester.startTest(paths)
    log.info('End tests')

