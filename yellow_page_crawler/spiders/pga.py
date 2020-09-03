from urllib.parse import urljoin
from scrapy import Request, Spider
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest
from ..items import YellowPageCrawlerItem

script = """
    function main(splash, args)
        splash.images_enabled = false
        assert(splash:go(args.url))
        assert(splash:wait(1))
        splash:runjs("$('div.buttonShowCo').click();")
        assert(splash:wait(5))
        return {
            html = splash:html(),
        }
    end
"""


class PgaSpider(Spider):
    name = 'pga'
    base_url = "https://www.yellowpagesofafrica.com"

    def start_requests(self):
        urls = [
            'https://www.yellowpagesofafrica.com/country/madagascar/'
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        activity_urls = response.xpath(
            ".//a[contains(@title, '- MADAGASCAR')]/@href"
        )

        # In case of limiting pages per activity
        #page_count = 1
        for url in activity_urls:
            # if page_count < 5:
            #     page_count += 1
            yield SplashRequest(url=urljoin(self.base_url, url.get()),
                                callback=self.parse_activity,
                                endpoint='execute',
                                args={'lua_source': script,
                                      'timeout': 10,
                                      'wait': 10},
                                )
            # yield Request(url=activity_url, callback=self.parse_activity)

    def parse_activity(self, response):
        activity = response.xpath(
            'normalize-space(.//h4[@class="ct-u-marginBottom20"])'
        )
        company_names = response.xpath(
            './/*[contains(@class, "ct-product--tilte")]'
        )
        company_addrs = response.xpath(
            './/*[contains(@class, "ct-product--description")]'
        )
        company_contacts = response.xpath(
            './/div[contains(@id, "coordonnees")]')

        for (name, addr, contact) in zip(company_names, company_addrs, company_contacts):
            items = ItemLoader(item=YellowPageCrawlerItem())

            # Activity denomination
            activity_name = activity.extract_first()
            items.add_value('activity', activity_name)
            # Name of the entity
            company_name = name.xpath(
                'normalize-space(./text())').extract_first()
            items.add_value('name', company_name)
            # Address
            address = addr.xpath('./text()').getall()
            items.add_value('address', address)
            # Contact = Mail + Phone
            contact = contact.css('::text').getall()

            # Phone
            items.add_value('phone', contact)
            # Mail
            items.add_value('mail', contact)

            yield items.load_item()

        next_page = response.css('a[aria-label=Next]::attr(href)').get()

        if next_page:
            yield SplashRequest(url=urljoin(self.base_url, next_page),
                                callback=self.parse_activity,
                                endpoint='execute',
                                args={'lua_source': script,
                                      'timeout': 10,
                                      'wait': 10},
                                )
