import urllib2, json
from testmadmike.logger import Logger

class Tester():
    def __init__(self, host='http://localhost:8080'):
        self.host = host
        self.log = Logger()
        pass

    def startTest(self, paths):
        for path in paths:
            if path['skip'] and 'subs' in path or 'subs' in path:
                for path_ in path['subs']['items']:
                    if path_['func'] is None:
                        path_['func'] = path['subs']['func']
                    self.test(path_, path)

    def test(self, path, parent):
        path['path'] = parent['path'] + path['path']
        func = None

        if path['func'] is None and parent['subs']['func'] is not None:
            func = parent['subs']['func']
        elif path['func'] is not None:
            func = path['func']

        if path['skip'] and 'subs' in path or 'subs' in path:
            for path_ in path['subs']['items']:
                if path_['func'] is None:
                    path_['func'] = path['subs']['func']
                if 'subs' in path_ and path_['subs']['func'] is None:
                    path_['subs']['func'] = path['subs']['func']
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
                            self.log.info('{}, message: {}\n'.format(link, object['message']))
                        except ValueError as e:
                            self.log.error('{}, error: {}\n'.format(link, e))
                except urllib2.HTTPError as data:
                    if data.code == path['response']:
                        self.log.info('Url {} unavailable, status is {} - correct\n'.format(link, data.code))
                    else:
                        self.log.error('Url {} unavailable, status is {} - incorrect\n'.format(link, data.code))
                        # exit()
            else:
                self.log.info('{} has not function\n'.format(link))
