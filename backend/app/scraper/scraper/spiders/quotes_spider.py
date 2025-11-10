from pathlib import Path

import scrapy
from scrapy.selector import Selector


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    async def start(self):
        urls = [
            "https://www.kleinanzeigen.de/s-suchanfrage.html?keywords=&categoryId=196&locationStr=Berlin&locationId=3331&radius=0&sortingField=SORTING_DATE&adType=&posterType=&pageNum=1&action=find&maxPrice=&minPrice=&buyNowEnabled=false&shippingCarrier="
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
        return Selector(response)
