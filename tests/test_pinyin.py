#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pypinyin import pinyin, slug
from pypinyin import STYLE_NORMAL, STYLE_TONE, STYLE_TONE2, STYLE_INITIALS
from pypinyin import STYLE_FIRST_LETTER, STYLE_FINALS, STYLE_FINALS_TONE
from pypinyin import STYLE_FINALS_TONE2


def test_pinyin_initials():
    """包含声明和韵母的词语"""
    hans = u'中心'
    # 默认风格，带声调
    assert pinyin(hans) == [[u'zh\u014dng'], [u'x\u012bn']]
    # 普通风格，不带声调
    assert pinyin(hans, STYLE_NORMAL) == [[u'zhong'], [u'xin']]
    # 声调风格，拼音声调在韵母第一个字母上
    assert pinyin(hans, STYLE_TONE) == [[u'zh\u014dng'], [u'x\u012bn']]
    # 声调风格2，即拼音声调在各个拼音之后，用数字 [0-4] 进行表示
    assert pinyin(hans, STYLE_TONE2) == [[u'zho1ng'], [u'xi1n']]
    # 声母风格，只返回各个拼音的声母部分
    assert pinyin(hans, STYLE_INITIALS) == [['zh'], ['x']]
    # 首字母风格，只返回拼音的首字母部分
    assert pinyin(hans, STYLE_FIRST_LETTER) == [[u'z'], [u'x']]
    # 启用多音字模式
    assert pinyin(hans, heteronym=True) == [[u'zh\u014dng', u'zh\xf2ng'],
                                            [u'x\u012bn']]
    # 韵母风格1，只返回各个拼音的韵母部分，不带声调
    assert pinyin(hans, style=STYLE_FINALS) == [['ong'], ['in']]
    # 韵母风格2，带声调，声调在韵母第一个字母上
    assert pinyin(hans, style=STYLE_FINALS_TONE) == [[u'\u014dng'],
                                                     [u'\u012bn']]
    # 韵母风格2，带声调，声调在各个拼音之后，用数字 [0-4] 进行表示
    assert pinyin(hans, style=STYLE_FINALS_TONE2) == [[u'o1ng'], [u'i1n']]


def test_pinyin_finals():
    """只包含韵母的词语"""
    hans = u'嗷嗷'
    assert pinyin(hans) == [[u'\xe1o'], [u'\xe1o']]
    assert pinyin(hans + 'abc') == [[u'\xe1o'], [u'\xe1o'], [u'abc']]
    assert pinyin(hans, STYLE_NORMAL) == [[u'ao'], [u'ao']]
    assert pinyin(hans, STYLE_TONE) == [[u'\xe1o'], [u'\xe1o']]
    assert pinyin(hans, STYLE_TONE2) == [[u'a2o'], [u'a2o']]
    assert pinyin(hans, STYLE_INITIALS) == [[''], ['']]
    assert pinyin(hans, STYLE_FIRST_LETTER) == [[u'a'], [u'a']]
    assert pinyin(hans, heteronym=True) == [[u'\xe1o'], [u'\xe1o']]
    assert pinyin(u'啊', heteronym=True) == [[u'\u0101', u'\xe1',
                                              u'\u01ce', u'\xe0', u'a']]
    assert pinyin(hans, style=STYLE_FINALS) == [['ao'], ['ao']]
    assert pinyin(hans, style=STYLE_FINALS_TONE) == [[u'\xe1o'], [u'\xe1o']]
    assert pinyin(hans, style=STYLE_FINALS_TONE2) == [[u'a2o'], [u'a2o']]


def test_slug():
    hans = u'中心'
    assert slug(hans) == 'zhong-xin'
    assert slug(hans, heteronym=True) == 'zhong-xin'


def test_zh_and_en():
    """中英文混合的情况"""
    # 中英文
    hans = u'中心'
    assert pinyin(hans + 'abc') == [[u'zh\u014dng'], [u'x\u012bn'], ['abc']]


def test_others():
    # 非字符串
    assert pinyin(1) == []
    # 空字符串
    assert pinyin('') == []
    # 单个汉字
    assert pinyin(u'營') == [[u'y\xedng']]
    # 中国 人
    assert pinyin(u'中国人') == [[u'zh\u014dng'], [u'gu\xf3'], [u'r\xe9n']]
    # 日文
    assert pinyin(u'の') == [[u'\u306e']]
    # 没有读音的汉字，还不存在的汉字
    assert pinyin(u'\u9fff') == [[u'\u9fff']]
