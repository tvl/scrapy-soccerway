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
        for i in range(1,213): # 1 - 212
            request = Request(url=start_url.format(str(i)), callback=self.parse)
            request.meta['proxy'] = 'http://127.0.0.1:8118'
            yield request

    def parse(self, response):
        l = ItemLoader(item=Competition(), response=response)
        area_id = parse_qs(response.xpath('//div[@class="clearfix subnav level-1"]//li//a[2]/@href').extract()[0])['area_id'][0]
        area_name = response.xpath('//div[@class="clearfix subnav level-1"]//li//a[2]/text()').extract()

        for i in
            l.add_value('ID', )
            l.add_value('area_id', area_id)
            l.add_value('area_name', area_name)
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

