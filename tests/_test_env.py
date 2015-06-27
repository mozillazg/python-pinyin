#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
os.environ['PYPINYIN_NO_PHRASES'] = 'true'
os.environ['PYPINYIN_NO_JIEBA'] = 'true'

import pypinyin


def test_env():
    assert pypinyin.PHRASES_DICT == {}
    assert pypinyin.seg.no_jieba
    assert pypinyin.seg('北京') == ['北京']
