#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
INITIALS = "zh,ch,sh,b,p,m,f,d,t,n,l,g,k,h,j,q,x,r,z,c,s,yu,y,w".split(",")
# 韵母表
FINALS = "ang,eng,ing,ong,an,en,in,un,er,ai,ei,ui,ao,ou,iu,ie,ve,a,o,e,i,u,v"
FINALS = FINALS.split(",")

PINYIN_STYLE = {
    'NORMAL': 0,        # 普通风格，不带音标
    'TONE': 1,          # 标准风格，音标在韵母的第一个字母上
    'TONE2': 2,         # 声调中拼音之后，使用数字 1~4 标识
    'INITIALS': 3,      # 仅需要声母部分
    'FIRST_LETTER': 4   # 仅保留首字母
}

# 带音标字符
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
STYLE_FIRST_LETTER = PINYIN_STYLE['FIRST_LETTER']


def initials(pinyin):
    """只显示声母.

    :param pinyin: 拼音
    :type pinyin: str
    :return: 声母
    :rtype: str
    """
    for i in INITIALS:
        if pinyin.startswith(i):
            return i
    return ""


def toFixed(pinyin, style):
    """修改拼音词库表中的格式.

    :param pinyin: 单个拼音
    :param style: 拼音风格
    """
    if style == PINYIN_STYLE['INITIALS']:
        return initials(pinyin)
    elif style == PINYIN_STYLE['FIRST_LETTER']:
        return pinyin[0]
    elif style == PINYIN_STYLE['NORMAL']:
        def _replace(matchobj):
            x = matchobj.group(0)
            return re.sub(RE_TONE2, r'\1', PHONETIC_SYMBOL[x])
    elif style == PINYIN_STYLE['TONE2']:
        def _replace(matchobj):
            x = matchobj.group(0)
            return PHONETIC_SYMBOL[x]
    else:
        def _replace(matchobj):
            x = matchobj.group(0)
            return x
    py = re.sub(RE_PHONETIC_SYMBOL, _replace, pinyin)
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
    """将汉字转换为拼音.

    :param hans: 汉字
    :type hans: unicode
    :param style: 指定拼音风格
    :param heteronym: 是否启用多音字
    :return: 拼音列表
    :rtype: list
    """
    if not isinstance(hans, basestring):
        return []
    options = {'style': style, 'heteronym': heteronym}
    phrases = jieba.cut(hans)
    pys = []
    for i in phrases:
        words = i
        if len(words) == 1:
            pys.append(single_pinyin(words, options))
        else:
            pys = pys + phrases_pinyin(words, options)
    return pys


def slug(hans, style=STYLE_NORMAL, heteronym=False,
         separator='-'):
    """生成 slug 字符串.

    :param hans: 汉字
    :type hans: unicode
    :param style: 指定拼音风格
    :param heteronym: 是否启用多音字
    :param separstor: 两个拼音间的分隔符/连接符
    :return: slug 字符串.
    """
    return separator.join(chain(*pinyin(hans, style, heteronym)))
