#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.1'
__author__ = 'Lovvvve'
__email__ = 'lovvvve+github@gmail.com'

import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector


class Baidutieba(CrawlSpider):
    name = 'Baidutieba'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['http://tieba.baidu.com/f/good?kw=武炼巅峰&ie=utf-8&cid=1']

    # rules = (
    # Rule(LinkExtractor(allow=('&pn=\d{1,}'))),
    # Rule(LinkExtractor(allow=('p/'))),
    # )
    # print '----------'
    def parse(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        # print "====================="
        # print "request url: " + response.url
        for sel in response.xpath('//a//@href').extract():
            if re.search('/p/\d+', sel):
                # print
                if re.search('http', sel):
                    yield scrapy.Request(sel, self.parse_post)
                    # post_url.append(sel)
                else:
                    posturl = 'http://tieba.baidu.com' + sel
                    yield scrapy.Request(posturl, self.parse_post)
        next_url = HtmlXPathSelector(response).select('//a[@class="next"]//@href').extract()
        if not len(next_url) == 0:
            next_url = "http://tieba.baidu.com" + next_url[0]
            # print next_url
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_post(self, response):
        if len(response.xpath('//h1[@style="width: 416px"]//text()').extract()) == 0:
            print "~~~~~~~~~~~~~!!!!!!!!!!!!!!!~~~~~~~~~~~~~"
            print response.url
        else:
            tittle = response.xpath('//h1[@style="width: 416px"]//text()').extract()[0]
            tittle = re.sub(" ", "_", tittle)
            content = '\n'.join(
                response.xpath('//div[@class="d_post_content j_d_post_content "]')[0].xpath('./text()').extract()
                )
            # print content
            with open("/opt/a/"+tittle+".txt", 'aw') as f:
                f.write(content.encode('utf-8'))