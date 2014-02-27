#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""从汉典网按 unicode 编码获取汉字及发音"""

import io
import re
import sys
from time import sleep

from bs4 import BeautifulSoup
import requests


class Message(object):
    def __init__(self, file_name):
        self.f = io.open(file_name, 'w', encoding='utf8')

    def write(self, msg):
        self.f.write(u'%s\n' % msg)

    def __del__(self):
        self.f.close()

# sys.stderr = Message('error.txt')
# sys.stdout = Message('info.txt')


def request(url, headers, cookies):
    r = requests.get(url, headers=headers, cookies=cookies)
    if r.ok:
        cookies.update(r.cookies.get_dict())
        return r.text
    else:
        print >> sys.stderr, url


def parse_word_url(html):
    soup = BeautifulSoup(html)
    tag_a = soup.select('li a.usual')
    if not tag_a:
        return
    a = tag_a[0]
    unicode_num = a.select('span')[0].text
    url = u'http://www.zdic.net' + a.attrs.get('href')
    return unicode_num.strip(), url.strip()


def parse_pinyin(html):
    soup = BeautifulSoup(html)
    word_html = soup.find(id='ziip').text.encode('raw_unicode_escape').decode('utf8')
    words = re.findall(ur'“([^”]+)”', word_html)
    word = words[0] if words else ''
    try:
        pinyins = [x.text for x in soup.select('td.z_i_t2_py')[0].select('a')]
        pinyins = [x.encode('raw_unicode_escape').decode('utf8') for x in pinyins]
    except:
        pinyins = []
    return word, pinyins


def get_words(unicode_range, url_base, headers, cookies):
    for n in xrange(int(unicode_range[0], 16), int(unicode_range[1], 16) + 1):
        url = url_base % '{0:x}'.format(n)
        print n,
        html = request(url, headers, cookies)
        try:
            unicode_num, url = parse_word_url(html)
            html = request(url, headers, cookies)
            word, pinyins = parse_pinyin(html)
            print unicode_num, repr(word), pinyins
            yield unicode_num, word, pinyins
        except Exception as e:
            print e
            yield '{0:x}'.format(n).upper(), '', []
        sleep(1)


def main():
    unicode_ranges = (
        ('3400', '4DBF'),     # CJK扩展A:[3400-4DBF]
        ('4E00', '9FFF'),     # CJK基本:[4E00-9FFF]
        ('F900', 'FAFF'),     # CJK兼容:[F900-FAFF]
        ('20000', '2A6DF'),   # CJK扩展B:[20000-2A6DF]
        ('2A700', '2B73F'),   # CJK扩展C:[2A700-2B73F]
        ('2B740', '2B81D'),   # CJK扩展D:[2B740-2B81D]
        ('2F800', '2FA1F'),   # CJK兼容扩展:[2F800-2FA1F]
    )
    url_base = 'http://www.zdic.net/sousuo/ac/?q=%s&tp=tp2&lb=uno'
    headers = {
        'Host': 'www.zdic.net',
        'User-Agent': ('Mozilla/5.0 (Windows NT 6.2; rv:26.0) Gecko/20100101'
                       'Firefox/26.0'),
        'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': 1,
        'X-Requested-With': 'XMLHttpRequest',
        'X-Prototype-Version': '1.5.0',
        'Referer': 'http://www.zdic.net/',
        'Connection': 'keep-alive'
    }
    cookies = {}
    f = io.open('pinyins.txt', 'w', buffering=1, encoding='utf8')
    for unicode_range in unicode_ranges:
        for word in get_words(unicode_range, url_base, headers, cookies):
            f.write(u"'{0}': '{1}'  # {2}\n".format(word[0],','.join(word[2]),
                                                  word[1]))
    f.close()


if __name__ == '__main__':
    main()
