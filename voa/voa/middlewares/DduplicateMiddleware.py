from scrapy import signals,log
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http import Request
from voa.utils import get_redis
 
class CustomSpiderMiddleware(object):
    redis = None
    lock = True
    info = {}
    def __init__(self):
        dispatcher.connect(self.open,signals.engine_started)
        dispatcher.connect(self.close,signals.engine_stopped)
    def process_spider_output(self,response, result, spider):
        if self.lock is True:
            self.info = spider
            self.lock = False
        for x in result:
            if isinstance(x, Request):
                if self.redis.zrank(spider.name,x.url) is not None:
                    log.msg(format="Filtered offsite request to page: %(request)s",
                                level=log.DEBUG, spider=spider, request=x)
                else:
                    yield x
            else:
                yield x
 
    def open(self):
        self.redis = get_redis()
    def close(self):
        self.redis.zrem(self.info.name,*self.info.start_urls)

