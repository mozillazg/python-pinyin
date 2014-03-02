#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""从汉典网(www.zdic.net)获取所有的汉字，找出拼音库未包含的汉字"""

import logging
from time import sleep

from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)


def parse_words(html):
    """解析 html 源码，返回汉字列表"""
    soup = BeautifulSoup(html)
    a_list = soup.find_all('a', attrs={'target': '_blank'})
    return [x.text for x in a_list if x.text]


def get_one_page(url, cookies, headers):
    r = requests.get(url, headers=headers, cookies=cookies)
    cookies.update(r.cookies.get_dict())
    return r.text


def main():
    import io
    from pypinyin.pinyin_dict import pinyin_dict

    headers = {
        'Referer': 'http://www.zdic.net/z/jbs/zbh/',
        'User-Agent': ('Mozilla/5.0 (Windows NT 6.2; rv:26.0) Gecko/20100101 '
                       'Firefox/26.0'),
    }
    url_base = 'http://www.zdic.net/z/jbs/zbh/bs/?jzbh=%s|%s'
    cookies = requests.get('http://www.zdic.net/z/jbs/zbh/').cookies.get_dict()
    word_list = []
    timer = 5

    for m in range(1, 66):  # 总笔画数
        sleep(timer)
        for page_num in xrange(1, 10000):  # 页数
            url = url_base % (m, page_num)
            logger.debug(url)
            html = get_one_page(url, cookies=cookies, headers=headers)
            words = parse_words(html)
            if not words:
                break
            for word in words:
                if word not in pinyin_dict:
                    logger.debug(repr(word))
                    word_list.append(word)
            sleep(timer)

    with io.open('words.txt', 'w', encoding='utf8') as f:
        for word in word_list:
            try:
                f.write(word)
            except Exception as e:
                logger.debug(e + '\n' + repr(word))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('requests').setLevel(logging.ERROR)
    main()
