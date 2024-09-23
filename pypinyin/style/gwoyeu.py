# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from pypinyin.constants import Style
from pypinyin.style import register

GWOYEU_REPLACE = (
    (re.compile(r'^r5$'), 'er5'),
    (re.compile(r'iu'), 'iou'),
    (re.compile(r'u([in])'), 'ue\\1'),
    (re.compile(r'ao'), 'au'),
    (re.compile(r'ong'), 'ung'),
    (re.compile(r'^yi?'), 'i'),
    (re.compile(r'^wu?'), 'u'),
    (re.compile(r'^([jqx])u'), '\\1iu'),
    (re.compile(r'^([zcsr]h?)i'), '\\1y'),
    (re.compile(r'^zh'), 'j'),
    (re.compile(r'^z'), 'tz'),
    (re.compile(r'^c'), 'ts'),
    (re.compile(r'^q'), 'ch'),
    (re.compile(r'^x'), 'sh'),
    (re.compile(r'er'), 'el'),
    (re.compile(r'5$'), ''),
    (re.compile(r'0$'), 'q'),
    (re.compile(r'i(.+[34])$'), 'yi\\1'),
    (re.compile(r'u(.+[34])$'), 'wu\\1'),
)

TONE_REPLACE = (
    (re.compile(r'^([lmnr])(.+)1$'), '\\1h\\2'),
    (re.compile(r'^([lmnr])(.+)2$'), '\\1\\2'),
    (re.compile(r'^([^ae]*)i2$'), '\\1yi'),
    (re.compile(r'^([^ae]*)i(.+)2$'), '\\1y\\2'),
    (re.compile(r'^([^ao]*)u2$'), '\\1wu'),
    (re.compile(r'^([^ao]*)u(.+)2$'), '\\1w\\2'),
    (re.compile(r'([aeiouy]+)(.*)2$'), '\\1r\\2'),
    (re.compile(r'^([^ae]*)i(.+)3$'), '\\1e\\2'),
    (re.compile(r'^([^ao]*)u(.+)3$'), '\\1o\\2'),
    (re.compile(r'([aeiouy])(.*)3$'), '\\1\\1\\2'),
    (re.compile(r'^([^ae]*)i4$'), '\\1ih'),
    (re.compile(r'^([^ao]*)u4$'), '\\1uh'),
    (re.compile(r'i4$'), 'y'),
    (re.compile(r'u4$'), 'w'),
    (re.compile(r'l4$'), 'll'),
    (re.compile(r'ng4$'), 'nq'),
    (re.compile(r'n4$'), 'nn'),
    (re.compile(r'4$'), 'h'),
)

def to_gwoyeu(self, pinyin, **kwargs):
    for find_re, replace in GWOYEU_REPLACE:
        pinyin = find_re.sub(replace, pinyin)
    for find_re, replace in TONE_REPLACE:
        if find_re.search(pinyin):
            return find_re.sub(replace, pinyin)
    return pinyin


register(Style.GWOYEU, func=to_gwoyeu)
