import glob
import os

import pytest
from scrapy.http import HtmlResponse

from app.scraper.scraper.spiders.kleinanzeigen_spider import KleinanzeigenSpider

base_dir = os.path.dirname(__file__)
path = os.path.join(base_dir, "sites/kleinanzeigen/")


@pytest.fixture
def spider():
    return KleinanzeigenSpider()


html_files = glob.glob(os.path.join(path, "*.html"))


@pytest.mark.parametrize("html_file", html_files)
def test_parse_all_html_files(spider, html_file):
    with open(html_file, "rb") as f:
        response = HtmlResponse(url="http://test.com", body=f.read())
    results = spider.parse(response)
    # Modify the assertion below as needed for your tests!
    assert results.xpath("//*[@id='srchrslt-adtable']").get() is not None
