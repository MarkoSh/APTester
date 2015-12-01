# -*- coding: utf-8 -*-
import scrapy, json, colors, sys
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from datetime import datetime

class MainspiderSpider(CrawlSpider):
    name = "mainspider"
    allowed_domains = ["http://api-dot-bizzbook-app.appspot.com/"]
    start_urls = (
        'http://api-dot-bizzbook-app.appspot.com/v2/dashboard/stats',
    )
    handle_httpstatus_list = [404, 405, 500]
    paths = [path.strip() for path in open('paths.txt', 'r').readlines() if 'cron' not in path]

    def parse(self, response):
        log = logger()
        log.info('Url {} available'.format(response.url))
        try:
            data = json.loads(response.body)
            if 'status' in data and data['status'] == 'success':
                log.success(data['message'])
            else:
                log.error(data['message'])
            for path in self.paths:
                yield Request(url='http://api-dot-bizzbook-app.appspot.com{}'.format(path), callback=self.parse_, dont_filter=True)
        except ValueError as e:
            log.error(e)

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

    def write(self, type, line):
        open('{}.log'.format(type), 'a').write('{}\n'.format(line))