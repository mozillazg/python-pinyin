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
    if has_module('jieba'):
        assert pinyin(hans + 'abc') == [['zh\u014dng'], ['x\u012bn'], ['abc']]
    else:
        assert pinyin(hans + 'abc') == [['zh\u014dng'], ['x\u012bn'],
                                        ['a'], ['b'], ['c']]
    # 中英文混合的固定词组
    assert pinyin('黄山B股', style=TONE2) == [['hua2ng'], ['sha1n'], ['B'], ['gu3']]
    assert pinyin('A股', style=TONE2) == [['A'], ['gu3']]
    assert pinyin('阿Q', style=TONE2) == [['a1'], ['Q']]
    assert pinyin('B超', style=TONE2) == [['B'], ['cha1o']]
    assert pinyin('AB超C', style=TONE2) == [['A'], ['B'], ['cha1o'], ['C']]
    if has_module('jieba'):
        assert pinyin('AB阿C', style=TONE2) == [['AB'], ['a1'], ['C']]
    else:
        assert pinyin('AB阿C', style=TONE2) == [['A'], ['B'], ['a1'], ['C']]
    assert pinyin('维生素C', style=TONE2) == [['we2i'], ['she1ng'], ['su4'], ['C']]


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


def has_module(module):
    try:
        __import__(module)
        return True
    except ImportError:
        pass


@pytest.mark.skipif(not has_module('jieba'), reason='cant import jieba')
def test_seg_jieba():
    hans = '音乐'
    import jieba
    hans_seg = list(jieba.cut(hans))
    assert pinyin(hans_seg, style=TONE2) == [['yi1n'], ['yue4']]
    # 中英文混合的固定词组
    assert pinyin('黄山B股', style=TONE2) == [['hua2ng'], ['sha1n'], ['B'], ['gu3']]
    assert pinyin('A股', style=TONE2) == [['A'], ['gu3']]
    assert pinyin('阿Q', style=TONE2) == [['a1'], ['Q']]
    assert pinyin('B超', style=TONE2) == [['B'], ['cha1o']]
    assert pinyin('AB超C', style=TONE2) == [['A'], ['B'], ['cha1o'], ['C']]
    assert pinyin('AB阿C', style=TONE2) == [['AB'], ['a1'], ['C']]
    assert pinyin('维生素C', style=TONE2) == [['we2i'], ['she1ng'], ['su4'], ['C']]


@pytest.mark.skipif(not has_module('snownlp'), reason='cant import snownlp')
def test_other_seg_module():
    hans = '音乐123'
    assert lazy_pinyin(hans, style=TONE2) == [u'yi1n', u'le4', u'1', u'2', u'3']
    from snownlp import SnowNLP
    hans_seg = SnowNLP(hans).words
    assert lazy_pinyin(hans_seg, style=TONE2) == [u'yi1n', u'yue4', u'123']


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


def test_update():
    data = {
        '便宜': 'pia2n yi2',
        '便宜从事': 'bia4n yi2 co2ng shi4',
        '便宜施行': 'bia4n yi2 shi1 xi2ng',
        '便宜货': 'pia2n yi2 huo4',
        '贪便宜': 'ta1n pia2n yi2',
        '讨便宜': 'ta3o pia2n yi2',
        '小便宜': 'xia3o pia2n yi2',
        '占便宜': 'zha4n pia2n yi2',
    }
    for h, p in data.items():
        assert slug([h], style=TONE2, separator=' ') == p
