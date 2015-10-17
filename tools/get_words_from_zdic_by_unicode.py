#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""从汉典网按 unicode 编码获取汉字及发音"""

import io
import re
import sys
from time import sleep

from bs4 import BeautifulSoup
import requests

from pypinyin.pinyin_dict import pinyin_dict


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
    word_html = soup.find(id='ziip').text.encode(
        'raw_unicode_escape'
    ).decode('utf8')
    words = re.findall(ur'“([^”]+)”', word_html)
    word = words[0] if words else ''

    try:
        pinyins = [x.text for x in soup.select('td.z_i_t2_py')[0].select('a')]
        pinyins = [x.encode('raw_unicode_escape'
                            ).decode('utf8') for x in pinyins]
    except Exception as e:
        e.word = word
        raise
    return word, pinyins


def get_word(n, url_base, headers, cookies):
    url = url_base % '{0:x}'.format(n)
    print hex(n)
    try:
        html = request(url, headers, cookies)
        unicode_num, url = parse_word_url(html)
        html = request(url, headers, cookies)
        word, pinyins = parse_pinyin(html)
        # print unicode_num, repr(word), pinyins
        return unicode_num, word, pinyins
    except Exception as e:
        print e
        return '{0:x}'.format(n).upper(), getattr(e, 'word', ''), []


def get_words(unicode_range, url_base, headers, cookies):
    m = 0
    for n in xrange(int(unicode_range[0], 16), int(unicode_range[1], 16) + 1):
        if n in pinyin_dict:
            continue
        if m > 900:
            m = 0
            sleep(120)
        m += 1

        yield get_word(n, url_base, headers, cookies)
        sleep(1)


def main():
    # CJK 汉字 Unicode 编码范围
    unicode_ranges = (
        ('2E80', '2EFF'),     # CJK 部首扩展:[2E80-2EFF]
        ('2F00', '2FDF'),     # CJK 康熙部首:[2F00-2FDF]
        ('31C0', '31EF'),     # CJK 笔画:[31C0-31EF]
        ('3400', '4DBF'),     # CJK 扩展 A:[3400-4DBF]
        ('4E00', '9FFF'),     # CJK 基本:[4E00-9FFF]
        ('F900', 'FAFF'),     # CJK 兼容:[F900-FAFF]
        ('20000', '2A6DF'),   # CJK 扩展 B:[20000-2A6DF]
        ('2A700', '2B73F'),   # CJK 扩展 C:[2A700-2B73F]
        ('2B740', '2B81D'),   # CJK 扩展 D:[2B740-2B81D]
        ('2F800', '2FA1F'),   # CJK 兼容扩展:[2F800-2FA1F]
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

    for n, unicode_range in enumerate(unicode_ranges):
        filename = 'pinyins_%s-%s.txt' % unicode_range
        with io.open(filename, 'w', buffering=1, encoding='utf8') as f:
            for word_info in get_words(unicode_range, url_base,
                                       headers, cookies):
                unicode_num, word, pinyins = word_info
                if pinyins:
                    f.write(u"0x{0}: '{1}',  # {2}\n".format(unicode_num,
                                                             ','.join(pinyins),
                                                             word))
                else:
                    if word:
                        word = ' ' + word
                    f.write(u"# 0x{0}: '{1}',  #{2}\n".format(unicode_num,
                                                              '', word))


if __name__ == '__main__':
    main()
