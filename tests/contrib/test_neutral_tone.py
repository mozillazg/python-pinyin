# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pypinyin import lazy_pinyin, Style
from pypinyin.contrib.neutral_tone import NeutralToneWith5Mixin
from pypinyin.contrib.uv import V2UMixin
from pypinyin.converter import DefaultConverter
from pypinyin.core import Pinyin


class MyConverter(NeutralToneWith5Mixin, DefaultConverter):
    pass


class HerConverter(NeutralToneWith5Mixin, V2UMixin, DefaultConverter):
    pass


my_pinyin = Pinyin(MyConverter())
her_pinyin = Pinyin(HerConverter())


def test_neutral_tone_with_5():
    assert lazy_pinyin('好了', style=Style.TONE2) == ['ha3o', 'le']
    assert my_pinyin.lazy_pinyin('好了', style=Style.TONE2) == ['ha3o', 'le5']
    assert her_pinyin.lazy_pinyin('好了', style=Style.TONE2) == ['ha3o', 'le5']

    assert lazy_pinyin('好了') == ['hao', 'le']
    assert my_pinyin.lazy_pinyin('好了') == ['hao', 'le']
    assert her_pinyin.lazy_pinyin('好了') == ['hao', 'le']
