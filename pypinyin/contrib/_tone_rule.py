# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
标调位置

    有 ɑ 不放过，

　　没 ɑ 找 o、e；

　　ɑ、o、e、i、u、ü

　　标调就按这顺序；

　　i、u 若是连在一起，

　　谁在后面就标谁。

http://www.hwjyw.com/resource/content/2010/06/04/8183.shtml
https://www.zhihu.com/question/23655297
https://github.com/mozillazg/python-pinyin/issues/160
http://www.pinyin.info/rules/where.html
"""


def right_mark_index(pinyin_no_number):
    # 有 ɑ 不放过, 没 ɑ 找 o、e
    for c in ['a', 'o', 'e']:
        if c in pinyin_no_number:
            return pinyin_no_number.index(c)

    # i、u 若是连在一起，谁在后面就标谁
    for c in ['iu', 'ui']:
        if c in pinyin_no_number:
            return pinyin_no_number.index(c) + 1

    # ɑ、o、e、i、u、ü
    for c in ['i', 'u', 'v', 'ü']:
        if c in pinyin_no_number:
            return pinyin_no_number.index(c)

    # n, m, ê
    for c in ['n', 'm', 'ê']:
        if c in pinyin_no_number:
            return pinyin_no_number.index(c)
