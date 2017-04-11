# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from soccerway.items import Area
from urllib.parse import urlencode, urlparse, parse_qs
from datetime import datetime

class AreasSpider(Spider):
    name = "areas"
    allowed_domains = ["http://www.soccerway.mobi"]
    start_urls = ['http://www.soccerway.mobi/?']
    params = {
        "sport": "soccer",
        "page": "leagues",
        "view" : "by_area",
        "area_id" : "212",
        "localization_id": "www"
    }
    def start_requests(self):
        for i in range(1,213): # 1 - 212
            self.params['area_id'] = str(i)
            request = Request(url=self.start_urls[0]+urlencode(self.params), callback=self.parse)
            request.meta['proxy'] = 'http://127.0.0.1:8118'
            yield request

    def parse(self, response):
        l = ItemLoader(item=Area(), response=response)
        l.add_value('id', parse_qs(response.xpath('//div[@class="clearfix subnav level-1"]//li//a[2]/@href').extract()[0])['area_id'][0])
        l.add_xpath('name', '//div[@class="clearfix subnav level-1"]//li//a[2]/text()')
        l.add_value('updated', datetime.utcnow().isoformat()) # you can also use literal values
        return l.load_item()
        #self.log('URL: {}'.format(response.url))

    """
    def parse(self, response):
        venue = Venue()
        venue['country'], venue['city'], venue['name'] = response.css('title::text')[0].extract().split(',')
        res = response.xpath('//td//b/text()')
        if len(res) > 0:
            venue['opened'] = res[0].extract()
        res = response.xpath('//td//b/text()')
        if len(res) > 1:
            venue['capacity'] = res[1].extract()
        venue['lat'], venue['lng'] = response.xpath('//script/text()')[1].re(r'\((.*)\)')[1].split(',')
        return venue
    """

