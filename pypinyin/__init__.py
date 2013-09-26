#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""汉语拼音转换工具."""

__title__ = 'pypinyin'
__version__ = '0.3.0'
__author__ = 'mozillazg, 闲耘 <hotoo.cn@gmail.com>'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2013 mozillazg, 闲耘 <hotoo.cn@gmail.com>'

import re
from itertools import chain
from copy import deepcopy

import jieba

from . import phrases_dict, phonetic_symbol, pinyin_dict

# 词语拼音库
PHRASES_DICT = phrases_dict.phrases_dict
# 拼音词库
PINYIN_DICT = pinyin_dict.pinyin_dict
# 声母表
INITIALS = 'zh,ch,sh,b,p,m,f,d,t,n,l,g,k,h,j,q,x,r,z,c,s,yu,y,w'.split(',')

PINYIN_STYLE = {
    'NORMAL': 0,          # 普通风格，不带声调
    'TONE': 1,            # 标准风格，声调在韵母的第一个字母上
    'TONE2': 2,           # 声调在拼音之后，使用数字 1~4 标识
    'INITIALS': 3,        # 仅保留声母部分
    'FIRST_LETTER': 4,    # 仅保留首字母
    'FINALS': 5,          # 仅保留韵母部分，不带声调
    'FINALS_TONE': 6,     # 仅保留韵母部分，带声调
    'FINALS_TONE2': 7,    # 仅保留韵母部分，声调在拼音之后，使用数字 1~4 标识
}

# 带声调字符
PHONETIC_SYMBOL = phonetic_symbol.phonetic_symbol
re_phonetic_symbol_source = ""
for k in PHONETIC_SYMBOL:
    re_phonetic_symbol_source += k
RE_PHONETIC_SYMBOL = r'[' + re.escape(re_phonetic_symbol_source) + r']'
RE_TONE2 = r'([aeoiuvnm])([0-4])$'

STYLE_NORMAL = PINYIN_STYLE['NORMAL']
STYLE_TONE = PINYIN_STYLE['TONE']
STYLE_TONE2 = PINYIN_STYLE['TONE2']
STYLE_INITIALS = PINYIN_STYLE['INITIALS']
STYLE_FINALS = PINYIN_STYLE['FINALS']
STYLE_FINALS_TONE = PINYIN_STYLE['FINALS_TONE']
STYLE_FINALS_TONE2 = PINYIN_STYLE['FINALS_TONE2']
STYLE_FIRST_LETTER = PINYIN_STYLE['FIRST_LETTER']


def initial(pinyin):
    """获取单个拼音中的声母.

    :param pinyin: 单个拼音
    :type pinyin: str
    :return: 声母
    :rtype: str
    """
    for i in INITIALS:
        if pinyin.startswith(i):
            return i
    return ''


def final(pinyin):
    """获取单个拼音中的韵母.

    :param pinyin: 单个拼音
    :type pinyin: str
    :return: 韵母
    :rtype: str
    """
    initial_ = initial(pinyin) or None
    if not initial_:
        return pinyin
    return ''.join(pinyin.split(initial_, 1))


def toFixed(pinyin, style):
    """修改拼音词库表中的格式.

    :param pinyin: 单个拼音
    :param style: 拼音风格
    """
    if style == PINYIN_STYLE['INITIALS']:
        return initial(pinyin)
    elif style in [PINYIN_STYLE['NORMAL'], PINYIN_STYLE['FIRST_LETTER'],
                   PINYIN_STYLE['FINALS']]:
        def _replace(matchobj):
            x = matchobj.group(0)
            return re.sub(RE_TONE2, r'\1', PHONETIC_SYMBOL[x])
    elif style in [PINYIN_STYLE['TONE2'], PINYIN_STYLE['FINALS_TONE2']]:
        def _replace(matchobj):
            x = matchobj.group(0)
            return PHONETIC_SYMBOL[x]
    else:
        def _replace(matchobj):
            x = matchobj.group(0)
            return x
    py = re.sub(RE_PHONETIC_SYMBOL, _replace, pinyin)

    if style == PINYIN_STYLE['FIRST_LETTER']:
        py = py[0]
    elif style in [PINYIN_STYLE['FINALS'], PINYIN_STYLE['FINALS_TONE'],
                   PINYIN_STYLE['FINALS_TONE2']]:
        py = final(py)
    return py


def single_pinyin(han, options):
    """单字拼音转换.

    :param han: 单个汉字
    :return: 返回拼音列表，多音字会有多个拼音项
    """
    if not isinstance(han, basestring):
        return []
    if len(han) != 1:
        return single_pinyin(han[0], options)
    if han not in PINYIN_DICT:
        return [han]
    pys = PINYIN_DICT[han].split(",")
    if not options['heteronym']:
        return [toFixed(pys[0], options['style'])]

    # 临时存储已存在的拼音，避免多音字拼音转换为非注音风格出现重复。
    py_cached = {}
    pinyins = []
    for i in pys:
        py = toFixed(i, options['style'])
        if py in py_cached:
            continue
        py_cached[py] = py
        pinyins.append(py)
    return pinyins


def phrases_pinyin(phrases, options):
    """词语拼音转换.

    :param phrases: 词语
    :return: 拼音列表
    """
    py = []
    if phrases in PHRASES_DICT:
        py = deepcopy(PHRASES_DICT[phrases])
        for idx, item in enumerate(py):
            py[idx] = [toFixed(item[0], options['style'])]
    else:
        for i in phrases:
            py.append(single_pinyin(i, options))
    return py


def pinyin(hans, style=STYLE_TONE, heteronym=False):
    u"""将汉字转换为拼音.

    :param hans: 汉字
    :type hans: unicode
    :param style: 指定拼音风格
    :param heteronym: 是否启用多音字
    :return: 拼音列表
    :rtype: list

    Usage::

      >>> from pypinyin import pinyin
      >>> import pypinyin
      >>> pinyin(u'中心')
      [[u'zh\u014dng'], [u'x\u012bn']]
      >>> pinyin(u'中心', heteronym=True)  # 启用多音字模式
      [[u'zh\u014dng', u'zh\xf2ng'], [u'x\u012bn']]
      >>> pinyin(u'中心', pypinyin.STYLE_INITIALS)  # 设置拼音风格
      [['zh'], ['x']]

    """
    if not isinstance(hans, basestring):
        return []
    options = {'style': style, 'heteronym': heteronym}
    phrases = jieba.cut(hans)
    pys = []
    for words in phrases:
        # 不处理非中文字符
        if not re.match(ur'^[\u4e00-\u9fff]+$', words):
            pys.append([words])
            continue
        if len(words) == 1:
            pys.append(single_pinyin(words, options))
        else:
            pys = pys + phrases_pinyin(words, options)
    return pys


def slug(hans, style=STYLE_NORMAL, heteronym=False, separator='-'):
    u"""生成 slug 字符串.

    :param hans: 汉字
    :type hans: unicode
    :param style: 指定拼音风格
    :param heteronym: 是否启用多音字
    :param separstor: 两个拼音间的分隔符/连接符
    :return: slug 字符串.
    """
    return separator.join(chain(*pinyin(hans, style, heteronym)))
