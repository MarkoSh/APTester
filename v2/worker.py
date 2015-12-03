# -*- coding: utf-8 -*-

__author__ = 'mark'

import json
from v2.classes import Tester


host = 'http://localhost:8080'
paths = json.load(open('../paths.json', 'r'))
paths_ = [path for path in [path['subs'] for path in paths]][0]

tester = Tester()
# tester.createDemo()
tester.startTest(paths)

