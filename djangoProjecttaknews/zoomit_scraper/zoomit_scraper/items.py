# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ZoomitItem(scrapy.Item):
    title = scrapy.Field()
    slug = scrapy.Field()
    summary = scrapy.Field()
    content = scrapy.Field()
    source_url = scrapy.Field()
    publish_date = scrapy.Field()
    image_url = scrapy.Field()
    tags = scrapy.Field()
    categories = scrapy.Field()