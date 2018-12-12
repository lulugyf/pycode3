import scrapy
import re

class MoneyNewsItem(scrapy.Item):
    # define the fields for your item here like:
    news_title = scrapy.Field()
    news_body = scrapy.Field()
    news_url = scrapy.Field()


class moneySpider(scrapy.Spider):
    name="myspider"
    allowed_domains = ["money.163.com"]
    start_urls = ["http://money.163.com/", "http://money.163.com/stock/"]
    follow=True
    # rules = Rule(
    #     LinkExtractor(allow=r"/\d+/\d+/\d+/*"),
    #     follow=True,
    #     callback="moneyparser"
    # )
    #def start_requests(self):
    #    for url in start_urls:
    #        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if re.search(r"/\d+/\d+/\d+/*", response.url) is None:
            return None
        #page = response.url.split("/")[-2]
        item = MoneyNewsItem()
        title = response.xpath("/html/head/title/text()").extract()
        if title:
            item['news_title'] = title[0][:-5]
        news_url = response.url
        if news_url:
            item['news_url'] = news_url
        news_body = response.xpath("//div[@id='endText']/p/text()").extract()
        if news_body:
            item['news_body'] = news_body
        return item

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
        # scrapy crawl quotes -o quotes.json
        # scrapy crawl quotes -o quotes.jl


