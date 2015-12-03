# -*- coding: utf-8 -*-
import scrapy, json, sys
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from testmadmike.logger import Logger

class MainspiderSpider(CrawlSpider):
    name = "mainspider"
    host = 'http://localhost:8080'

    allowed_domains = ()
    start_urls = (
        host,
    )
    handle_httpstatus_list = [404, 405, 500]
    paths = json.load(open('paths.json', 'r'))
    log = Logger()

    def parse(self, response):
        assert response.status == 404
        self.log.info('Url {} available, status is {} - correct'.format(response.url, response.status))
        for path in self.paths:
            if not path['skip'] and not path['func']:
                yield Request(url='{}{}'.format(self.host, path['path']), meta={
                    'path': path
                }, callback=self.checkStatus)


    def checkStatus(self, response):
        path = response.meta['path']
        assert response.status == path['response']
        self.log.info('Url {} available, status is {} - correct'.format(response.url, response.status))

    def parse_(self, response):
        if response.status == 200:
            self.log.info('Url {} available'.format(response.url))
            try:
                data = json.loads(response.body)
                if 'status' in data and data['status'] == 'success':
                    self.log.success(data['message'])
                else:
                    self.log.error(data['message'])
            except ValueError as e:
                self.log.error(e)
        else:
            self.log.error('Url {} not available'.format(response.url))
            self.log.error('Response status {}'.format(response.status))