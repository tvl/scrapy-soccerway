# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from soccerway.items import Venue
from urllib.parse import urlencode, urlparse, parse_qs
from datetime import datetime, timezone
from soccerway.competitions import competitions_id_list
from random import randint

areas = ['afghanistan', 'albania', 'algeria', 'andorra', 'angola', 'argentina', 'armenia', 'aruba', 'australia', 'austria',
        'azerbaijan', 'bahrain', 'bangladesh', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bolivia',
        'botswana', 'brazil', 'bulgaria', 'cambodia', 'cameroon', 'canada', 'chad', 'chile', 'colombia', 'congo', 'croatia',
        'cuba', 'cyprus', 'denmark', 'ecuador', 'england', 'estonia', 'ethiopia', 'finland', 'france', 'gabon', 'gambia',
        'georgia', 'germany', 'ghana', 'greece', 'grenada', 'guam', 'guatemala', 'guinea', 'guyana', 'honduras', 'hungary',
        'iceland', 'india', 'indonesia', 'iran', 'iraq', 'israel', 'italy', 'jamaica', 'japan', 'jordan', 'kazakhstan', 'kenya',
        'kuwait', 'kyrgyzstan', 'laos', 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania',
        'luxembourg', 'macao', 'malaysia', 'malta', 'mexico', 'moldova', 'mongolia', 'morocco', 'mozambique', 'namibia', 'nepal',
        'netherlands', 'nicaragua', 'niger', 'nigeria', 'norway', 'oman', 'pakistan', 'palestine', 'panama', 'paraguay', 'peru',
        'philippines', 'poland', 'portugal', 'romania', 'russia', 'rwanda', 'samoa', 'scotland', 'senegal', 'slovakia',
        'slovenia', 'somalia', 'spain', 'sudan', 'swaziland', 'sweden', 'switzerland', 'syria', 'tajikistan', 'tanzania',
        'thailand', 'togo', 'tonga', 'tunisia', 'turkey', 'turkmenistan', 'uganda', 'ukraine', 'usa', 'uruguay',
        'uzbekistan', 'venezuela', 'vietnam', 'wales', 'yemen', 'zambia', 'zimbabwe']

areas_count = len(areas)

class TeamsSpider(Spider):
    name = "venues"
    #allowed_domains = ["http://www.soccerway.mobi"]
    start_urls = ['http://www.soccerway.mobi/?']
    params = {
        "sport": "soccer",
        "page": "match",
        "id" : "2255155",
        "localization_id": "www"
    }
    def start_requests(self):
        start_url = 'http://int.soccerway.com/venues/{}/venue/v{}/'
        for i in range(925, 938): # 27617 on 12.04.2017, 29392 on 15.01.2018
            request = Request(url=start_url.format(areas[randint(0, areas_count-1)], str(i)), callback=self.parse)
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
        item['city'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="City:"]/following-sibling::dd[preceding-sibling::dt[1]/text()="City:"]/text()').extract_first()
        item['phone'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Phone:"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Phone:"]/text()').extract_first()
        item['fax'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Fax:"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Fax:"]/text()').extract_first()
        item['email'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="E-mail:"]/following-sibling::dd[preceding-sibling::dt[1]/text()="E-mail:"]/a/text()').extract_first()
        item['website'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Website:"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Website:"]/a/text()').extract_first()
        item['opened'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Opened:"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Opened:"]/text()').extract_first()
        item['architect'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Architect:"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Architect:"]/text()').extract_first()
        item['capacity'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Capacity:"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Capacity:"]/text()').extract_first()
        item['surface'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Surface:"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Surface:"]/text()').extract_first()
        item['previous'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Previous names:"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Previous names:"]/text()').extract_first()
        item['facts'] = response.xpath('//div[@class="clearfix"]/dl/dt[.="Facts:"]/following-sibling::dd[preceding-sibling::dt[1]/text()="Facts:"]/text()').extract_first()
        script = response.xpath('//script[contains(., "setMarker")]').extract_first()
        if not script is None:
            item['lat'] = response.xpath('//script[contains(., "setMarker")]').extract_first().split('\n')[10][:-1].strip()
            item['lon'] = response.xpath('//script[contains(., "setMarker")]').extract_first().split('\n')[11][:-1].strip()
            item['link'] = response.xpath('//script[contains(., "setMarker")]').extract_first().split('\n')[19][:-1].strip().strip('"')
        #item['url'] = response.url
        item['updated'] = datetime.utcnow().isoformat(' ')
        yield item
        return item
        #self.log('URL: {}'.format(response.url))

