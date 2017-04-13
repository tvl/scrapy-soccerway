# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from soccerway.items import Venue
from urllib.parse import urlencode, urlparse, parse_qs
from datetime import datetime, timezone
from soccerway.competitions import competitions_id_list

class TeamsSpider(Spider):
    name = "venues"
    allowed_domains = ["http://www.soccerway.mobi"]
    start_urls = ['http://www.soccerway.mobi/?']
    params = {
        "sport": "soccer",
        "page": "match",
        "id" : "2255155",
        "localization_id": "www"
    }
    def start_requests(self):
        start_url = 'http://int.soccerway.com/venues/england/venue/v{}/'
        for i in range(6, 27618): # 27617 on 12.04.2017
            request = Request(url=start_url.format(str(i)), callback=self.parse)
            request.meta['proxy'] = 'http://127.0.0.1:8118'
            yield request

    def parse(self, response):
        item = Venue()
        item['id'] = response.url.split('/')[-2][1:]
        if not int(item['id']):
            self.log('Skip URL: {}'.format(response.url))
            return None
        item['name'] = response.xpath('//h1/text()').extract_first()
        item['address'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Address:"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Address:"]/text()').extract_first()
        item['zip'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Zip code:"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Zip code:"]/text()').extract_first()
        item['opened'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Opened:"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Opened:"]/text()').extract_first()
        item['capacity'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Capacity:"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Capacity:"]/text()').extract_first()
        item['surface'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Surface:"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Surface:"]/text()').extract_first()
        item['lat'] = response.xpath('//script[contains(., "setMarker")]').extract_first().split('\n')[10][:-1].strip()
        item['lon'] = response.xpath('//script[contains(., "setMarker")]').extract_first().split('\n')[11][:-1].strip()
        #item['url'] = response.url
        item['updated'] = datetime.utcnow().isoformat(' ')
        yield item
        return item
        #self.log('URL: {}'.format(response.url))

