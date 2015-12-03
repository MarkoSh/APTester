# -*- coding: utf-8 -*-

__author__ = 'mark'

import urllib2, json
from testmadmike.logger import Logger

class Tester():
    def __init__(self, host='http://localhost:8080'):
        self.host = host
        self.log = Logger()

    def startTest(self, paths):
        for path in paths:
            if path['skip'] and 'subs' in path or 'subs' in path:
                for path_ in path['subs']['items']:
                    if path_['func'] is None:
                        path_['func'] = path['subs']['func']
                    if 'subs' in path_ and path_['subs']['func'] is None:
                        path_['subs']['func'] = path['subs']['func']
                    self.test(path_, path)

    def test(self, path, parent):
        path['path'] = parent['path'] + path['path']
        func = path['func']
        param = path['param']

        if func is None:
            func = parent['subs']['func']

        if param is None:
            param = parent['param']
        elif parent['param'] is not None:
            param = list(set(param + parent['param']))

        if path['skip'] and 'subs' in path or 'subs' in path:
            for path_ in path['subs']['items']:
                path_['func'] = func
                if path_['param'] is not None:
                    path_['param'] += param
                else:
                    path_['param'] = param

                if 'subs' in path_ and path_['subs']['func'] is None:
                    path_['subs']['func'] = func
                self.test(path_, path)
        else:
            link = '{}{}'.format(self.host, path['path'])

            if func == 'checkStatus':
                self.log.info('{}, function: {}'.format(link, path['func']))
                try:
                    data = urllib2.urlopen(url=link)
                    if data.code == path['response']:
                        self.log.info('{} available, status is {} - correct'.format(link, data.code))
                        try:
                            object = json.load(data.fp)
                            self.log.info('{}, message: {}'.format(link, object['message']))
                        except ValueError as e:
                            self.log.error('{}, error: {}'.format(link, e))
                except urllib2.HTTPError as data:
                    if data.code == path['response']:
                        self.log.info('Url {} unavailable, status is {} - correct'.format(link, data.code))
                    else:
                        self.log.error('Url {} unavailable, status is {} - incorrect'.format(link, data.code))
                        exit()

            elif func == 'testBusiness':
                self.log.info('{}, function: {}'.format(link, path['func']))

            elif func == 'testUser':
                self.log.info('{}, function: {}'.format(link, path['func']))

            else:
                self.log.info('{} has not function'.format(link))

            self.log.info(param)
