#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
os.environ['PYPINYIN_NO_PHRASES'] = 'true'
os.environ['PYPINYIN_NO_JIEBA'] = 'true'

import pypinyin.core  # noqa


def test_env():
    assert pypinyin.core.PHRASES_DICT == {}
    assert pypinyin.core.seg.no_jieba
    assert pypinyin.core.seg('北京') == ['北京']
