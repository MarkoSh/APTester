# -*- coding: utf-8 -*-

__author__ = 'mark'

import requests, json, random
from testmadmike.logger import Logger
import hashlib

class Tester():
    def __init__(self, host='http://localhost:8080'):
        self.host = host
        self.log = Logger()
        self.log.info('Starting tests...')
        self.log.info('Getting users...')
        req = requests.get(url='{}/v2/users'.format(self.host))
        if req.status_code == requests.codes.ok:
            self.log.info('Trying to get JSON object with users...')
            try:
                self.users = req.json()['data']
                self.log.success('JSON object with users got, users count {}'.format(len(self.users)))
            except ValueError as e:
                self.log.error('Getting JSON object failed with error {}'.format(e))

    def createDemo(self):
        ## Creating users
        for i in range(0, 10000):
            string = hashlib.sha224()
            string.update('{}'.format(random.random()))
            first = 'first{}'.format(string.hexdigest()[0:10])
            string.update('{}'.format(random.random()))
            last = 'last{}'.format(string.hexdigest()[0:10])
            email = 'email{}'.format(string.hexdigest()[0:10])
            req = requests.post(url='{}{}'.format(self.host, '/v2/user/register'), data={
                'first': first,
                'last': last,
                'tel': '{}'.format(random.randint(0000000000, 9999999999)),
                'email': '{}@localhost.email'.format(email),
                'pass': 'password',
                'type': 'customer',
            })
            if req.status_code == requests.codes.ok:
                data = req.json()
                self.log.success('Adding user {} success, message {}'.format(email, data['message']))
            else:
                try:
                    data = req.json()
                    self.log.error('Adding user {} failed, error {}'.format(email, data['message']))
                except ValueError as e:
                    self.log.error('Adding user {} failed, status {}'.format(email, e))

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
            self.log.info('{}, function: {}'.format(link, path['func']))
            if func == 'checkStatus':
                data = requests.get(url=link)
                if data.status_code == path['response']:
                    if data.status_code == requests.codes.ok:
                        self.log.info('{} available, status is {} - correct'.format(link, data.status_code))
                        try:
                            self.log.success('{}, message: {}'.format(link, data.json()['message']))
                        except ValueError as e:
                            self.log.error('{}, error: {}'.format(link, e))
                    else:
                        self.log.info('{} available, status is {} - correct'.format(link, data.status_code))
                else:
                    self.log.error('Url {} unavailable, status is {} - incorrect'.format(link, data.status_code))
                    #TODO uncomment next line before start
                    # exit()
            elif func == 'testUser':
                pass
            self.log.info(param)
