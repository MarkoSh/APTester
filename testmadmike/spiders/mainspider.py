# -*- coding: utf-8 -*-
import scrapy, json, sys
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from testmadmike.logger import Logger
from scrapy import optional_features
optional_features.remove('boto')

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
        self.startTesting()

    def startTesting(self):
        if self.paths[0]['skip']:
             for path in self.paths[0]['subs']['items']:
                 path['path'] = self.paths[0]['path'] + path['path']
                 self.testItem(path, self.paths[0]['subs']['func'])

    def testItem(self, path, func):
        pass