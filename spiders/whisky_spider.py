import scrapy
from scrapy.spider import BaseSpider
from scrapy.http import Request
class WhiskySpider(scrapy.Spider):
    name = "whisky"
    allowed_domains = ['www.whiskybase.com']
    max_cid = 90000
	
    def start_requests(self):
        for i in range(self.max_cid):
            yield Request('https://www.whiskybase.com/whisky/%d' % i,
                    callback=self.parse)
					
    def parse(self, response):
        for quote in response.css('body > div.container.page'):
            yield {
                'BRAND': quote.css('div.content > div:nth-child(1) > div > h1 > span.whisky-brandname > a::text').extract_first(),
				'NAME': quote.css('div.content > div:nth-child(1) > div > h1 > span.whisky-name::text').extract_first(),
				'DISTILLERY': quote.css('#whisky-distillery-list > a::text').extract_first(),
				'RATING': quote.css('#whisky-rating::text').extract_first().strip(),
				'AGE' : quote.xpath("//*[@id='whisky-info']//text()[contains(.,'Age')]/../../*[contains(@class, 'v2 val v2')]/text()").re(r'([0-9]+)'),
				'PRICE' : quote.xpath("//*[@id='whisky-info']//*[contains(@class, 'whisky_price')]/text()").extract()[1].strip()
				

            }