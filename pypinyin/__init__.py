#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""汉语拼音转换工具."""

from __future__ import unicode_literals
from .compat import __builtin__
from .core import *   # noqa

__title__ = 'pypinyin'
__version__ = '0.8.0'
__author__ = 'mozillazg, 闲耘'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2014 mozillazg, 闲耘'
__all__ = [
    'pinyin', 'lazy_pinyin', 'slug',
    'STYLE_NORMAL', 'NORMAL',
    'STYLE_TONE', 'TONE',
    'STYLE_TONE2', 'TONE2',
    'STYLE_INITIALS', 'INITIALS',
    'STYLE_FINALS', 'FINALS',
    'STYLE_FINALS_TONE', 'FINALS_TONE',
    'STYLE_FINALS_TONE2', 'FINALS_TONE2',
    'STYLE_FIRST_LETTER', 'FIRST_LETTER'
]
# fix "TypeError: Item in ``from list'' not a string" on Python 2
__all__ = [__builtin__.str(x) for x in __all__]
