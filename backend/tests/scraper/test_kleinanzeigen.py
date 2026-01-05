import pytest
from app.scraper.spiders.kleinanzeigen import KleinanzeigenSpider
from scrapy.http import HtmlResponse, Request


@pytest.fixture
def spider():
    return KleinanzeigenSpider(
        start_url="https://www.kleinanzeigen.de/s-wohnung-kaufen/test/c1l1"
    )


def fake_response(url, html):
    request = Request(url=url)
    return HtmlResponse(url=url, request=request, body=html, encoding="utf-8")


def test_extract_apartment_id(spider):
    href = "/s-anzeige/altbauwohnung/2864938123-196-3331"
    assert spider.extract_apartment_id(href) == "2864938123"


def test_filter_known_links(monkeypatch, spider):
    html_links = [
        "/s-anzeige/test/111-1-1",
        "/s-anzeige/test/222-1-1",
        "/s-anzeige/test/333-1-1",
    ]

    # Pretend apartment 222 already exists
    def fake_filter(links):
        return [l for l in links if "222" not in l]

    monkeypatch.setattr(spider, "filter_known_links", fake_filter)

    filtered = spider.filter_known_links(html_links)
    assert "/s-anzeige/test/222-1-1" not in filtered
    assert len(filtered) == 2


def test_parse_paginates(spider, monkeypatch):
    html = """
    <html>
      <body>
        <article class="aditem" data-href="/s-anzeige/test/111-1-1"></article>
        <a class="pagination-next" href="/seite:2"></a>
      </body>
    </html>
    """

    response = fake_response(spider.start_urls[0], html)

    monkeypatch.setattr(spider, "filter_known_links", lambda links: links)

    results = list(spider.parse(response))

    item_requests = [r for r in results if "s-anzeige" in r.url]
    next_page = [r for r in results if "seite:2" in r.url]

    assert len(item_requests) == 1
    assert len(next_page) == 1


def test_parse_stops_on_known(spider, monkeypatch):
    html = """
    <html>
      <body>
        <article class="aditem" data-href="/s-anzeige/test/111-1-1"></article>
      </body>
    </html>
    """

    response = fake_response(spider.start_urls[0], html)

    monkeypatch.setattr(spider, "filter_known_links", lambda links: [])

    results = list(spider.parse(response))
    assert results == []
