# -*- coding: utf-8 -*-

__author__ = 'mark'

import json, sys
from classes import Tester
from logger import Profiler

params = sys.argv
ownparams = {
    'first': [
        '--create-users',
        '--create-businesses',
        '--create-appoinments'
    ],
    'second': [
        '--test-users',
        '--test-businesses',
        '--test-appoinments'
    ]
}

for i in range(0, len(params)):
    param = params[i]
    if param in ownparams['high']:
        if isinstance(params[i + 1], int):
            pass

host = 'http://localhost:8080'

with open('paths.json', 'r') as fp, Profiler() as p:
    paths = json.load(fp)
    tester = Tester()
    # tester.createDemo()
    tester.startTest(paths)

