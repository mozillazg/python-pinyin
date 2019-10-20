# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pytest import mark

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


@mark.parametrize('input,expected_old, expected_new', [
    ['你好', ['ni3', 'ha3o'], ['ni3', 'ha3o']],
    ['男孩儿', ['na2n', 'ha2i', 'er'], ['na2n', 'ha2i', 'e5r']],
    ['我们', ['wo3', 'men'], ['wo3', 'me5n']],
    ['衣裳', ['yi1', 'shang'], ['yi1', 'sha5ng']],
    ['好吧', ['ha3o', 'ba'], ['ha3o', 'ba5']],
])
def test_neutral_tone_with_5_many_cases(input, expected_old, expected_new):
    assert lazy_pinyin(input, style=Style.TONE2) == expected_old
    assert my_pinyin.lazy_pinyin(input, style=Style.TONE2) == expected_new
