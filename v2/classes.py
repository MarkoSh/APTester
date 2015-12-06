# -*- coding: utf-8 -*-

__author__ = 'mark'

import requests, json, random
from logger import Logger, Profiler
import hashlib
from requests.exceptions import ConnectionError


class Tester():
    def __init__(self, host='http://localhost:8080'):
        self.host = host
        self.log = Logger()
        try:
            self.log.info('Getting users...')
            req = requests.get(url='{}/v2/users'.format(self.host))
            self.log.success('Users received\n')
            if req.status_code == requests.codes.ok:
                self.log.info('Trying to get JSON object with users...')
                try:
                    self.users = req.json()['data']
                    self.log.success('JSON object with users received, users count {}\n'.format(len(self.users)))
                except ValueError as e:
                    self.log.error('Getting JSON object failed with error {}'.format(e))
                    exit()
        except ConnectionError as e:
            self.log.error('Request failed with error {}'.format(e))
            exit()

    def createDemo(self):
        ## Creating users
        for i in range(0, 100):
            with Profiler() as p:
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
                            # exit()
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
        if 'subs' in path:
            path['subs']['func'] = func
            for path_ in path['subs']['items']:
                self.test(path_, path)
        if not path['skip']:
            link = '{}{}'.format(self.host, path['path'])
            self.log.info('{}, function: {}'.format(link, path['func']))
            with Profiler() as p:
                if func == 'checkStatus':
                    self.checkStatus(path=path)
                if func == 'testUser':
                    self.testUser(path=path)
                if func == 'authUser':
                    self.authUser(path=path)
                if func == 'testLocation':
                    self.testLocation(path=path)
                if func == 'getStats':
                    self.getStats(path=path)
                if func == 'sendMessage':
                    self.sendMessage(path=path)
                if func == 'ziptoloc':
                    self.ziptoloc(path=path)

    def ziptoloc(self, path):
        link = '{}{}'.format(self.host, path['path'])
        self.log.info('Requesting convertation zip to location...')
        for i in range(0, 20):
            with Profiler() as p:
                try:
                    zipcode = random.randint(10000, 99999)
                    link_ = '{}?zip_code={}'.format(link, zipcode)
                    self.log.info('ZipCode is: {}'.format(zipcode))
                    req = requests.get(url=link_)
                    try:
                        data = req.json()
                        if data['status'] == 'success':
                            if data['data']['city'] is not None:
                                self.log.success('Zip to location success, location is {}'.format(data['data']))
                            else:
                                self.log.success('Zip to location success, but zip is not exists')
                        else:
                            self.log.error('Zip to location failed with message {}'.format(data['message']))
                    except ValueError as e:
                        self.log.error('Getting JSON object failed with error {}'.format(e))
                        exit()
                except ConnectionError as e:
                    self.log.error('Request failed with error {}'.format(e))
                    exit()

    def checkStatus(self, path):
        link = '{}{}'.format(self.host, path['path'])
        data = requests.get(url=link)
        if data.status_code == path['response']:
            if data.status_code == requests.codes.ok:
                self.log.info('{} available, status is {} - correct'.format(link, data.status_code))
                try:
                    self.log.success('{}, message: {}'.format(link, data.json()['message']))
                except ValueError as e:
                    self.log.error('{}, error: {}'.format(link, e))
                    exit()
            else:
                self.log.info('{} available, status is {} - correct'.format(link, data.status_code))
        else:
            self.log.error('Url {} unavailable, status is {} - incorrect'.format(link, data.status_code))
            exit()

    def sendMessage(self, path):
        random.shuffle(self.users)
        ### Коректная отправка с исключение самого отправителя из списка
        self.log.info('Correct receivers sending...')
        for i in range(0, 10):
            user_from = self.users[i]['email']
            users_to = list()
            postData = {
                    'sent_from': user_from,
                }
            self.users.pop(i)
            link = '{}{}'.format(self.host, path['path'])
            for c in range(0, random.randrange(1, 10)):
                user_to = self.users[c]
                users_to.append(user_to['email'])
            random.shuffle(users_to)
            users_to = ', '.join(users_to)
            postData['send_to'] = users_to
            self.log.info('Sender {}'.format(user_from))
            self.log.info('Receivers {}'.format(users_to))
        self.log.separator()
        ### Ошибочная отправка с включением самого отправителя в список
        self.log.info('Incorrect receivers sending...')
        for i in range(0, 10):
            user_from = self.users[i]['email']
            users_to = list()
            postData = {
                    'sent_from': user_from,
                }
            link = '{}{}'.format(self.host, path['path'])
            for c in range(0, random.randrange(1, 10)):
                user_to = self.users[c]
                users_to.append(user_to['email'])
            random.shuffle(users_to)
            users_to = ', '.join(users_to)
            postData['send_to'] = users_to
            self.log.info('Sender {}'.format(user_from))
            self.log.info('Receivers {}'.format(users_to))

    def getStats(self, path):
        link = '{}{}'.format(self.host, path['path'])
        try:
            self.log.info('Get stats...')
            req = requests.get(url=link)
            try:
                data = req.json()
                if data['status'] == 'success':
                    self.log.success('Stats received')
                    self.log.info('#TODO сделать обработку статы, пока что стата пустая, так что обработать нечего')
                    #TODO сделать обработку статы, пока что стата пустая, так что обработать нечего
                else:
                    self.log.error('Getting stats failed with message {}'.format(data['message']))
                    exit()
            except ValueError as e:
                self.log.error('Getting JSON object failed with error {}'.format(e))
                exit()
        except ConnectionError as e:
            self.log.error('Request failed with error {}'.format(e))
            exit()

    def testLocation(self, path):
        link = '{}{}'.format(self.host, path['path'])
        with open('cities.txt', 'r') as fp:
            cities = [city.strip() for city in fp.readlines()]
            random.shuffle(cities)
            cities = cities[0:10]
            for city in cities:
                with Profiler() as p:
                    try:
                        self.log.info('Search places for {}...'.format(city))
                        req = requests.get(url='{}?q={}'.format(link, city))
                        try:
                            data = req.json()
                            if data['status'] == 'success':
                                self.log.success('Location received, places is:')
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
            with Profiler() as p:
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
                    else:
                        try:
                            data = req.json()
                            self.log.error('User {} login failed, message: {}'.format(user['email'], data['message']))
                        except ValueError as e:
                            self.log.error('Getting JSON object failed with error {}'.format(e))
                        exit()
                except ConnectionError as e:
                    self.log.error('Request failed with error {}'.format(e))
                    exit()

    def testUser(self, path):
        random.shuffle(self.users)
        for i in range(0, 10):
            with Profiler() as p:
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
