#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from importlib import reload
import os

os.environ['PYPINYIN_NO_PHRASES'] = 'true'

import pypinyin.core  # noqa


def test_env():
    assert pypinyin.core.PHRASES_DICT == {}
    assert pypinyin.core.seg('北京') == ['北京']


def test_no_copy():
    """ 禁用 copy 操作 """
    reload(pypinyin.constants)
    assert pypinyin.core.PINYIN_DICT is not pypinyin.pinyin_dict.pinyin_dict

    os.environ['PYPINYIN_NO_DICT_COPY'] = 'true'
    reload(pypinyin.constants)
    assert pypinyin.constants.PINYIN_DICT is pypinyin.pinyin_dict.pinyin_dict
