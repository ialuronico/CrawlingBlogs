# -*- coding: utf-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import BaseSpider
import html2text
import scrapy
import lxml.html
import re
import unicodedata

class BlogSpider(BaseSpider):
    name = "blog_spider"
    start_urls = []
    base_url = "http://www.nomadicmatt.com/page/"
    for i in range(1,100):
        url = base_url + str(i) + "/?s"
        start_urls.append(url)
    
    
    def parse(self, response):
        i = 0
        for href in response.css('.entry-title a::attr(href)'):
            url = href.extract()            
            yield scrapy.Request(url, callback=self.parse_page)
                
    def parse_page(self, response):
        text = ""
        for par in response.css('.entry-content p'):
            this_text = lxml.html.fromstring(par.extract())
            this_text = this_text.text_content().strip()
            this_text = unicodedata.normalize('NFKD', u"" + this_text)
            this_text = this_text.encode('ascii', errors='backslashreplace')
            # substitue apostrope
            this_text = this_text.replace("\u2019", "'")
            this_text = this_text.replace('\\xa0', ' ')
            # add it up
            text = text + " " + this_text
            
        yield {
            'Text': text
        }