#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from pypinyin.runner import get_parser


def test_default():
    options = get_parser().parse_args(['你好'])
    assert options.func == 'pinyin'
    assert options.style == 'TONE'
    assert options.separator == '-'
    assert not options.heteronym
    assert options.hans == '你好'
    assert options.errors == 'default'


def test_custom():
    options = get_parser().parse_args(['--func', 'slug',
                                       '--style', 'NORMAL',
                                       '--separator', ' ',
                                       '--errors', 'ignore',
                                       '--heteronym', '你好啊'])
    assert options.func == 'slug'
    assert options.style == 'NORMAL'
    assert options.separator == ' '
    assert options.errors == 'ignore'
    assert options.heteronym
    assert options.hans == '你好啊'
