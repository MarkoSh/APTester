# -*- coding: utf-8 -*-

__author__ = 'mark'

import json
from v2.classes import Tester


host = 'http://localhost:8080'
paths = json.load(open('../paths.json', 'r'))

tester = Tester()
tester.startTest(paths)

