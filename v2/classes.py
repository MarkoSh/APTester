# -*- coding: utf-8 -*-

__author__ = 'mark'

import requests, json, random
from logger import Logger
import hashlib
from requests.exceptions import ConnectionError


class Tester():
    def __init__(self, host='http://localhost:8080'):
        self.host = host
        self.log = Logger()
        self.log.info('Starting tests...')
        try:
            self.log.info('Getting users...')
            req = requests.get(url='{}/v2/users'.format(self.host))
            self.log.success('Users got\n')
            if req.status_code == requests.codes.ok:
                self.log.info('Trying to get JSON object with users...')
                try:
                    self.users = req.json()['data']
                    self.log.success('JSON object with users got, users count {}\n'.format(len(self.users)))
                except ValueError as e:
                    self.log.error('Getting JSON object failed with error {}'.format(e))
                    exit()
        except ConnectionError as e:
            self.log.error('Request failed with error {}'.format(e))
            exit()

    def createDemo(self):
        ## Creating users
        for i in range(0, 10000):
            string = hashlib.sha224()
            string.update('{}'.format(random.random()))
            first = 'first{}'.format(string.hexdigest()[0:10])
            string.update('{}'.format(random.random()))
            last = 'last{}'.format(string.hexdigest()[0:10])
            tel = '{}'.format(random.randint(0000000000, 9999999999))
            email = 'email{}@localhost.email'.format(string.hexdigest()[0:10])

            postData = {
                    'first': first,
                    'last': last,
                    'tel': tel,
                    'email': email,
                    'pass': 'password',
                    'type': 'customer',
                }

            try:
                req = requests.post(url='{}{}'.format(self.host, '/v2/user/register'), data=postData)
                if req.status_code == requests.codes.ok:
                    try:
                        data = req.json()
                        user = data['data']
                        if first == user['first_name'] and \
                                        last == user['last_name'] and \
                                        tel == str(user['phone_number']) and \
                                        email == user['email']:
                            self.log.success('Adding user {} success, message {}'.format(email, data['message']))
                        else:
                            self.log.error('Adding user failed')
                            self.log.error('Posted data: {}'.format(postData))
                            self.log.error('Received data: {}'.format(user))
                            exit()
                    except ValueError as e:
                        self.log.error('Getting JSON object failed with error {}'.format(e))
                        exit()
                else:
                    try:
                        data = req.json()
                        self.log.error('Adding user {} failed, message {}'.format(email, data['message']))
                        exit()
                    except ValueError as e:
                        self.log.error('Getting JSON object failed with error {}'.format(e))
                        exit()
            except ConnectionError as e:
                self.log.error('Request failed with error {}'.format(e))
                exit()

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
        if path['func'] is None and parent['subs']['func'] is not None:
            path['func'] = parent['subs']['func']

        if path['param'] is None and parent['param'] is not None:
            path['param'] = parent['param']

        elif path['param'] is not None and parent['param'] is not None:
            path['param'] = list(set(path['param'] + parent['param']))

        func = path['func']
        param = path['param']

        if 'subs' in path:
            path['subs']['func'] = func
            for path_ in path['subs']['items']:
                self.test(path_, path)

        if not path['skip']:
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
                    exit()
            elif func == 'testUser':
                self.testUser(path=path)
                # pass
            elif func == 'authUser':
                self.authUser(path=path)
            elif func == 'testLocation':
                self.testLocation(path=path)

    def testLocation(self, path):
        link = '{}{}'.format(self.host, path['path'])
        cities = [city.strip() for city in open('cities.txt', 'r').readlines()]
        random.shuffle(cities)
        cities = cities[0:10]
        for city in cities:
            try:
                self.log.info('Search places for {}...'.format(city))
                req = requests.get(url='{}?q={}'.format(link, city))
                try:
                    data = req.json()
                    if data['status'] == 'success':
                        self.log.success('Location got, places is:')
                        for place in data['data']:
                            self.log.success('{}'.format(place['place']))
                    else:
                        self.log.error('Getting location failed with message {}'.format(data['message']))
                        exit()
                except ValueError as e:
                        self.log.error('Getting JSON object failed with error {}'.format(e))
                        exit()
            except ConnectionError as e:
                    self.log.error('Request failed with error {}'.format(e))
                    exit()

    def authUser(self, path):
        random.shuffle(self.users)
        for i in range(0, 10):
            user = self.users[i]
            link = '{}{}'.format(self.host, path['path'])
            try:
                self.log.info('Authenticate user {}, {}...'.format(user['email'], link))
                req = requests.post(url=link, data={
                    'user_id': user['email'],
                    'password': 'password'
                })
                if req.status_code == path['response']:
                    self.log.info('Trying to get JSON object for user...')
                    try:
                        data = req.json()
                        user_ = data['data']
                        if user['email'] == user['email']:
                            self.log.success('Received {}:{} equals expected {}:{}'.format('email', user_['email'], 'email', user['email']))
                        else:
                            self.log.error('{}, message: {}'.format(link, data['message']))
                            exit()
                    except ValueError as e:
                        self.log.error('Getting JSON object failed with error {}'.format(e))
                        exit()
            except ConnectionError as e:
                self.log.error('Request failed with error {}'.format(e))
                exit()

    def testUser(self, path):
        random.shuffle(self.users)
        for i in range(0, 10):
            user = self.users[i]
            link = '{}{}'.format(self.host, path['path'].replace('<user_id:\\d+>', str(user['key']['id'])))
            try:
                self.log.info('Getting user {}, {}...'.format(user['email'], link))
                req = requests.get(url=link)
                if req.status_code == path['response']:
                    self.log.info('Trying to get JSON object for user...')
                    try:
                        data = req.json()
                        user_ = data['data']
                        for key, val in user_.iteritems():
                            if key in user:
                                if val == user[key]:
                                    self.log.success('Received {}:{} equals expected {}:{}'.format(key, val, key, user[key]))
                                else:
                                    self.log.error('Received {}:{} not equals expected {}:{}'.format(key, val, key, user[key]))
                                    exit()
                            else:
                                self.log.error('Received key {} not found in dict'.format(key))
                                exit()
                    except ValueError as e:
                        self.log.error('Getting JSON object failed with error {}'.format(e))
                        exit()
                else:
                    self.log.error('{}, message: {}'.format(link, data['message']))
                    exit()
            except ConnectionError as e:
                self.log.error('Request failed with error {}'.format(e))
                exit()
