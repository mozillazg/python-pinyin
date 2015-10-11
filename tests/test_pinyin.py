#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pytest

from pypinyin import (
    pinyin, slug, lazy_pinyin, load_single_dict,
    load_phrases_dict, NORMAL, TONE, TONE2, INITIALS,
    FIRST_LETTER, FINALS, FINALS_TONE, FINALS_TONE2
)
from .utils import has_module


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
    assert pinyin(hans + 'abc') == [['\xe1o'], ['\xe1o'], ['abc']]
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
    assert pinyin(hans + 'abc') == [['zh\u014dng'], ['x\u012bn'], ['abc']]
    # 中英文混合的固定词组
    assert pinyin('黄山B股', style=TONE2) == [['hua2ng'], ['sha1n'], ['B'], ['gu3']]
    assert pinyin('A股', style=TONE2) == [['A'], ['gu3']]
    assert pinyin('阿Q', style=TONE2) == [['a1'], ['Q']]
    assert pinyin('B超', style=TONE2) == [['B'], ['cha1o']]
    assert pinyin('AB超C', style=TONE2) == [['AB'], ['cha1o'], ['C']]
    assert pinyin('AB阿C', style=TONE2) == [['AB'], ['a1'], ['C']]
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
    assert pinyin('AB超C', style=TONE2) == [['AB'], ['cha1o'], ['C']]
    assert pinyin('AB阿C', style=TONE2) == [['AB'], ['a1'], ['C']]
    assert pinyin('维生素C', style=TONE2) == [['we2i'], ['she1ng'], ['su4'], ['C']]


@pytest.mark.skipif(not has_module('snownlp'), reason='cant import snownlp')
def test_other_seg_module():
    from snownlp import SnowNLP
    hans = '音乐123'
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


def test_errors_callable():
    def foobar(chars):
        return 'a' * len(chars)

    class Foobar(object):
        def __call__(self, chars):
            return 'a' * len(chars)

    n = 5
    assert lazy_pinyin('あ' * n, errors=foobar) == ['a' * n]
    assert lazy_pinyin('あ' * n, errors=Foobar()) == ['a' * n]


def test_simple_seg():
    data = {
        '北京abcc': 'be3i ji1ng abcc',
        '你好にほんごРусский язык': 'ni3 ha3o にほんごРусский язык',
    }
    for h, p in data.items():
        assert slug([h], style=TONE2, separator=' ') == p

    hans = '你好にほんごРусский язык'
    ret = 'ni3 ha3o'
    errors = lambda x: None
    assert slug(hans, style=TONE2, separator=' ', errors=errors) == ret


data_for_update = [
    # 便宜的发音
    [
        ['便宜'], {'style': TONE2}, ['pia2n', 'yi2']
    ],
    [
        ['便宜从事'], {'style': TONE2}, ['bia4n', 'yi2', 'co2ng', 'shi4']
    ],
    [
        ['便宜施行'], {'style': TONE2}, ['bia4n', 'yi2', 'shi1', 'xi2ng']
    ],
    [
        ['便宜货'], {'style': TONE2}, ['pia2n', 'yi2', 'huo4']
    ],
    [
        ['贪便宜'], {'style': TONE2}, ['ta1n', 'pia2n', 'yi2']
    ],
    [
        ['讨便宜'], {'style': TONE2}, ['ta3o', 'pia2n', 'yi2']
    ],
    [
        ['小便宜'], {'style': TONE2}, ['xia3o', 'pia2n', 'yi2']
    ],
    [
        ['占便宜'], {'style': TONE2}, ['zha4n', 'pia2n', 'yi2']
    ],
    #
    [
        '\u3400', {'style': TONE2}, ['qiu1'],  # CJK 扩展 A:[3400-4DBF]
    ],
    [
        '\u4E00', {'style': TONE2}, ['yi1'],   # CJK 基本:[4E00-9FFF]
    ],
    [
        '\uFA29', {'style': TONE2}, ['da3o'],  # CJK 兼容:[F900-FAFF]
    ],
    # 误把 yu 放到声母列表了
    ['鱼', {'style': TONE2}, ['yu2']],
    ['鱼', {'style': FINALS}, ['v']],
    ['雨', {'style': TONE2}, ['yu3']],
    ['雨', {'style': FINALS}, ['v']],
    ['元', {'style': TONE2}, ['yua2n']],
    ['元', {'style': FINALS}, ['van']],
    # y, w 也不是拼音, yu的韵母是v, yi的韵母是i, wu的韵母是u
    ['呀', {'style': INITIALS}, ['']],
    ['呀', {'style': TONE2}, ['ya1']],
    ['呀', {'style': FINALS}, ['ia']],
    ['无', {'style': INITIALS}, ['']],
    ['无', {'style': TONE2}, ['wu2']],
    ['无', {'style': FINALS}, ['u']],
    ['衣', {'style': TONE2}, ['yi1']],
    ['衣', {'style': FINALS}, ['i']],
    ['万', {'style': TONE2}, ['wa4n']],
    ['万', {'style': FINALS}, ['uan']],
    # ju, qu, xu 的韵母应该是 v
    ['具', {'style': FINALS_TONE}, ['ǜ']],
    ['具', {'style': FINALS_TONE2}, ['v4']],
    ['具', {'style': FINALS}, ['v']],
    ['取', {'style': FINALS_TONE}, ['ǚ']],
    ['取', {'style': FINALS_TONE2}, ['v3']],
    ['取', {'style': FINALS}, ['v']],
    ['徐', {'style': FINALS_TONE}, ['ǘ']],
    ['徐', {'style': FINALS_TONE2}, ['v2']],
    ['徐', {'style': FINALS}, ['v']],

]


@pytest.mark.parametrize('hans, kwargs,result', data_for_update)
def test_update(hans, kwargs, result):
    assert lazy_pinyin(hans, **kwargs) == result
