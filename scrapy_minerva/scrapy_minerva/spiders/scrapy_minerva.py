# -*- coding: utf-8 -*-
import scrapy


class ScrapyMinervaSpider(scrapy.Spider):
    name = 'scrapy_minerva'
    allowed_domains = ['cs.mcgill.ca']
    start_urls = ['https://www.cs.mcgill.ca/~jeromew/comp250.html']

    def parse(self, response):

        print(response.text)
