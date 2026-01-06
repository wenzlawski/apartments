import re
from datetime import datetime

from scrapy.spiders import Spider
from sqlmodel import Session, select

from app.core.db import engine
from app.models import Apartment, ApartmentPage


class KleinanzeigenSpider(Spider):
    name = "kleinanzeigen"
    allowed_domains = ["kleinanzeigen.de"]
    root_url = "https://www.kleinanzeigen.de"

    ID_RE = re.compile(r"/(\d+)-\d+-\d+$")

    custom_settings = {
        "CONCURRENT_REQUESTS": 8,
        "DOWNLOAD_DELAY": 0.25,
        "LOG_LEVEL": "DEBUG",
    }

    def __init__(self, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not start_url:
            raise ValueError("start_url argument is required")

        self.start_urls = [start_url]

        self.stop_pagination = False
        self.engine = engine

    def parse(self, response):
        self.logger.info("Parsing search page")
        links = response.css("article.aditem::attr(data-href)").getall()
        filtered = self.filter_known_links(links)

        if not filtered:
            self.logger.info("Known listings reached - stopping pagination")
            return

        for href in filtered:
            yield response.follow(self.root_url + href, self.parse_item)

        # Extract next page link from site instead of hardcoding
        next_page = response.css("a.pagination-next::attr(href)").get()
        if next_page:
            yield response.follow(self.root_url + next_page, self.parse)

    def filter_known_links(self, links):
        return []
        pairs = [
            (apt_id, href)
            for href in links
            if (apt_id := self.extract_apartment_id(href))
        ]

        if not pairs:
            return []

        ids = [p[0] for p in pairs]

        with Session(self.engine) as session:
            existing = session.exec(
                select(Apartment.posting_id).where(Apartment.posting_id.in_(ids))
            ).all()

        known_ids = set(existing)

        return [href for apt_id, href in pairs if apt_id not in known_ids]

    def parse_european_number(self, num_str):
        return float(num_str.replace(".", "").replace(",", "."))

    def extract_apartment_id(self, href):
        m = self.ID_RE.search(href)
        return m.group(1) if m else None

    def parse_item(self, response):
        self.logger.info(f"Parsing page for item at {response.url}")
        apt_id = self.extract_apartment_id(response.url)

        yield {
            "posting_id": apt_id,
            "pages": [
                ApartmentPage(
                    url=response.url,
                    content=response.text,
                    scraped_at=datetime.utcnow(),
                )
            ],
        }
        # result_script = item.css('script::text').get()

        # script_json = json.loads(result_script)

        # parsed["title"] = script_json["title"]
        # parsed["description"] = script_json["description"]

        # location = item.css("div.aditem-main--top--left::text").getall()

        # location = ' '.join(word for s in location for word in s.split())

        # parsed["location"] = location.split('(')[0].split(maxsplit=1)[1].strip()
        # parsed["plz"] = location.split(None, 1)[0]

        # price = item.css("p.aditem-main--middle--price-shipping--price::text").get().strip()
        # price_old = item.css("span.aditem-main--middle--price-shipping--old-price::text").get().strip()

        # parsed["price"] = self.parse_european_number(price.split()[0])
        # parsed["price_old"] = self.parse_european_number(price_old.split()[0]) if price_old else None
        # self.logger.info(f"{price=}")
        # self.logger.info(f"{price_old=}")
        # self.logger.info(f"{parsed=}")

        # return parsed
