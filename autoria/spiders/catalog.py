import scrapy
from autoria.items import CarItem


class CatalogSpider(scrapy.Spider):
    name = 'catalog'

    # allowed_domains = ['auto.ria.com']
    # start_urls = ['https://auto.ria.com/uk/legkovie/tesla/']
    def start_requests(self):
        url = 'https://auto.ria.com/uk/legkovie/tesla/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, *args, **kwargs):
        auto_cards = response.css('div.content')
        for auto_card in auto_cards:
            auto = CarItem()
            auto['model'] = auto_card.css('span::text').get().strip()
            auto['year'] = auto_card.css('div.head-ticket a[class="address"]::text')[1].get().strip()
            auto['mileage'] = auto_card.css('li[class="item-char js-race"]::text').get().strip()
            auto['price_uah'] = auto_card.css('span[data-currency="UAH"]::text').get()
            auto['price_usd'] = auto_card.css('span[data-currency="USD"]::text').get()
            auto['vin_code'] = self.extract_vin_code(auto_card.css('span.label-vin span'))
            auto['link'] = auto_card.css('a::attr(href)').get()
            yield auto

        next_page_button = response.css('span[class="page-item next text-r"]')
        next_page_is_available = 'disabled' not in next_page_button.css('a::attr(class)').get()
        if next_page_is_available:
            url = next_page_button.css('a::attr(href)').get()
            yield scrapy.Request(url=url, callback=self.parse)

    def extract_vin_code(self, vin_code_parts):
        vin_code = ''
        for part_of_the_vin in vin_code_parts:
            span_text = part_of_the_vin.css('span::text').get().strip()
            if span_text.startswith(('AUTO.RIA', 'Проверено')):
                break
            vin_code += span_text
        return vin_code
