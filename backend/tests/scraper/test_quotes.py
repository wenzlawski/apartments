import glob
import os

import pytest
from app.scraper.spiders.quotes_spider import QuotesSpider
from scrapy.http import HtmlResponse

base_dir = os.path.dirname(__file__)
path = os.path.join(base_dir, "sites/quotes/")


@pytest.fixture
def spider():
    return QuotesSpider()


html_files = glob.glob(os.path.join(path, "*.html"))


@pytest.mark.parametrize("html_file", html_files)
def test_parse_all_html_files(spider, html_file):
    with open(html_file, "rb") as f:
        response = HtmlResponse(url="http://test.com", body=f.read())
    results = spider.parse(response)
    # Modify the assertion below as needed for your tests!
    assert results.xpath("//h1/text()").get() == "Example"


def test_parse(spider):
    response = HtmlResponse(url="http://example.com", body=b"<h1>Example</h1>")
    results = spider.parse(response)
    assert results.xpath("//h1/text()").get() == "Example"


def test_dir(spider):
    with open(os.path.join(path, "1.html"), "rb") as f:
        response = HtmlResponse(url="http://test.com", body=f.read())
    results = spider.parse(response)
    assert results.xpath("//h1/text()").get() == "Example"
