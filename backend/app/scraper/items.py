# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


@dataclass
class KleinanzeigenSearchItem:
    title: str
    price: float
    price_old: float | None
    plz: str
    location: str
    m2: float
    rooms: float
