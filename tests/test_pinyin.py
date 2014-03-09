#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pytest

from pypinyin import (pinyin, slug, lazy_pinyin, load_single_dict,
                      load_phrases_dict, NORMAL, TONE, TONE2, INITIALS,
                      FIRST_LETTER, FINALS, FINALS_TONE, FINALS_TONE2)


def test_pinyin_initials():
    """包含声明和韵母的词语"""
    hans = '中心'
    # 默认风格，带声调
    assert pinyin(hans) == [['zh\u014dng'], ['x\u012bn']]
    # 普通风格，不带声调
    assert pinyin(hans, NORMAL) == [['zhong'], ['xin']]
    # 声调风格，拼音声调在韵母第一个字母上
    assert pinyin(hans, TONE) == [['zh\u014dng'], ['x\u012bn']]
    # 声调风格2，即拼音声调在各个拼音之后，用数字 [0-4] 进行表示
    assert pinyin(hans, TONE2) == [['zho1ng'], ['xi1n']]
    # 声母风格，只返回各个拼音的声母部分
    assert pinyin(hans, INITIALS) == [['zh'], ['x']]
    # 首字母风格，只返回拼音的首字母部分
    assert pinyin(hans, FIRST_LETTER) == [['z'], ['x']]
    # 启用多音字模式
    assert pinyin(hans, heteronym=True) == [['zh\u014dng', 'zh\xf2ng'],
                                            ['x\u012bn']]
    # 韵母风格1，只返回各个拼音的韵母部分，不带声调
    assert pinyin(hans, style=FINALS) == [['ong'], ['in']]
    # 韵母风格2，带声调，声调在韵母第一个字母上
    assert pinyin(hans, style=FINALS_TONE) == [['\u014dng'], ['\u012bn']]
    # 韵母风格2，带声调，声调在各个拼音之后，用数字 [0-4] 进行表示
    assert pinyin(hans, style=FINALS_TONE2) == [['o1ng'], ['i1n']]


def test_pinyin_finals():
    """只包含韵母的词语"""
    hans = '嗷嗷'
    assert pinyin(hans) == [['\xe1o'], ['\xe1o']]
    try:
        assert pinyin(hans + 'abc') == [['\xe1o'], ['\xe1o'], ['abc']]
    except AssertionError:
        assert pinyin(hans + 'abc') == [['\xe1o'], ['\xe1o'],
                                        ['a'], ['b'], ['c']]
    assert pinyin(hans, NORMAL) == [['ao'], ['ao']]
    assert pinyin(hans, TONE) == [['\xe1o'], ['\xe1o']]
    assert pinyin(hans, TONE2) == [['a2o'], ['a2o']]
    assert pinyin(hans, INITIALS) == [[''], ['']]
    assert pinyin(hans, FIRST_LETTER) == [['a'], ['a']]
    assert pinyin(hans, heteronym=True) == [['\xe1o'], ['\xe1o']]
    assert pinyin('啊', heteronym=True) == [['\u0101', '\xe1',
                                              '\u01ce', '\xe0', 'a']]
    assert pinyin(hans, style=FINALS) == [['ao'], ['ao']]
    assert pinyin(hans, style=FINALS_TONE) == [['\xe1o'], ['\xe1o']]
    assert pinyin(hans, style=FINALS_TONE2) == [['a2o'], ['a2o']]


def test_slug():
    hans = '中心'
    assert slug(hans) == 'zhong-xin'
    assert slug(hans, heteronym=True) == 'zhong-xin'


def test_zh_and_en():
    """中英文混合的情况"""
    # 中英文
    hans = '中心'
    try:
        assert pinyin(hans + 'abc') == [['zh\u014dng'], ['x\u012bn'], ['abc']]
    except AssertionError:
        assert pinyin(hans + 'abc') == [['zh\u014dng'], ['x\u012bn'],
                                        ['a'], ['b'], ['c']]


def test_others():
    # 空字符串
    assert pinyin('') == []
    # 单个汉字
    assert pinyin('營') == [['y\xedng']]
    # 中国 人
    assert pinyin('中国人') == [['zh\u014dng'], ['gu\xf3'], ['r\xe9n']]
    # 日文
    assert pinyin('の') == [['\u306e']]
    # 没有读音的汉字，还不存在的汉字
    assert pinyin('\u9fff') == [['\u9fff']]


def test_lazy_pinyin():
    assert lazy_pinyin('中国人') == ['zhong', 'guo', 'ren']
    assert lazy_pinyin('中心') == ['zhong', 'xin']
    assert lazy_pinyin('中心', style=TONE) == ['zh\u014dng', 'x\u012bn']
    assert lazy_pinyin('中心', style=INITIALS) == ['zh', 'x']


def has_jieba():
    try:
        __import__('jieba')
        return True
    except ImportError:
        pass


@pytest.mark.skipif(not has_jieba(), reason='cant import jieba')
def test_seg():
    hans = '音乐'
    import jieba
    hans_seg = list(jieba.cut(hans))
    # assert pinyin(hans, style=TONE2) == [['yi1n'], ['le4']]
    assert pinyin(hans_seg, style=TONE2) == [['yi1n'], ['yue4']]


def test_custom_pinyin_dict():
    hans = '桔'
    try:
        assert lazy_pinyin(hans, style=TONE2) == ['ju2']
    except AssertionError:
        pass
    load_single_dict({ord('桔'): 'jú,jié'})
    assert lazy_pinyin(hans, style=TONE2) == ['ju2']


def test_custom_pinyin_dict2():
    hans = ['同行']
    try:
        assert lazy_pinyin(hans, style=TONE2) == ['to2ng', 'ha2ng']
    except AssertionError:
        pass
    load_phrases_dict({'同行': [['tóng'], ['xíng']]})
    assert lazy_pinyin(hans, style=TONE2) == ['to2ng', 'xi2ng']


def test_errors():
    hans = (
        ('啊', {'style': TONE2}, ['a1']),
        ('啊a', {'style': TONE2}, ['a1', 'a']),
        ('⺁', {'style': TONE2}, ['\u2e81']),
        ('⺁', {'style': TONE2, 'errors': 'ignore'}, []),
        ('⺁', {'style': TONE2, 'errors': 'replace'}, ['2e81']),
        ('鿅', {'style': TONE2}, ['\u9fc5']),
        ('鿅', {'style': TONE2, 'errors': 'ignore'}, []),
        ('鿅', {'style': TONE2, 'errors': 'replace'}, ['9fc5']),
    )
    for han in hans:
        assert lazy_pinyin(han[0], **han[1]) == han[2]
