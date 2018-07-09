#!/usr/bin/env python
# coding=utf-8


"""Tornado 异步爬虫"""


import time
from datetime import datetime, timedelta
from urllib.parse import urljoin, urldefrag

from html.parser import HTMLParser
from tornado.httpclient import AsyncHTTPClient
from tornado import gen, ioloop, queues


BASE_URL = 'http://www.tornadoweb.org/en/stable/'
concurrency = 10


@gen.coroutine
def get_link_from_url(url):
    """
    从给定的url中解析页面中的链接, 在返回urls, 通过raise抛出
    """
    try:
        resp = yield AsyncHTTPClient().fetch(url)
        print ('Fetched {}'.format(url))
        html = resp.body if isinstance(resp.body, str) \
                else resp.body.decode()
        urls = [urljoin(url, remove_fragment(new_url))
                for new_url in get_links(html)]
    except Exception as e:
        print ('Exception {}:{}'.format(e, url))
        raise gen.Return([])
    raise gen.Return(urls)


def remove_fragment(url):
    pure_url, frag = urldefrag(url)
    return pure_url


def get_links(html):
    class URLSeeker(HTMLParser):
        
        def __init__(self):
            super(URLSeeker, self).__init__()
            self.__urls = []

        def handle_starttag(self, tag, attrs):
            href=dict(attrs).get('href')
            if href and tag == 'a':
                self.__urls.append(href)

        @property
        def urls(self):
            return self.__urls
    
    url_seeker = URLSeeker()
    url_seeker.feed(html)
    return url_seeker.urls

@gen.coroutine
def main():
    q = queues.Queue()
    start = time.time()
    fetching, fetched = set(), set()
    
    @gen.coroutine
    def fetch_url():
        current_url = yield q.get()
        try:
            if current_url in fetching:
                return
            print ('fetching {}'.format(current_url))
            fetching.add(current_url)
            urls = yield get_link_from_url(current_url)
            fetched.add(current_url)
            for new_url in urls:
                if new_url.startswith(BASE_URL) and new_url not in fetched:
                    yield q.put(new_url)
        finally:
            # 减少计数次数
            q.task_done()
    
    @gen.coroutine
    def worker():
        while True:
            yield fetch_url()

    q.put(BASE_URL)
    
    for _ in range(concurrency):
        worker()
    yield q.join(timeout=timedelta(seconds=300))
    assert fetching == fetched
    print ('Done in {} seconds fetched {} urls'.format(
            time.time()-start, len(fetched)
            ))

if __name__ == '__main__':
    import logging
    logging.basicConfig()
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)
    # 写完后的感觉是, 遇到I/O的时候, yield, 貌似这么理解没有问题

