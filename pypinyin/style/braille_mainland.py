# -*- coding: utf-8 -*-
"""中国内地盲文相关的几个拼音风格实现:

Style.BRAILLE_MAINLAND
Style.BRAILLE_MAINLAND_TONE

https://en.wikipedia.org/wiki/Mainland_Chinese_Braille
"""
from __future__ import unicode_literals
import re

from pypinyin.constants import Style
from pypinyin.style import register
from pypinyin.style._constants import RE_TONE3
from pypinyin.style._utils import (
    replace_symbol_to_number, replace_symbol_to_no_symbol)

BRAILLE_MAINLAND_REPLACE = (
    (re.compile(r'iu'), 'iou'),
    (re.compile(r'ui'), 'uei'),
    (re.compile(r'un'), 'uen'),
    (re.compile(r'ong'), 'ung'),
    (re.compile(r'^yi?'), 'i'),
    (re.compile(r'^wu?'), 'u'),
    (re.compile(r'y'), 'i'),
    (re.compile(r'w'), 'u'),
    (re.compile(r'iu'), 'v'),
    (re.compile(r'^([jqx])u'), '\\1v'),
    (re.compile(r'([iuv])n'), '\\1en'),
    (re.compile(r'^zhi?'), 'Z'),
    (re.compile(r'^chi?'), 'C'),
    (re.compile(r'^shi?'), 'S'),
    (re.compile(r'^([zcsr])i'), '\\1'),
    (re.compile(r'iang'), '⠭'),
    (re.compile(r'uang'), '⠶'),
    (re.compile(r'ueng'), '⠲'),
    (re.compile(r'iong'), '⠹'),
    (re.compile(r'ang'), '⠦'),
    (re.compile(r'eng'), '⠼'),
    (re.compile(r'uai'), '⠽'),
    (re.compile(r'iao'), '⠜'),
    (re.compile(r'iou'), '⠳'),
    (re.compile(r'ian'), '⠩'),
    (re.compile(r'uan'), '⠻'),
    (re.compile(r'van'), '⠯'),
    (re.compile(r'uen'), '⠒'),
    (re.compile(r'ing'), '⠡'),
    (re.compile(r'ong'), '⠲'),
    (re.compile(r'er'), '⠗'),
    (re.compile(r'ai'), '⠪'),
    (re.compile(r'ei'), '⠮'),
    (re.compile(r'ao'), '⠖'),
    (re.compile(r'ou'), '⠷'),
    (re.compile(r'an'), '⠧'),
    (re.compile(r'en'), '⠴'),
    (re.compile(r'ia'), '⠫'),
    (re.compile(r'ua'), '⠿'),
    (re.compile(r'ie'), '⠑'),
    (re.compile(r'uo'), '⠕'),
    (re.compile(r've'), '⠾'),
    (re.compile(r'ui'), '⠺'),
    (re.compile(r'in'), '⠣'),
    (re.compile(r'vn'), '⠸'),
)

BRAILLE_MAINLAND_TABLE = dict(zip(
    'bpmfdtnlgkhjqxZCSrzcsiuvaoe1234',
    '⠃⠏⠍⠋⠙⠞⠝⠇⠛⠅⠓⠛⠅⠓⠌⠟⠱⠚⠵⠉⠎⠊⠥⠬⠔⠢⠢⠁⠂⠄⠆'
))


class BrailleMainlandConverter(object):
    def to_braille_mainland_tone(self, pinyin, **kwargs):
        # 用数字表示声调
        pinyin = replace_symbol_to_number(pinyin)
        # 将声调数字移动到最后
        pinyin = RE_TONE3.sub(r'\1\3\2', pinyin)
        for find_re, replace in BRAILLE_MAINLAND_REPLACE:
            pinyin = find_re.sub(replace, pinyin)
        pinyin = ''.join(BRAILLE_MAINLAND_TABLE.get(x, x) for x in pinyin)
        return pinyin

    def to_braille_mainland(self, pinyin, **kwargs):
        pinyin = replace_symbol_to_no_symbol(pinyin)
        for find_re, replace in BRAILLE_MAINLAND_REPLACE:
            pinyin = find_re.sub(replace, pinyin)
        pinyin = ''.join(BRAILLE_MAINLAND_TABLE.get(x, x) for x in pinyin)
        return pinyin


converter = BrailleMainlandConverter()
register(Style.BRAILLE_MAINLAND_TONE, func=converter.to_braille_mainland_tone)
register(Style.BRAILLE_MAINLAND, func=converter.to_braille_mainland)
