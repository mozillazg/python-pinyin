#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""汉语拼音转换工具."""

from __future__ import unicode_literals

from .compat import PY2
from .constants import (
    STYLE_NORMAL, STYLE_TONE, STYLE_TONE2, STYLE_TONE3,
    STYLE_INITIALS, STYLE_FIRST_LETTER,
    STYLE_FINALS, STYLE_FINALS_TONE, STYLE_FINALS_TONE2, STYLE_FINALS_TONE3,
    STYLE_BOPOMOFO, STYLE_BOPOMOFO_FIRST
)
from .core import (     # noqa
    pinyin, lazy_pinyin, slug, load_single_dict, load_phrases_dict
)

NORMAL = STYLE_NORMAL
TONE = STYLE_TONE
TONE2 = STYLE_TONE2
TONE3 = STYLE_TONE3
INITIALS = STYLE_INITIALS
FIRST_LETTER = STYLE_FIRST_LETTER
FINALS = STYLE_FINALS
FINALS_TONE = STYLE_FINALS_TONE
FINALS_TONE2 = STYLE_FINALS_TONE2
FINALS_TONE3 = STYLE_FINALS_TONE3
BOPOMOFO = STYLE_BOPOMOFO
BOPOMOFO_FIRST = STYLE_BOPOMOFO_FIRST

__title__ = 'pypinyin'
__version__ = '0.13.0'
__author__ = 'mozillazg, 闲耘'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2016 mozillazg, 闲耘'
__all__ = [
    'pinyin', 'lazy_pinyin', 'slug', 'load_single_dict', 'load_phrases_dict',
    'STYLE_NORMAL', 'NORMAL',
    'STYLE_TONE', 'TONE',
    'STYLE_TONE2', 'TONE2',
    'STYLE_TONE3', 'TONE3',
    'STYLE_INITIALS', 'INITIALS',
    'STYLE_FINALS', 'FINALS',
    'STYLE_FINALS_TONE', 'FINALS_TONE',
    'STYLE_FINALS_TONE2', 'FINALS_TONE2',
    'STYLE_FINALS_TONE3', 'FINALS_TONE3',
    'STYLE_FIRST_LETTER', 'FIRST_LETTER',
    'STYLE_BOPOMOFO', 'BOPOMOFO',
    'STYLE_BOPOMOFO_FIRST', 'BOPOMOFO_FIRST'
]
if PY2:
    # fix "TypeError: Item in ``from list'' not a string" on Python 2
    __all__ = [x.encode('utf-8') for x in __all__]
