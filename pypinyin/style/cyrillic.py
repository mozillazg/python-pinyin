# -*- coding: utf-8 -*-
"""CYRILLIC 相关的几个拼音风格实现:

Style.CYRILLIC
Style.CYRILLIC_FIRST
"""
from __future__ import unicode_literals
import re

from pypinyin.constants import Style
from pypinyin.style import register
from pypinyin.style._constants import RE_TONE3
from pypinyin.style._utils import replace_symbol_to_number

# 俄语转换表
CYRILLIC_REPLACE = (
    (re.compile('ong'), 'ung'),
    (re.compile('([zcs])i'), '\\1U'),
    (re.compile('([xqj])u'), '\\1v'),
    (re.compile('^wu(.?)$'), 'u\\1'),
    (re.compile('(.+)r(.?)$'), '\\1R\\2'),
    (re.compile('^zh'), 'Cr'),
    (re.compile('^ch'), 'C'),
    (re.compile('^j'), 'qZ'),
    (re.compile('^z'), 'qZ'),
    (re.compile('^x'), 's'),
    (re.compile('^sh'), 'S'),
    (re.compile('([^CSdst])uo'), '\\1o'),
    (re.compile('^y(.*)$'), 'I\\1'),
    (re.compile('Iai'), 'AI'),
    (re.compile('Ia'), 'A'),
    (re.compile('Ie'), 'E'),
    (re.compile('Ii'), 'i'),
    (re.compile('Iou'), 'V'),
    (re.compile('Iu'), 'v'),
    (re.compile('(.v)(\d?)$'), '\\1I\\2'),
    (re.compile('Io'), 'O'),
    (re.compile('iu'), 'v'),
    (re.compile('ie'), 'E'),
    (re.compile('hui'), 'huei'),
    (re.compile('ui'), 'uI'),
    (re.compile('ai'), 'aI'),
    (re.compile('ei'), 'eI'),
    (re.compile('ia'), 'A'),
    (re.compile('(.*[^h])n([^g]?)$'), '\\1nM\\2'),
    (re.compile('(.*[^h])ng(.?)$'), '\\1n\\2'),
    (re.compile('^v(\d?$)'), 'vI'),
)
CYRILLIC_TABLE = dict(zip(
    u'abwgdEOrZiIklmnopRstufhqcCSHTMUevAV',
    u'абвгдеёжзийклмнопрстуфхццчшщъьыэюяю'
))


class CyrillicfoConverter(object):
    def to_cyrillic(self, pinyin, **kwargs):
        pinyin = self._pre_convert(pinyin)
        # 查表替换成注音
        for find_re, replace in CYRILLIC_REPLACE:
            pinyin = find_re.sub(replace, pinyin)
        pinyin = ''.join(CYRILLIC_TABLE.get(x, x) for x in pinyin)
        return pinyin

    def to_cyrillic_first(self, pinyin, **kwargs):
        pinyin = self.to_cyrillic(pinyin, **kwargs)
        return pinyin[0]

    def _pre_convert(self, pinyin):
        # 用数字表示声调
        pinyin = replace_symbol_to_number(pinyin)
        # 将声调数字移动到最后
        return RE_TONE3.sub(r'\1\3\2', pinyin)


converter = CyrillicfoConverter()
register(Style.CYRILLIC, func=converter.to_cyrillic)
register(Style.CYRILLIC_FIRST, func=converter.to_cyrillic_first)
