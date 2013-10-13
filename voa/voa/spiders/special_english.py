import os, sys
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log
from voa.items import VoaSpecialItem
from voa.utils import get_redis
from voa.utils import split_title_day
from voa.utils import strip_tags
from voa.utils import _f
from voa.utils import wget_download_mp3
from voa.settings import SPE_MP3_STORE_DIR

class SpecialEnglishSpider(CrawlSpider):
    name = 'special'
    allowed_domains = ['51voa.com']
    start_urls = ['http://www.51voa.com/VOA_Special_English/']
    _redis = get_redis()

    #rules = (
    #    Rule(SgmlLinkExtractor(allow=['/VOA_Special_English/.*']), callback='parse_item', follow=True),
    #)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        alst = hxs.select('//*[@id="list"]/ul/li/a')
        for asel in alst:
            atext = _f(asel.select('text()').extract()).strip()
            ahref = _f(asel.select('attribute::href').extract()).strip()
            if ahref.startswith('/VOA_Special_English') or ahref.startswith('http://www.51voa.com/VOA_Special_English/'):
                title, day = split_title_day(atext)
                page_url = ahref if ahref.startswith('http') else 'http://www.51voa.com' + ahref

                if self._redis.exists(page_url):
                    continue

                i = VoaSpecialItem()
                i['page_url'] = page_url
                i['day'] = day
                yield Request(page_url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        log.msg(response.url)
        hxs = HtmlXPathSelector(response)
        i = VoaSpecialItem()
        i['title'] = _f(hxs.select('//*[@id="title"]/text()').extract())
        i['category'] = _f(hxs.select('//*[@id="nav"]/a[3]/text()').extract())
        i['day'] = _f(hxs.select('//*[@id="content"]/span[2]').extract())
        i['page_url'] = response.url
        i['mp3_url'] = _f(hxs.select('//*[@id="mp3"]/attribute::href').extract())
        x = _f(hxs.select('//*[@id="content"]'))
        i['article'] = strip_tags(x.extract())

        if self.download_mp3(i['mp3_url']):
            redis = get_redis()
            redis.set(i['page_url'], i)
        return i

    def download_mp3(self, mp3_url):
        base_dir = SPE_MP3_STORE_DIR
        old_mp3_url = mp3_url
        mp3_url = mp3_url.lstrip('http://')
        if not mp3_url.find('/'):
            return False
        lslash = mp3_url.find('/')
        rslash = mp3_url.rfind('/')
        mid_dir = mp3_url[lslash+1 : rslash]
        name = mp3_url[rslash + 1:]

        if wget_download_mp3(old_mp3_url, os.path.join(base_dir, mid_dir), name) == 0:
            return True
        return False


