#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pypinyin import *   # noqa
from pypinyin import simple_seg


def test_import_all():
    pinyin('啦啦啦')
    pinyin('啦啦啦', TONE2)
    lazy_pinyin('啦啦啦')
    slug('啦啦啦')


def test_simple_seg():
    assert simple_seg('啦啦') == ['啦啦']
    assert simple_seg('啦啦abc') == ['啦啦', 'abc']
    assert simple_seg('&##啦啦abc') == ['&##', '啦啦', 'abc']
    assert simple_seg('&#哦#啦啦abc') == ['&#', '哦', '#', '啦啦', 'abc']
    assert simple_seg('哦ほ#') == ['哦', 'ほ#']
    assert simple_seg(['啦啦']) == ['啦啦']
    assert simple_seg(['啦啦', 'abc']) == ['啦啦', 'abc']
    assert simple_seg('哦ほ#哪') == ['哦', 'ほ#', '哪']
    assert simple_seg('哦ほ#哪#') == ['哦', 'ほ#', '哪', '#']
    assert simple_seg('啊 --') == ['啊', ' --']
    assert simple_seg('啊 -- ') == ['啊', ' -- ']
    assert simple_seg('啊 -- 那') == ['啊', ' -- ', '那']
