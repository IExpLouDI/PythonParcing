import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SupjobSpider(scrapy.Spider):

    name = 'supjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://mo.superjob.ru/vacancy/search/?keywords=python',
                  'https://spb.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[contains(@class, 'dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[contains(@class, 'icMQ_ _6AfZ9')]//@href").getall()

        for link in links:
            yield response.follow(link, callback=self.vacan_parse)


    def vacan_parse(self, response: HtmlResponse):

        name = response.xpath("//h1//text()").get()
        salary = response.xpath("//span[contains(@class, '_1OuF_ ZON4b')]//text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
