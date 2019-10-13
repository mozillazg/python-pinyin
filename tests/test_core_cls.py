# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pypinyin.constants import Style
from pypinyin.core import (
    Pinyin, to_fixed, handle_nopinyin, single_pinyin, phrase_pinyin)


def test_use_pre_seg_to_skip_seg():
    class A(Pinyin):
        def pre_seg(self, hans, **kwargs):
            return ['a', 'b', 'c']

    mypinyin = A()

    assert Pinyin().pinyin('测试') == [['cè'], ['shì']]
    assert mypinyin.pinyin('测试') == [['a'], ['b'], ['c']]


def test_use_post_seg_to_change_seg_result():
    class A(Pinyin):
        def post_seg(self, hans, seg_data, **kwargs):
            return ['a', 'b', 'c']

    mypinyin = A()

    assert Pinyin().pinyin('测试') == [['cè'], ['shì']]
    assert mypinyin.pinyin('测试') == [['a'], ['b'], ['c']]


def test_use_seg_function_change_seg_func():
    def seg(han):
        return ['a', 'b', 'c']

    class A(Pinyin):
        def get_seg(self):
            return seg

    mypinyin = A()

    assert Pinyin().pinyin('测试') == [['cè'], ['shì']]
    assert mypinyin.pinyin('测试') == [['a'], ['b'], ['c']]


def test_to_fixed_for_compatibly():
    assert to_fixed('cè', Style.INITIALS) == 'c'


def test_handle_nopinyin_for_compatibly():
    assert handle_nopinyin('test') == [['test']]


def test_single_pinyin_for_compatibly():
    assert single_pinyin('测', Style.TONE, False) == [['cè']]


def test_phrase_pinyin_for_compatibly():
    assert phrase_pinyin('测试', Style.TONE, False) == [['cè'], ['shì']]
