# -*- coding: utf-8 -*-
import scrapy, json
from scrapy.spiders import CrawlSpider
from scrapy.http import Request


class MainspiderSpider(CrawlSpider):
    name = "mainspider"
    allowed_domains = ["appointmentpro.com"]
    start_urls = (
        'http://appointmentpro.com/',
    )

    def parse(self, response):
        pass
