#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.1'
__author__ = 'Lovvvve'
__email__ = 'lovvvve+github@gmail.com'

import scrapy


class Proxy_cn_proxy(scrapy.Spider):
    name = "Proxy_cn_proxy"
    allowed_domains = ["cn-proxy.com"]
    start_urls = ['http://cn-proxy.com/']

    def parse(self, response):
        for sel in response.xpath('//table[@class="sortable"]//tbody//tr'):
            ip = sel.xpath('td//text()').extract()[0]
            port = sel.xpath('td//text()').extract()[1]
            # print ip, port
            with open("test.txt", 'aw') as f:
                f.write(ip+':'+port+'\n')