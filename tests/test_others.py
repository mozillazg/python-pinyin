#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pytest import mark

from pypinyin import pinyin, Style, lazy_pinyin, slug
from pypinyin.seg.simpleseg import simple_seg


def test_import_all():
    pinyin('啦啦啦')         # noqa
    pinyin('啦啦啦', Style.TONE2)  # noqa
    lazy_pinyin('啦啦啦')    # noqa
    slug('啦啦啦')           # noqa


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
    assert simple_seg('你好啊 --') == ['你好啊', ' --']
    assert simple_seg('啊 -- ') == ['啊', ' -- ']
    assert simple_seg('你好啊 -- 那') == ['你好啊', ' -- ', '那']
    assert simple_seg('啊 -- 你好那 ') == ['啊', ' -- ', '你好那', ' ']
    assert simple_seg('a 你好啊 -- 那 ') == ['a ', '你好啊', ' -- ', '那', ' ']
    assert simple_seg('a啊 -- 你好那 ') == ['a', '啊', ' -- ', '你好那', ' ']


def test_issue_205():
    assert pinyin('金融行业', Style.FIRST_LETTER)[2] == ['h']
    assert pinyin('军工行业', Style.FIRST_LETTER)[2] == ['h']
    assert pinyin('浦发银行', Style.FIRST_LETTER)[3] == ['h']
    assert pinyin('交通银行', Style.FIRST_LETTER)[3] == ['h']


def test_issue_266():
    assert lazy_pinyin('哟', style=Style.FINALS) == ['o']
    assert lazy_pinyin('哟', style=Style.FINALS, strict=False) == ['o']

    assert lazy_pinyin('嗯', style=Style.FINALS) == ['']
    assert lazy_pinyin('嗯', style=Style.FINALS, strict=False) == ['n']

    assert lazy_pinyin('呣', style=Style.FINALS) == ['']
    assert lazy_pinyin('呣', style=Style.FINALS, strict=False) == ['m']


def test_issue_311():
    assert lazy_pinyin('大城', style=Style.TONE2) == ['da4', 'che2ng']
    assert lazy_pinyin('大城市', style=Style.TONE2) == ['da4', 'che2ng', 'shi4']
    assert lazy_pinyin('大城区', style=Style.TONE2) == ['da4', 'che2ng', 'qu1']


@mark.parametrize('neutral_tone_with_five', [True, False])
def test_issue_284(neutral_tone_with_five):
    assert lazy_pinyin('嗯', style=Style.FINALS_TONE3,
                       neutral_tone_with_five=neutral_tone_with_five) == ['']
    assert lazy_pinyin('呣', style=Style.FINALS_TONE3,
                       neutral_tone_with_five=neutral_tone_with_five) == ['']
    assert lazy_pinyin('嗯', style=Style.FINALS,
                       neutral_tone_with_five=neutral_tone_with_five) == ['']
    assert lazy_pinyin('呣', style=Style.FINALS,
                       neutral_tone_with_five=neutral_tone_with_five) == ['']
    assert lazy_pinyin('嗯', style=Style.INITIALS,
                       neutral_tone_with_five=neutral_tone_with_five) == ['']
    assert lazy_pinyin('呣', style=Style.INITIALS,
                       neutral_tone_with_five=neutral_tone_with_five) == ['']


def test_finals_syllabic_ng_keeps_n():
    # 嗯 等字的 ńg/ňg/ǹg 读音在非严格模式下，韵母应是完整的 ``ng``，
    # 而不是把声母 n 切掉后剩下的无效韵母 ``g``。
    finals = pinyin('嗯', style=Style.FINALS, heteronym=True, strict=False)[0]
    assert 'ng' in finals
    assert 'g' not in finals

    tone3 = pinyin('嗯', style=Style.FINALS_TONE3, heteronym=True,
                   strict=False)[0]
    assert 'ng2' in tone3 and 'ng3' in tone3 and 'ng4' in tone3
    assert 'g2' not in tone3

    # 严格模式（默认）下没有韵母的设计保持不变。
    assert pinyin('嗯', style=Style.FINALS, heteronym=True) == [['']]


if __name__ == '__main__':
    import pytest
    pytest.cmdline.main()
