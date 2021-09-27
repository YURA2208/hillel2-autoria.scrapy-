import scrapy


class CarItem(scrapy.Item):
    model = scrapy.Field()
    year = scrapy.Field()
    mileage = scrapy.Field()
    price_uah = scrapy.Field()
    price_usd = scrapy.Field()
    vin_code = scrapy.Field()
    link = scrapy.Field()
