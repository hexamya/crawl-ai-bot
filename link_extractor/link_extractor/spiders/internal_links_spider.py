import scrapy
from urllib.parse import urlparse, urlunparse


class InternalLinksSpider(scrapy.Spider):
    name = "internal_links"

    start_urls = ['https://zaviehmag.ir/']
    visited_links = set()

    def parse(self, response, **kwargs):
        domain = urlparse(response.url).netloc

        for href in response.css('a::attr(href)').getall():
            link = response.urljoin(href)
            link_domain = urlparse(link).netloc

            raw_link = link.split('?')[0].split('#')[0]
            if link_domain == domain and raw_link not in self.visited_links:
                self.visited_links.add(raw_link)
                yield {
                    'url': raw_link
                }

                yield response.follow(raw_link, self.parse)
