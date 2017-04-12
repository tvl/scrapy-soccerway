# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from soccerway.items import Match
from urllib.parse import urlencode, urlparse, parse_qs
from datetime import datetime, timezone
from soccerway.competitions import competitions_id_list

class MatchesSpider(Spider):
    name = "matches"
    allowed_domains = ["http://www.soccerway.mobi"]
    start_urls = ['http://www.soccerway.mobi/?']
    params = {
        "sport": "soccer",
        "page": "match",
        "id" : "2255155",
        "localization_id": "www"
    }
    def start_requests(self):
        start_url = 'http://www.soccerway.mobi/?sport=soccer&page=competition&id={}&localization_id=www'
        for i in competitions_id_list:
            request = Request(url=start_url.format(str(i)), callback=self.parse)
            request.meta['proxy'] = 'http://127.0.0.1:8118'
            yield request

    def parse(self, response):
        items = []
        area_id = parse_qs(response.xpath('//div[@class="clearfix subnav level-1"]//a[1]/@href').extract()[1])['area_id'][0]
        area_name = response.xpath('//div[@class="clearfix subnav level-1"]//a[1]/text()').extract()[1]
        competition_id = parse_qs(response.xpath('//div[@class="clearfix subnav level-1"]//li//a[2]/@href').extract_first())['id'][0]
        competition_name = response.xpath('//div[@class="clearfix subnav level-1"]//li//a[2]/text()').extract_first()
        matches = response.xpath('//table[@class="matches   "]//tbody//tr')
        for m in matches:
            item = Match()
            item['id'] = parse_qs(m.xpath('./td[@class="info-button button"]//a/@href').extract_first())['id'][0]
            item['datetime'] = datetime.fromtimestamp(int(m.xpath('@data-timestamp').extract_first()), timezone.utc).isoformat(' ')
            item['home_team_id'] = parse_qs(m.xpath('./td[contains(@class, "team team-a")]//a/@href').extract_first())['id'][0]
            item['away_team_id'] = parse_qs(m.xpath('./td[contains(@class, "team team-b")]//a/@href').extract_first())['id'][0]
            item['home_team'] = m.xpath('./td[contains(@class, "team team-a")]//a/text()').extract_first().strip()
            item['away_team'] = m.xpath('./td[contains(@class, "team team-b")]//a/text()').extract_first().strip()
            item['kick_off'] = m.xpath('./td[@class="score-time status"]//span/text()').extract_first()
            item['score'] = m.xpath('./td[@class="score-time score"]//span/text()').extract_first()

            item['area_id'] = area_id
            item['area_name'] = area_name
            item['competition_id'] = competition_id
            item['competition_name'] = competition_name

            item['updated'] = datetime.utcnow().isoformat(' ')
            yield item
            items.append(item)
        return items
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

