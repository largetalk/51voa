# Scrapy settings for voa project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os, sys

BOT_NAME = 'voa'

SPIDER_MODULES = ['voa.spiders']
NEWSPIDER_MODULE = 'voa.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'voa (+http://www.yourdomain.com)'

#HTTPCACHE_ENABLED = True
#HTTPCACHE_DIR = '/tmp/spidercache'

LOG_LEVEL = 'DEBUG'

#DOWNLOADER_MIDDLEWARES = {
#}

#SPIDER_MIDDLEWARES = {
#    'voa.middlewares.duplicate.DduplicateMiddleware': 543,
#}

#FILE_CACHE = '/tmp/spidercachefile'
#DEPTH_PRIORITY = 0
#DEPTH_LIMIT = 3 

REDIS_SERVER = '127.0.0.1'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
COOKIES_ENABLED = True

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

SPE_MP3_STORE_DIR = os.path.join(PROJECT_DIR, 'SPE_MP3')
STE_MP3_STORE_DIR = os.path.join(PROJECT_DIR, 'STE_MP3')
