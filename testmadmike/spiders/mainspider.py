# -*- coding: utf-8 -*-
import scrapy, json, colors
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from datetime import datetime



class MainspiderSpider(CrawlSpider):
    name = "mainspider"
    allowed_domains = ["http://api-dot-bizzbook-app.appspot.com/"]
    start_urls = (
        'https://api-dot-bizzbook-app.appspot.com/v2/dashboard/stats',
    )
    # paths = [path.strip() for path in open('paths.txt', 'r').readlines()]

    def parse(self, response):
        log = logger()
        data = json.loads(response.body)
        if data['status'] == 'success':
            log.success(data['message'])
        else:
            log.error(data['message'])
        pass

class logger():
    def success(self, msg='Success'):
        print('{} - {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), colors.green(msg)))
    def error(self, msg='Error'):
        print('{} - {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), colors.red(msg)))