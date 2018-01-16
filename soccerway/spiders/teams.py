# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.loader import ItemLoader
#from scrapy.stats import stats
from soccerway.items import Team
from urllib.parse import urlencode, urlparse, parse_qs
from datetime import datetime, timezone
from soccerway.competitions import competitions_id_list

nonexistent = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65]

class TeamsSpider(Spider):
    name = "teams"
    #allowed_domains = ["http://www.soccerway.mobi"]
    start_urls = ['http://www.soccerway.mobi/?']
    params = {
        "sport": "soccer",
        "page": "match",
        "id" : "2255155",
        "localization_id": "www"
    }

    def start_requests(self):
        start_url = 'http://www.soccerway.mobi/?sport=soccer&page=team&id={}&localization_id=www'
        self.crawler.stats.set_value('nonexistent',str(nonexistent))
        for i in range(1, 41980): # 38736 on 12.04.2017, 41962 on 12.01.2018
            if i in nonexistent:
                continue
            request = Request(url=start_url.format(str(i)), callback=self.parse)
            request.meta['proxy'] = 'http://127.0.0.1:8118'
            yield request
        #self.logger.info('Nonexistent teams: {}'.format(nonexistent))

    def parse(self, response):
        if response.xpath('//div[@class="clearfix subnav level-1"]//li//a[2]/@href').extract_first() is None:
            id = int(parse_qs(response.url)['id'][0])
            nonexistent.append(id)
            self.crawler.stats.set_value('nonexistent',str(nonexistent))
            return None
        item = Team()
        item['id'] = parse_qs(response.xpath('//div[@class="clearfix subnav level-1"]//li//a[2]/@href').extract_first())['id'][0]
        item['name'] = response.xpath('//div[@class="clearfix subnav level-1"]//li//a[2]/text()').extract_first()
        item['area_id'] = parse_qs(response.xpath('//div[@class="clearfix subnav level-1"]//a[1]/@href').extract()[1])['area_id'][0]
        item['area_name'] = response.xpath('//div[@class="clearfix subnav level-1"]//a[1]/text()').extract()[1]
        item['website'] = response.xpath('//p[@class="center website"]/a/@href').extract_first()
        item['address'] = ", ".join(list(map(str.strip, response.xpath('//div[@class="clearfix"]/dl/dt[.="Address"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Address"]/text()').extract())))
        item['founded'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Founded"]/following-sibling::dd/text()').extract_first()
        item['country'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Country"]/following-sibling::dd/text()').extract_first()
        item['phone'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Phone"]/following-sibling::dd/text()').extract_first()
        item['fax'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Fax"]/following-sibling::dd/text()').extract_first()
        item['email'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="E-mail"]/following-sibling::dd/a/text()').extract_first()
        item['updated'] = datetime.utcnow().isoformat(' ')
        yield item
        return item
        #self.log('URL: {}'.format(response.url))

