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

    def parse(self, response):
        """
        找到页面中所有章节的URL,然后给 parse_item 来抓取页面中的文章
        """
        # self.log('Hi, this is an item page! %s' % response.url)
        for sel in response.xpath('//a//@href').extract():
            """
            抓取所有/p/d+ 的 url 然后交给 parse_item 来抓取页面中的内容
            """
            if re.search('/p/\d+', sel):
                # print
                if re.search('http', sel):
                    yield scrapy.Request(sel, self.parse_item)
                    # post_url.append(sel)
                else:
                    posturl = 'http://tieba.baidu.com' + sel
                    yield scrapy.Request(posturl, self.parse_item)
        next_url = HtmlXPathSelector(response).select('//a[@class="next"]//@href').extract()

        if not len(next_url) == 0:  # 判断下一页是否存在
            """
            当前页面所有/p/d+ 的 url 抓取完成后找到下一页的URL, 并返回给自己继续处理页面中的/p/d+ URL
            """
            if next_url[0].startswith('/'):  # 判断URL是否完整,如果不完整就先补全URL
                next_url = "http://tieba.baidu.com" + next_url[0]
                yield scrapy.Request(next_url, callback=self.parse)
            else:
                yield scrapy.Request(next_url[0], callback=self.parse)

    def parse_item(self, response):
        """
        抓取页面中 tittle 为章节名称,一楼为章节内容
        """
        if len(response.xpath('//h1[@style="width: 416px"]//text()').extract()) == 0:
            #吧有问题的URL 保存到文件里面
            with open("/opt/a/error_url.txt", 'aw+') as f:
                f.write(response.url)
        else:  # 抓取页面中的文章
            tittle = response.xpath('//h1[@style="width: 416px"]//text()').extract()[0]
            tittle = re.sub(" ", "_", tittle)
            content = '\n'.join(
                response.xpath('//div[@class="d_post_content j_d_post_content "]')[0].xpath('./text()').extract()
            )
            with open("/opt/a/" + tittle + ".txt", 'aw') as f:
                f.write(content.encode('utf-8'))