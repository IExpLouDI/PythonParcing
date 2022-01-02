# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramItem(scrapy.Item):
    # define the fields for your item here like:
    user_db = scrapy.Field()
    user_section = scrapy.Field()
    user_nick_name = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    user_img = scrapy.Field()
    _id = scrapy.Field()
