# -*- coding: utf-8 -*-
import scrapy


class ScrapyMinervaSpider(scrapy.Spider):
    name = 'scrapy_minerva'
    allowed_domains = ['horizon.mcgill.ca']
    start_urls = ['http://horizon.mcgill.ca/']

    def parse(self, response):
        pass
