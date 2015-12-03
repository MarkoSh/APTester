import urllib2, json
from testmadmike.logger import Logger

class Tester():
    def __init__(self, host='http://localhost:8080'):
        self.host = host
        self.log = Logger()
        pass

    def startTest(self, paths):
        for path in paths:
            if path['skip'] and 'subs' in path:
                for path_ in path['subs']['items']:
                    path_['func'] = path['subs']['func']
                    self.test(path_, path)

    def test(self, path, parent):
        if path['skip'] and 'subs' in path:
            path['path'] = parent['path'] + path['path']
            for path_ in path['subs']['items']:
                path_['func'] = path['subs']['func']
                self.test(path_, path)
        else:
            link = '{}{}{}'.format(self.host, parent['path'], path['path'])
            try:
                data = urllib2.urlopen(url=link)
                if data.code == path['response']:
                    self.log.info('{} available, status is {} - correct'.format(link, data.code))
                    if path['func'] == 'checkStatus':
                        self.log.info('{}, function: {}'.format(link, path['func']))
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
