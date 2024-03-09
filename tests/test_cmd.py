#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
from pypinyin.compat import SUPPORT_UCS4
from pypinyin import runner
from pypinyin.tools import toneconvert
from pytest import mark


class Buffer(object):
    def __init__(self):
        self._data = []

    def write(self, data):
        self._data.append(data)


def test_runner_default():
    options = runner.get_parser().parse_args(['你好'])
    assert options.func == 'pinyin'
    assert options.style == 'zh4ao'
    assert options.separator == '-'
    assert not options.heteronym
    assert options.hans == ['你好']
    assert options.errors == 'default'


def test_runner_custom():
    options = runner.get_parser().parse_args([
        '--func', 'slug', '--style', 'zhao', '--separator', ' ',
        '--errors', 'ignore', '--heteronym', '你好啊'])
    assert options.func == 'slug'
    assert options.style == 'zhao'
    assert options.separator == ' '
    assert options.errors == 'ignore'
    assert options.heteronym
    assert options.hans == ['你好啊']


@mark.parametrize('args,output', [
    [['to-normal', 'yí,yì'], ['yi,yi', '\n']],
    [['to-tone', 'yi2,yi4'], ['yí,yì', '\n']],
    [['to-tone', 'hao3'], ['hǎo', '\n']],
    [['to-tone', 'zhong4 xin1'], ['zhòng xīn', '\n']],
    [['to-tone2', 'hǎo'], ['ha3o', '\n']],
    [['to-tone3', 'hǎo'], ['hao3', '\n']],
])
def test_toneconvert_default(args, output):
    buf = Buffer()
    sys.stdout = sys.stderr = buf
    toneconvert.main(args)
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    assert buf._data == output


@mark.skipif(not SUPPORT_UCS4, reason='dont support ucs4')
@mark.parametrize('args,output', [
    [['to-normal', 'm̄, ḿ, m̀, ê̄, ế, ê̌'], ['m, m, m, ê, ê, ê', '\n']],
    [['to-tone', 'm1, m2, m4, ê1, ê2, ê3'], ['m̄, ḿ, m̀, ê̄, ế, ê̌', '\n']],
    [['to-tone2', 'm̄, ḿ, m̀, ê̄, ế, ê̌'], ['m1, m2, m4, ê1, ê2, ê3', '\n']],
    [['to-tone3', 'm̄, ḿ, m̀, ê̄, ế, ê̌'], ['m1, m2, m4, ê1, ê2, ê3', '\n']],
])
def test_toneconvert_nme(args, output):
    buf = Buffer()
    sys.stdout = sys.stderr = buf
    toneconvert.main(args)
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    assert buf._data == output


if __name__ == '__main__':
    import pytest
    pytest.cmdline.main()
