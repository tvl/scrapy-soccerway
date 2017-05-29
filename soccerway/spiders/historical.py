# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from soccerway.items import HistoricalData
from urllib.parse import urlencode, urlparse, parse_qs
from datetime import datetime, timezone

class HistoricalSpider(Spider):
    name = "historical"
    #allowed_domains = ["http://www.soccerway.mobi/"]
    start_urls = ['http://www.soccerway.mobi/?']

    def start_requests(self):
        start_url = 'http://www.soccerway.mobi/?sport=soccer&page=match&id={}&_teamtype=default&localization_id=www'
        for i in range(920000, 930000):
            request = Request(url=start_url.format(str(i)), callback=self.parse)
            request.meta['proxy'] = 'http://127.0.0.1:8118'
            yield request

    def parse(self, response):
        item = HistoricalData()
        links = response.xpath('//div[@class="clearfix subnav level-1"]//li//a/@href').extract()
        if len(links) != 4:
            self.log('SKIP URL: {}'.format(response.url))
            return None
        item['id'] = parse_qs(response.xpath('//div[@class="clearfix subnav level-1"]//li//a/@href').extract()[3])['id'][0]
        item['area_id'] = parse_qs(response.xpath('//div[@class="clearfix subnav level-1"]//a[1]/@href').extract()[1])['area_id'][0]
        item['competition_id'] = parse_qs(response.xpath('//div[@class="clearfix subnav level-1"]//li//a[2]/@href').extract_first())['id'][0]
        item['area'] = response.xpath('//div[@class="clearfix subnav level-1"]//li//a/text()').extract()[1]
        item['competition'] = response.xpath('//div[@class="clearfix subnav level-1"]//li//a/text()').extract()[2]
        item['home_team'] = response.xpath('//div[@class="container left"]//a/text()').extract_first()
        item['away_team'] = response.xpath('//div[@class="container right"]//a/text()').extract_first()
        #item['ht_last5'] = ''.join(response.xpath('//div[@class="container left"]//a/text()').extract()[1:6])
        #item['at_last5'] = ''.join(response.xpath('//div[@class="container right"]//a/text()').extract()[1:6])
        item['timestamp'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Date"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Date"]//span/@data-value').extract_first()
        item['datetime'] = datetime.fromtimestamp(int(item['timestamp']), timezone.utc).isoformat(' ')
        #item['competition'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Competition"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Competition"]/a/text()').extract_first()
        item['game_week'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Game week"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Game week"]/text()').extract_first()
        item['kick_off'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Kick-off"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Kick-off"]//span/text()').extract_first()
        item['hts'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Half-time"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Half-time"]/text()').extract_first()
        item['fts'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Full-time"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Full-time"]/text()').extract_first()
        item['ets'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Extra-time"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Extra-time"]/text()').extract_first()
        item['pts'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Penalties"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Penalties"]/text()').extract_first()
        item['aggregate'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="On aggregate"]/following-sibling::dd[preceding-sibling::dt[1]/text()="On aggregate"]//a/text()').extract_first()
        line = response.xpath('//h3[@class="thick scoretime "]/text()').extract()
        if len(line) == 1:
            item['score'] = line[0].split('\n')[2].strip()
        if len(line) == 3:
            item['score'] = line[1].strip()
        item['venue'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Venue"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Venue"]//a/text()').extract_first()
        item['attendance'] = response.xpath('//div[@class="details clearfix"]/dl/dt[.="Attendance"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Attendance"]/text()').extract_first()
        item['updated'] = datetime.utcnow()
        yield item
        return item
        #self.log('URL: {}'.format(response.url))

