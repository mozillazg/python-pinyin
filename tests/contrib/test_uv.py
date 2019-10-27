# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pypinyin import lazy_pinyin
from pypinyin.contrib.uv import V2UMixin
from pypinyin.converter import DefaultConverter
from pypinyin.core import Pinyin


class MyConverter(V2UMixin, DefaultConverter):
    pass


my_pinyin = Pinyin(MyConverter())


def test_v2u():
    assert lazy_pinyin('战略') == ['zhan', 'lve']
    assert my_pinyin.lazy_pinyin('战略') == ['zhan', 'lüe']
