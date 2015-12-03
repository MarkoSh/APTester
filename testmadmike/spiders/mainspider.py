# -*- coding: utf-8 -*-
import scrapy, json, colors, sys
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from datetime import datetime

class MainspiderSpider(CrawlSpider):
    name = "mainspider"
    host = 'http://localhost:8080'

    allowed_domains = ()
    start_urls = (
        host,
    )
    handle_httpstatus_list = [404, 405, 500]
    paths = json.load(open('paths.json', 'r'))


    def parse(self, response):
        assert response.status == 404
        log = logger()
        log.info('Url {} available, status is {} - correct'.format(response.url, response.status))
        for path in self.paths:
            if path['func'] == 'checkStatus':
                if not path['skip']:
                    yield Request(url='{}{}'.format(self.host, path['path']), meta={
                        'path': path
                    }, callback=self.checkStatus)
                else:
                    for path_ in path['subs']:
                        path_['path'] = path['path'] + path_['path']
                        yield Request(url='{}{}'.format(self.host, path_['path']), meta={
                        'path': path_
                    }, callback=self.checkStatus)

    def checkStatus(self, response):
        # assert response.status == 200
        path = response.meta['path']
        pass


    def parse_(self, response):
        log = logger()
        if response.status == 200:
            log.info('Url {} available'.format(response.url))
            try:
                data = json.loads(response.body)
                if 'status' in data and data['status'] == 'success':
                    log.success(data['message'])
                else:
                    log.error(data['message'])
            except ValueError as e:
                log.error(e)
        else:
            log.error('Url {} not available'.format(response.url))
            log.error('Response status {}'.format(response.status))

class logger():
    timeformat = '%Y-%m-%d %H:%M:%S'
    def info(self, msg='Information'):
        line = 'INFORMATION: {} - {}'.format(datetime.now().strftime(self.timeformat), msg)
        print(colors.yellow(line))
        self.write('log', line)

    def success(self, msg='Success'):
        line = 'SUCCESS: {} - {}'.format(datetime.now().strftime(self.timeformat), msg)
        print(colors.green(line))
        self.write('log', line)

    def error(self, msg='Error'):
        line = 'ERROR: {} - {}'.format(datetime.now().strftime(self.timeformat), msg)
        print >> sys.stderr, colors.red(line)
        self.write('error', line)
        self.write('log', line)

    def write(self, type, line):
        open('{}.log'.format(type), 'a').write('{}\n'.format(line))