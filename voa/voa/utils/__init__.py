#coding:utf-8

import redis
import re
import threading
import os, sys
import subprocess
from scrapy import log
from voa.settings import REDIS_SERVER

_lock = threading.Lock()
_redis = None

def get_redis():
    if _redis:
        return _redis
    global _redis
    try:
        _lock.acquire()
        _redis = redis.Redis(REDIS_SERVER, db=3)
        return _redis
    finally:
        _lock.release()

_f = lambda x:x[0] if isinstance(x, list) and len(x) else ''

def split_title_day(textin):
    textin = textin.strip()
    reg = re.compile('\((\d{4}-\d{1,2}-\d{1,2})\)$')
    out = reg.split(textin)
    if len(out) < 2:
        return textin, ''
    else:
        return out[0].strip(), out[1]

def strip_tags(html):
    """
    Python中过滤HTML标签的函数
    >>> str_text=strip_tags("<font color=red>hello</font>")
    >>> print str_text
    hello
    """
    from HTMLParser import HTMLParser
    html = html.strip()
    html = html.strip("\n")
    result = []
    parser = HTMLParser()
    parser.handle_data = result.append
    parser.feed(html)
    parser.close()
    return ''.join(result)

def guarant_dir_exists(path):
    log.msg(path)
    if not os.path.exists(path):
        os.makedirs(path)

def wget_download_mp3(url, fdir, name):
    guarant_dir_exists(fdir)
    command = 'cd %s && /usr/bin/wget -P %s -c -t 5 %s -O %s' % (fdir, fdir, url, name)
    log.msg(command)
    returnCode = subprocess.call(command, shell=True)
    return returnCode

