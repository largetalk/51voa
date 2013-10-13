from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from voa.items import VoaSpecialItem
from voa.utils import get_redis
from voa.utils import _f

class SpecialEnglishSpider(CrawlSpider):
    name = 'special_english'
    allowed_domains = ['www.51voa.com']
    start_urls = ['http://www.www.51voa.com/VOA_Special_English/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'VOA_Special_English/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = VoaSpecialItem()
        i['title'] = _f(hxs.select('//*[@id="title"]/text()').extract())
        i['category'] = _f(hxs.select('//*[@id="nav"]/a[3]/text()').extract())
        i['day'] = _f(hxs.select('//*[@id="content"]/span[2]').extract())
        i['page_url'] = response.url
        i['mp3_url'] = _f(hxs.select('//*[@id="mp3"]/attribute::href').extract())
        i['article'] = _f(hxs.select('//*[@id="content"]/text()').extract())

        redis = get_redis()
        redis.set(i['page_url'], i)
        return i
