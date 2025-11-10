import scrapy
from scrapy.selector import Selector


class KleinanzeigenSpider(scrapy.Spider):
    name = "kleinanzeigen"

    async def start(self):
        pass

    def parse(self, response):
        return Selector(response)
