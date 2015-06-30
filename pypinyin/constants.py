#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
import re
import sys

from . import phonetic_symbol, pinyin_dict

# 词语拼音库
if os.environ.get('PYPINYIN_NO_PHRASES'):
    PHRASES_DICT = {}
else:
    from . import phrases_dict
    PHRASES_DICT = phrases_dict.phrases_dict.copy()

# 单字拼音库
PINYIN_DICT = pinyin_dict.pinyin_dict.copy()
# 声母表
_INITIALS = 'zh,ch,sh,b,p,m,f,d,t,n,l,g,k,h,j,q,x,r,z,c,s,yu,y,w'.split(',')
# 带声调字符与使用数字标识的字符的对应关系，类似： {u'ā': 'a1'}
PHONETIC_SYMBOL = phonetic_symbol.phonetic_symbol.copy()
# 所有的带声调字符
re_phonetic_symbol_source = ''.join(PHONETIC_SYMBOL.keys())
# 匹配带声调字符的正则表达式
RE_PHONETIC_SYMBOL = r'[' + re.escape(re_phonetic_symbol_source) + r']'
# 匹配使用数字标识声调的字符的正则表达式
RE_TONE2 = r'([aeoiuvnm])([0-4])$'
# 有拼音的汉字
RE_HANS = re.compile(r'''^(?:
    [\u3400-\u4dbf]     # CJK 扩展 A:[3400-4DBF]
    |[\u4e00-\u9fff]    # CJK 基本:[4E00-9FFF]
    |[\uf900-\ufaff]    # CJK 兼容:[F900-FAFF]
)+$''', re.X)
# 没有拼音的字符
RE_NONE_HANS = re.compile(r'''^(?:
    [^\u3400-\u4dbf
     \u4e00-\u9fff
     \uf900-\ufaff]
)+$''', re.X)
# 分割中文字符和非中文字符
RE_NONE_HANS_SPLIT = re.compile(r'''
(?:
    (?<=                        # 非中文字符
        [^\u3400-\u4dbf
         \u4e00-\u9fff
         \uf900-\ufaff]
    )
    (?=                         # 中文字符
        (?:
            [\u3400-\u4dbf]     # CJK 扩展 A:[3400-4DBF]
            |[\u4e00-\u9fff]    # CJK 基本:[4E00-9FFF]
            |[\uf900-\ufaff]    # CJK 兼容:[F900-FAFF]
        )
    )
)
| (?:
    (?<=                        # 中文字符
        (?:
            [\u3400-\u4dbf]     # CJK 扩展 A:[3400-4DBF]
            |[\u4e00-\u9fff]    # CJK 基本:[4E00-9FFF]
            |[\uf900-\ufaff]    # CJK 兼容:[F900-FAFF]
        )
    )
    (?=                         # 非中文字符
        [^\u3400-\u4dbf
         \u4e00-\u9fff
         \uf900-\ufaff]
    )
)
''', re.X)

# 拼音风格
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
# 普通风格，不带声调
NORMAL = STYLE_NORMAL = PINYIN_STYLE['NORMAL']
# 标准风格，声调在韵母的第一个字母上
TONE = STYLE_TONE = PINYIN_STYLE['TONE']
# 声调在拼音之后，使用数字 1~4 标识
TONE2 = STYLE_TONE2 = PINYIN_STYLE['TONE2']
# 仅保留声母部分
INITIALS = STYLE_INITIALS = PINYIN_STYLE['INITIALS']
# 仅保留首字母
FIRST_LETTER = STYLE_FIRST_LETTER = PINYIN_STYLE['FIRST_LETTER']
# 仅保留韵母部分，不带声调
FINALS = STYLE_FINALS = PINYIN_STYLE['FINALS']
# 仅保留韵母部分，带声调
FINALS_TONE = STYLE_FINALS_TONE = PINYIN_STYLE['FINALS_TONE']
# 仅保留韵母部分，声调在拼音之后，使用数字 1~4 标识
FINALS_TONE2 = STYLE_FINALS_TONE2 = PINYIN_STYLE['FINALS_TONE2']
