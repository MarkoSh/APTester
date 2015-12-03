# -*- coding: utf-8 -*-

__author__ = 'mark'

import requests, json, random
from testmadmike.logger import Logger
import hashlib

class Tester():
    def __init__(self, host='http://localhost:8080'):
        self.host = host
        self.log = Logger()

    def createDemo(self):
        ## Creating users
        for i in range(0, 10):
            string = hashlib.sha224()
            string.update('{}'.format(random.random()))
            first = 'first{}'.format(string.hexdigest()[0:10])
            string.update('{}'.format(random.random()))
            last = 'last{}'.format(string.hexdigest()[0:10])
            email = 'email{}'.format(string.hexdigest()[0:10])
            req = requests.post(url='{}{}'.format(self.host, '/v2/user/register'), data={
                'first': first,
                'last': last,
                'tel': '8001234567',
                'email': '{}@localhost.email'.format(email),
                'pass': 'password',
                'type': 'customer',
            })
            respone = req.json()
            pass

    def removeDemo(self):


        pass

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
                if path_['param'] is not None and param is not None:
                    try:
                        path_['param'] += param
                    except TypeError as e:
                        self.log.error(e)
                else:
                    path_['param'] = param

                if 'subs' in path_ and path_['subs']['func'] is None:
                    path_['subs']['func'] = func
                self.test(path_, path)
        else:
            link = '{}{}'.format(self.host, path['path'])
            if func == 'checkStatus':
                self.log.info('{}, function: {}'.format(link, path['func']))
                data = requests.get(url=link)
                if data.status_code == path['response']:
                    if data.status_code == requests.codes.ok:
                        self.log.info('{} available, status is {} - correct'.format(link, data.status_code))
                        try:
                            self.log.info('{}, message: {}'.format(link, data.json()['message']))
                        except ValueError as e:
                            self.log.error('{}, error: {}'.format(link, e))
                    else:
                        self.log.info('{} available, status is {} - correct'.format(link, data.status_code))
                else:
                    self.log.error('Url {} unavailable, status is {} - incorrect'.format(link, data.status_code))
                    exit()
            elif func == 'testBusiness':
                self.log.info('{}, function: {}'.format(link, path['func']))
            elif func == 'testUser':
                self.log.info('{}, function: {}'.format(link, path['func']))
            self.log.info(param)
