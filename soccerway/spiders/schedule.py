# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from soccerway.items import MatchInfo
from urllib.parse import urlencode, urlparse, parse_qs
from datetime import datetime, timezone

class ScheduleSpider(Spider):
    name = "schedule"
    #allowed_domains = ["http://www.soccerway.mobi/"]
    start_urls = ['http://www.soccerway.mobi/?']

    def start_requests(self):
        start_url = 'http://www.soccerway.mobi/'
        request = Request(url=start_url, callback=self.parse_index)
        request.meta['proxy'] = 'http://127.0.0.1:8118'
        yield request

    def parse_index(self, response):
        start_url = 'http://www.soccerway.mobi/'
        links = response.xpath('//th[@class="competition-link"]//a/@href').extract()
        for l in links:
            #self.log('URL: {}'.format(start_url+l))
            request = Request(url=start_url+l, callback=self.parse_competition)
            request.meta['proxy'] = 'http://127.0.0.1:8118'
            yield request

    def parse_competition(self, response):
        start_url = 'http://www.soccerway.mobi/'
        links = response.xpath('//td[@class="score-time status"]//a/@href').extract()
        for l in links:
            #self.log('URL: {}'.format(start_url+l))
            request = Request(url=start_url+l, callback=self.parse_match)
            request.meta['proxy'] = 'http://127.0.0.1:8118'
            yield request

    def parse_match(self, response):
        item = MatchInfo()
        item['id'] = parse_qs(response.xpath('//div[@class="clearfix subnav level-1"]//li//a/@href').extract()[3])['id'][0]
        item['area'] = response.xpath('//div[@class="clearfix subnav level-1"]//li//a/text()').extract()[1]
        item['competition'] = response.xpath('//div[@class="clearfix subnav level-1"]//li//a/text()').extract()[2]
        item['home_team'] = response.xpath('//div[@class="container left"]//a/text()').extract_first()
        item['away_team'] = response.xpath('//div[@class="container right"]//a/text()').extract_first()
        item['ht_last5'] = ''.join(response.xpath('//div[@class="container left"]//a/text()').extract()[1:6])
        item['at_last5'] = ''.join(response.xpath('//div[@class="container right"]//a/text()').extract()[1:6])
        item['datetime'] = datetime.fromtimestamp(int(response.xpath('//div[@class="details clearfix"]/dl/dt[.="Date"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Date"]//span/@data-value').extract_first()), timezone.utc).isoformat(' ')
        #item['competition'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Competition"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Competition"]/a/text()').extract_first()
        item['game_week'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Game week"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Game week"]/text()').extract_first()
        item['kick_off'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Kick-off"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Kick-off"]//span/text()').extract_first()
        item['venue'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Venue"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Venue"]//a/text()').extract_first()
        item['updated'] = datetime.utcnow().isoformat(' ')
        yield item
        return item
        #self.log('URL: {}'.format(response.url))

