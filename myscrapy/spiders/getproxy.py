#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.1'
__author__ = 'Lovvvve'
__email__ = 'lovvvve+github@gmail.com'

import scrapy
import re
from myscrapy.items import ProxyIpItem


class Proxy_cn_proxy(scrapy.Spider):
    name = "Proxy_cn_proxy"
    allowed_domains = ["cn-proxy.com"]
    start_urls = ["http://cn-proxy.com"]

    def parse(self, response):
        for sel in response.xpath('//table[@class="sortable"]//tbody//tr'):
            ip = sel.xpath('td//text()').extract()[0]
            port = sel.xpath('td//text()').extract()[1]
            # print ip, port
            with open("test.txt", 'aw') as f:
                f.write(ip+':'+port+'\n')


class Proxy_www_proxy_com_ru(scrapy.Spider):
    name = "Proxy_www_proxy_com_ru"
    allowed_domains = ["www.proxy.com.ru"]
    start_urls = [
        'http://www.proxy.com.ru/list_1.html',
        'http://www.proxy.com.ru/list_2.html',
        'http://www.proxy.com.ru/list_3.html',
        'http://www.proxy.com.ru/list_4.html',
        'http://www.proxy.com.ru/list_5.html',
        'http://www.proxy.com.ru/list_6.html',
        ]

    def parse(self, response):
        for sel in response.xpath('//table[@width="100%"]')[3].xpath('tr')[1:]:
            iterm = ProxyIpItem()
            iterm['ip'] = sel.xpath('td//text()').extract()[1]
            iterm['port'] = sel.xpath('td//text()').extract()[2]
            yield iterm

