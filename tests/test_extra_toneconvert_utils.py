# -*- coding: utf-8 -*-
"""contrib.tone_convert 直接调用、phonetic_symbol 表与 utils 的缺口。

上游 test_tone_convert 已覆盖大量转换表；本文件只补：
- to_initials/to_finals 的空串、单字母、无声母、iou 等边界
- to_normal/to_tone/to_tone2/to_tone3 对 v/空串/非拼音串的实测行为
- tone2_to_tone / tone_to_tone2 对 m/n/ê 特殊音节的往返
- phonetic_symbol 正反表本身（上游只间接经转换函数测到）
- pypinyin.utils 的三个内部函数（上游无任何测试）
"""
from __future__ import unicode_literals

import pytest

from pypinyin.contrib.tone_convert import (
    tone_to_tone2, tone2_to_tone, to_normal, to_tone, to_tone2, to_tone3,
    to_initials, to_finals, to_finals_tone, to_finals_tone2, to_finals_tone3,
)
from pypinyin.phonetic_symbol import (
    phonetic_symbol, phonetic_symbol_reverse,
)
from pypinyin.utils import (
    _remove_dup_items, _remove_dup_and_empty,
    _replace_tone2_style_dict_to_default,
)


@pytest.mark.parametrize('pinyin,strict,expected', [
    ('lü', True, 'l'),
    ('lüe', True, 'l'),
    ('lüe', False, 'l'),
    ('', True, ''),
    ('zhong', True, 'zh'),
    ('a', True, ''),
    ('iou', True, ''),
    # 无合法声母时实测返回首字母（不是空串）。
    ('xyz', True, 'x'),
])
def test_to_initials_edges(pinyin, strict, expected):
    assert to_initials(pinyin, strict) == expected


@pytest.mark.parametrize('pinyin,strict,v_to_u,expected', [
    ('lü', True, False, 'v'),
    ('lü', False, False, 'v'),
    ('lüe', True, False, 've'),
    ('lüe', True, True, 'üe'),
    ('', True, False, ''),
    ('m', True, False, ''),
    ('n', True, False, ''),
    ('iou', True, False, 'iou'),
])
def test_to_finals_edges(pinyin, strict, v_to_u, expected):
    assert to_finals(pinyin, strict, v_to_u) == expected


@pytest.mark.parametrize('func,args,expected', [
    (to_finals_tone, ('lü', True), 'ü'),
    (to_finals_tone, ('lüe', True), 'üe'),
    (to_finals_tone2, ('lü', True, False), 'v'),
    (to_finals_tone2, ('lüe', True, True), 'üe'),
    (to_finals_tone3, ('lü', True, False), 'v'),
    (to_finals_tone3, ('lüe', True, True), 'üe'),
    (to_finals_tone, ('iou', False), 'iou'),
])
def test_to_finals_tone_variants(func, args, expected):
    assert func(*args) == expected


@pytest.mark.parametrize('func,pinyin,expected', [
    (to_normal, 'lü4', 'lv'),
    (to_normal, 'v4', 'v'),
    (to_normal, '', ''),
    (to_normal, 'abc', 'abc'),
    (to_tone, 'lü4', 'lǜ'),
    (to_tone2, 'lü4', 'lv4'),
    (to_tone3, 'lü4', 'lv4'),
])
def test_tone_family_on_v_and_passthrough(func, pinyin, expected):
    assert func(pinyin) == expected


@pytest.mark.parametrize('tone,expected_tone2', [
    ('m̄', 'm1'),
    ('ń', 'n2'),
    ('ê̌', 'ê3'),
])
def test_special_syllables_to_tone2(tone, expected_tone2):
    assert tone_to_tone2(tone) == expected_tone2
    assert tone2_to_tone(expected_tone2) == tone


def test_tone2_to_tone_v_forms():
    assert tone2_to_tone('v') == 'ü'
    assert tone2_to_tone('v4') == 'ǜ'
    assert tone2_to_tone('lüe4') == 'lüè'
    assert tone_to_tone2('lüè') == 'lve4'


def test_tone_roundtrip_zhong():
    assert tone2_to_tone(tone_to_tone2('zhōng')) == 'zhōng'
    assert tone_to_tone2('zhōng') == 'zho1ng'


# ---------------- phonetic_symbol ----------------

def test_phonetic_symbol_table_size_and_reverse():
    assert len(phonetic_symbol) == 35
    assert len(phonetic_symbol_reverse) == 35
    # 正反表逐项互逆（不是只抽查几个）。
    for key, value in phonetic_symbol.items():
        assert phonetic_symbol_reverse[value] == key


def test_phonetic_symbol_special_entries():
    assert phonetic_symbol['ü'] == 'v'
    assert phonetic_symbol_reverse['v1'] == 'ǖ'
    # m̄ / ê̌ 是双码点字符（带结合符），len 为 2。
    assert len('m̄') == 2 and phonetic_symbol['m̄'] == 'm1'
    assert len('ê̌') == 2 and phonetic_symbol['ê̌'] == 'ê3'


# ---------------- utils ----------------

def test_remove_dup_items():
    assert _remove_dup_items(['a', 'b', 'a', '', 'b']) == ['a', 'b', '']
    assert _remove_dup_items(['a', '', 'b', ''],
                             remove_empty=True) == ['a', 'b']


def test_remove_dup_and_empty():
    # 空子列表去重后为空时补 ['']，保持外层长度不变。
    assert _remove_dup_and_empty([['a', 'a', ''], [], ['b']]) == [
        ['a'], [''], ['b']]


def test_replace_tone2_style_dict_to_default():
    assert _replace_tone2_style_dict_to_default('ha3o') == 'hǎo'
    assert _replace_tone2_style_dict_to_default('hao') == 'hao'
