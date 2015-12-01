# -*- coding: utf-8 -*-
import scrapy, json
from scrapy.spiders import CrawlSpider
from scrapy.http import Request


class MainspiderSpider(CrawlSpider):
    name = "mainspider"
    allowed_domains = ["appointmentpro.net"]
    start_urls = (
        'http://appointmentpro.net/',
    )

    def parse(self, response):

        pass
