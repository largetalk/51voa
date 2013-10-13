# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class VoaSpecialItem(Item):
    title = Field()
    category = Field()
    day = Field()
    page_url = Field()
    mp3_url = Field()
    article = Field()
