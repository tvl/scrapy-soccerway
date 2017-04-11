# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from soccerway.items import Competition
from urllib.parse import urlencode, urlparse, parse_qs

class CompetitionsSpider(Spider):
    name = "areas"
    allowed_domains = ["http://www.soccerway.mobi"]
    start_urls = 	['http://www.soccerway.mobi/?']
    params = {
        "sport": "soccer",
        "page": "leagues",
        "view" : "by_area",
        "area_id" : "212",
        "localization_id": "www"
    }
    def start_requests(self):
        start_url = 'http://www.soccerway.mobi/?sport=soccer&page=leagues&view=by_area&area_id={}&localization_id=www'
        for i in range(1,213): # 1 - 213
            request = Request(url=start_url.format(str(i)), callback=self.parse)
            request.meta['proxy'] = 'http://127.0.0.1:8118'
            yield request

    def parse(self, response):
        items = []
        item = Competition()
        area_id = parse_qs(response.xpath('//div[@class="clearfix subnav level-1"]//li//a[2]/@href').extract_first())['area_id'][0]
        area_name = response.xpath('//div[@class="clearfix subnav level-1"]//li//a[2]/text()').extract_first()
        links = response.xpath('//div[@class="block_competitions_list real-content clearfix "]//li/a')
        for l in links:
            item['id'] = parse_qs(l.xpath('./@href').extract_first())['id'][0]
            item['name'] = l.xpath('./text()').extract_first()
            item['area_id'] = area_id
            item['area_name'] = area_name
            item['updated'] = datetime.utcnow().isoformat()
            yield item

        items.add(item)
        return items
        #self.log('URL: {}'.format(response.url))


