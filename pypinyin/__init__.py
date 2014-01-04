#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""汉语拼音转换工具."""

from __future__ import unicode_literals

__title__ = 'pypinyin'
__version__ = '0.4.1'
__author__ = 'mozillazg, 闲耘'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2014 mozillazg, 闲耘'
__all__ = ['pinyin', 'lazy_pinyin', 'slug', 'STYLE_NORMAL', 'STYLE_TONE',
           'STYLE_TONE2', 'STYLE_INITIALS', 'STYLE_FINALS',
           'STYLE_FINALS_TONE', 'STYLE_FINALS_TONE2',
           'STYLE_FIRST_LETTER']

import re
from itertools import chain
from copy import deepcopy

from . import phrases_dict, phonetic_symbol, pinyin_dict

try:
    unicode        # python 2
except NameError:
    unicode = str  # python 3

# 词语拼音库
PHRASES_DICT = phrases_dict.phrases_dict
# 单字拼音库
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


def load_single_dict(pinyin_dict):
    """载入用户自定义的单字拼音库

    :param pinyin_dict: 单字拼音库。比如： {u"阿": u"ā,ē"}
    :type pinyin_dict: dict

    """
    PINYIN_DICT.update(pinyin_dict)



def load_phrases_dict(phrases_dict):
    """载入用户自定义的词语拼音库

    :param phrases_dict: 词语拼音库。比如： {u"阿爸": [[u"ā"], [u"bà"]]}
    :type phrases_dict: dict

    """
    PHRASES_DICT.update(phrases_dict)


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
    if han not in PINYIN_DICT:
        return [han]
    pys = PINYIN_DICT[han].split(",")
    if not options['heteronym']:
        return [toFixed(pys[0], options['style'])]

    # 临时存储已存在的拼音，避免多音字拼音转换为非音标风格出现重复。
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

    :param hans: 汉字字符串(u'你好吗')或列表([u'你好', u'吗'])
                 如果用户安装了 jieba，将使用 jieba 对字符串进行分词处理。
                 用户也可以使用自己喜爱的分词模块对字符串进行分词处理。
                 只需将进行过分词处理的字符串列表传进来就可以了。
    :type hans: unicode 字符串或字符串列表
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
      >>> pinyin(u'中心', style=pypinyin.STYLE_INITIALS)  # 设置拼音风格
      [[u'zh'], [u'x']]
      >>> pinyin(u'中心', style=pypinyin.STYLE_TONE2)
      [[u'zho1ng'], [u'xi1n']]

    """
    options = {'style': style, 'heteronym': heteronym}
    if isinstance(hans, unicode):
        try:
            import jieba
            hans = jieba.cut(hans)
        except ImportError:
            pass
    pys = []
    for words in hans:
        # 不处理非中文字符
        if not re.match(r'^[\u4e00-\u9fff]+$', words):
            pys.append([words])
            continue
        if len(words) == 1:
            pys.append(single_pinyin(words, options))
        else:
            pys.extend(phrases_pinyin(words, options))
    return pys


def slug(hans, style=STYLE_NORMAL, heteronym=False, separator='-'):
    """生成 slug 字符串.

    :param hans: 汉字
    :type hans: unicode or list
    :param style: 指定拼音风格
    :param heteronym: 是否启用多音字
    :param separstor: 两个拼音间的分隔符/连接符
    :return: slug 字符串.
    """
    return separator.join(chain(*pinyin(hans, style, heteronym)))


def lazy_pinyin(hans, style=STYLE_NORMAL):
    """不包含多音字的拼音列表.

    与 :py:func:`~pypinyin.pinyin` 的区别是返回的拼音是个字符串，并且每个字只包含一个读音.

    :param hans: 汉字
    :type hans: unicode or list
    :param style: 指定拼音风格
    :return: 拼音列表(e.g. ``['zhong', 'guo', 'ren']``)
    :rtype: list

    Usage::

      >>> from pypinyin import lazy_pinyin
      >>> import pypinyin
      >>> lazy_pinyin(u'中心')
      [u'zhong', u'xin']
      >>> lazy_pinyin(u'中心', style=pypinyin.STYLE_TONE)
      [u'zh\u014dng', u'x\u012bn']
      >>> lazy_pinyin(u'中心', style=pypinyin.STYLE_INITIALS)
      [u'zh', u'x']
      >>> lazy_pinyin(u'中心', style=pypinyin.STYLE_TONE2)
      [u'zho1ng', u'xi1n']
    """
    return list(chain(*pinyin(hans, style=style, heteronym=False)))
