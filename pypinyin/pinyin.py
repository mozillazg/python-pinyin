#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

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

PINYIN_STYLE =  {
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

RE_PHONETIC_SYMBOL = r'([' + re_phonetic_symbol_source + r'])'
RE_TONE2 = r'([aeoiuvnm])([0-4])$'
DEFAULT_OPTIONS = {
  'style': PINYIN_STYLE['TONE'],     # 风格
  'heteronym': False              # 多音字
}


def extend(origin, more):
    if not more:
        return origin
    obj = {}
    for k in origin:
        if k in more:
            obj[k] = more[k]
        else:
            obj[k] = origin[k]
    return obj

# /**
#  * 修改拼音词库表中的格式。
#  * @param {String} pinyin, 单个拼音。
#  * @param {PINYIN_STYLE} style, 拼音风格。
#  * @return {String}
#  */
def toFixed(pinyin, style):
    handle = None
    tone = None   # 声调
    if style ==  PINYIN_STYLE['INITIALS']:
        return initials(pinyin)
    elif style == PINYIN_STYLE['FIRST_LETTER']:
        return pinyin.charAt(0)
    elif style == PINYIN_STYLE['NORMAL']:
        def foo(matchobj):
            x = matchobj.group(0)
            y = matchobj.group(1)
            return re.sub(RE_TONE2, y, PHONETIC_SYMBOL[x])
        handle = foo
    elif style == PINYIN_STYLE['TONE2']:
        def foo(matchobj):
            x = matchobj.group(0)
            y = matchobj.group(1)
            tone = re.sub(RE_TONE2, y, PHONETIC_SYMBOL[x])
            return re.sub(RE_TONE2, '', PHONETIC_SYMBOL[x])
        handle = foo
    else:
        def foo(matchobj):
            x = matchobj.group(0)
            y = matchobj.group(1)
            return y
        handle = foo
    py = re.sub(RE_PHONETIC_SYMBOL, handle, pinyin)
    if style == PINYIN_STYLE['TONE2']:
        py += tone
    return py


# /**
#  * 单字拼音转换。
#  * @param {String} han, 单个汉字
#  * @return {Array} 返回拼音列表，多音字会有多个拼音项。
#  */
def single_pinyin(han, options):
    if not isinstance(han, basestring): return []
    options = extend(DEFAULT_OPTIONS, options)
    if len(han) != 1:
        return single_pinyin(han.charAt(0), options)
    if han not in PINYIN_DICT: return [han]
    pys = PINYIN_DICT[han].split(",")
    if not options['heteronym']:
        return [toFixed(pys[0], options['style'])]

    # 临时存储已存在的拼音，避免多音字拼音转换为非注音风格出现重复。
    py_cached = {}
    pinyins = []
    for i in pys:
       py = toFixed(i, options['style'])
       if py in py_cached: continue
       py_cached[py] = py
       pinyins.append(py)
    return pinyins


# /**
#  * 词语注音
#  * @param {String} phrases, 指定的词组。
#  * @param {Object} options, 选项。
#  * @return {Array}
#  */
def phrases_pinyin(phrases, options):
    py = []
    if phrases in PHRASES_DICT:
        py = PHRASES_DICT[phrases]
        for idx, item in enumerate(py):
            py[idx] = [toFixed(item[0], options['style'])]
    else:
        for i in phrases:
          py.append(single_pinyin(i, options))
    return py


# /**
#  * @param {String} hans 要转为拼音的目标字符串（汉字）。
#  * @param {Object} options, 可选，用于指定拼音风格，是否启用多音字。
#  * @return {Array} 返回的拼音列表。
#  */
def pinyin(hans, options={}):
    if not isinstance(hans, basestring): return []
    options = extend(DEFAULT_OPTIONS, options)
    phrases = jieba.cut(hans)
    # print "phrases:", phrases
    leng = len(hans)
    pys = []
    for i in phrases:
        words = i;
        if len(words) == 1:
            pys.append(single_pinyin(words, options))
        else:
            pys = pys + phrases_pinyin(words, options)
    return pys


# /**
#  * 声母(Initials)、韵母(Finals)。
#  * @param {String/Number/RegExp/Date/Function/Array/Object}
#  * @return {String/Number/RegExp/Date/Function/Array/Object}
#  */
def initials(pinyin):
    for i in INITIALS:
        if len(i) == 0:
            return i
    return ""

# = pinyin
STYLE_NORMAL = PINYIN_STYLE['NORMAL']
STYLE_TONE = PINYIN_STYLE['TONE']
STYLE_TONE2 = PINYIN_STYLE['TONE2']
STYLE_INITIALS = PINYIN_STYLE['INITIALS']
STYLE_FIRST_LETTER = PINYIN_STYLE['FIRST_LETTER']
