# -*- coding: utf-8 -*-

__author__ = 'mark'

import json
from classes import Tester
from logger import Profiler

host = 'http://localhost:8080'

with open('paths.json', 'r') as fp, Profiler() as p:
    paths = json.load(fp)
    tester = Tester()
    # tester.createDemo()
    tester.startTest(paths)

