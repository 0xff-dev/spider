#!/usr/bin/env python
# coding=utf-8

import asyncio
import aiohttp
import time, re
import multiprocessing as mp
from urllib.request import urljoin
from bs4 import BeautifulSoup


BASE_URL = 'https://morvanzhou.github.io/'


async def crawl(url, session):
    resp = await session.get(url)
    html = await resp.text()
    await asyncio.sleep(0.1)
    return html


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.find_all('a', {"href": re.compile('^/.+?/$')})
    title = soup.find('h1').get_text().strip()
    page_urls = set([urljoin(BASE_URL, url['href']) for url in urls])
    url = soup.find('meta', {'property': "og:url"})['content']
    return title, page_urls, url


unseen = set([BASE_URL])
seen = set()

async def main(loop):
    pool = mp.Pool(4)
    async with aiohttp.ClientSession() as session:
        count = 1
        while len(unseen) != 0:
            # 创建异步任务
            print('Asyncing Crawl...')
            tasks = [loop.create_task(crawl(url, session)) for url in unseen]
            finished, unfinished = await asyncio.wait(tasks)
            htmls = [f.result() for f in finished]
            
            # 多进程解析
            print('Pool Parsing...')
            parse_jobs = [pool.apply_async(parse, args=(html,)) for html in htmls]
            results = [r.get() for r in parse_jobs]
            seen.update(unseen)
            unseen.clear()

            for title, page_urls, url in results:
                print(count, title, url)
                unseen.update(page_urls-seen)
                count += 1
            
if __name__ == '__main__':
    # 创建时间循环
    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    print('All time {}.'.format(time.time()-start))
