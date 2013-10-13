# Scrapy settings for voa project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'voa'

SPIDER_MODULES = ['voa.spiders']
NEWSPIDER_MODULE = 'voa.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'voa (+http://www.yourdomain.com)'

HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = '/tmp/spidercache/'

LOG_LEVEL = 'INFO'

DOWNLOADER_MIDDLEWARES = {
}

SPIDER_MIDDLEWARES = {
    ‘voa.middlewares.DduplicateMiddleware’: 543,   #这是爬虫中间件，， 543是运行的优先级
}
FILE_CACHE = '/tmp/spidercachefile'
DEPTH_PRIORITY = 0
DEPTH_LIMIT = 3 

REDIS_SERVER = '127.0.0.1'
