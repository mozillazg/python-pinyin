#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from pypinyin import phonetic_symbol
from pypinyin.constants import RE_TONE2
# 用于向后兼容，TODO: 废弃
from pypinyin.seg.simpleseg import simple_seg  # noqa


def _replace_tone2_style_dict_to_default(string):
    regex = re.compile(RE_TONE2.pattern.replace('$', ''))
    d = phonetic_symbol.phonetic_symbol_reverse
    string = string.replace('ü', 'v').replace('5', '').replace('0', '')

    def _replace(m):
        s = m.group(0)
        return d.get(s) or s

    return regex.sub(_replace, string)


def _remove_dup_items(lst):
    new_lst = []
    for item in lst:
        if item not in new_lst:
            new_lst.append(item)
    return new_lst
