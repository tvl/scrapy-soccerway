# -*- coding: utf-8 -*-
import scrapy
from soccerway.items import Match
from urllib.parse import urlencode

class MatchesSpider(scrapy.Spider):
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
        for i in range(2255155,2255155+5):
            self.params['id'] = str(i)
            request = scrapy.Request(url=self.start_urls[0]+urlencode(self.params), callback=self.parse)
            request.meta['proxy'] = 'http://127.0.0.1:8118'
            yield request

    def parse(self, response):
        self.log('URL: {}'.format(response.url))

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

