# -*- coding: utf-8 -*-
"""slug 变体与 errors 参数：上游 test_pinyin.py 只测了 slug 两例、
errors 主要测 ⺁/鿅 两字，本文件补其余组合。

所有断言均经探针实测（2026-10-27，python-pinyin 0.55.0 fresh clone）。
"""
from __future__ import unicode_literals

import pytest

from pypinyin import pinyin, lazy_pinyin, slug, Style
from pypinyin.exceptions import PinyinNotFoundException


# ---------------- slug ----------------

def test_slug_empty():
    assert slug('') == ''


def test_slug_list_input():
    assert slug(['中心', '你好']) == 'zhong-xin-ni-hao'


def test_slug_first_letter():
    assert slug('中国人', style=Style.FIRST_LETTER) == 'z-g-r'


def test_slug_separator_space():
    assert slug('中国人', separator=' ') == 'zhong guo ren'


def test_slug_separator_empty():
    assert slug('中国人', separator='') == 'zhongguoren'


def test_slug_tone2():
    assert slug('中心', style=Style.TONE2) == 'zho1ng-xi1n'


def test_slug_heteronym_takes_all_readings():
    # 上游只测了 slug('中心', heteronym=True)（单读音）；行在 TONE 下有 5 个读音，
    # 但 slug 默认 NORMAL 风格去声调后 xíng/xìng、háng/hàng 分别合并，只剩 3 个。
    assert slug('行', heteronym=True) == 'xing-hang-heng'
    assert slug('行', heteronym=False) == 'xing'


def test_slug_heteronym_list():
    assert slug(['中心', '行'], heteronym=True) == 'zhong-xin-xing-hang-heng'


def test_slug_errors_ignore_and_replace():
    assert slug('中心⺁', errors='ignore') == 'zhong-xin'
    assert slug('中心⺁', errors='replace') == 'zhong-xin-2e81'


def test_slug_non_han_only():
    assert slug('abc') == 'abc'


# ---------------- pinyin / lazy_pinyin 输入形态 ----------------

def test_pinyin_empty_list():
    assert pinyin([]) == []


def test_pinyin_list_of_single_chars():
    assert pinyin(['中', '心']) == [['zhōng'], ['xīn']]


def test_pinyin_list_mixed_with_non_han():
    assert pinyin(['你好', 'abc']) == [['nǐ'], ['hǎo'], ['abc']]


def test_pinyin_list_phrase_plus_non_han_ultimate_branch():
    # UltimateConverter 分支：列表元素里非汉字串先分词、汉字串直接当词。
    assert pinyin(['黄山', 'B股'], style=Style.TONE2) == [
        ['hua2ng'], ['sha1n'], ['B'], ['gu3']]


def test_pinyin_list_with_empty_string():
    assert pinyin(['']) == []


def test_lazy_pinyin_empty_and_list():
    assert lazy_pinyin('') == []
    assert lazy_pinyin(['中', '心']) == ['zhong', 'xin']


# ---------------- errors ----------------

@pytest.mark.parametrize('fn,kwargs,expected', [
    (pinyin, dict(errors='ignore'), []),
    (pinyin, dict(errors='replace'), [['3042']]),
    (lazy_pinyin, dict(errors='ignore'), []),
    (lazy_pinyin, dict(errors='replace'), ['3042']),
    # 可调用对象返回空字符串 / None 时结果都是空列表（不是 [['']]）。
    (pinyin, dict(errors=lambda x: ''), []),
    (pinyin, dict(errors=lambda x: None), []),
    # 未知 errors 字符串不报错，实测按“无结果”处理。
    (pinyin, dict(errors='bogus'), []),
    (lazy_pinyin, dict(errors='bogus'), []),
])
def test_errors_variants_for_japanese_kana(fn, kwargs, expected):
    assert fn('あ', **kwargs) == expected


def test_errors_ignore_in_list_input():
    assert pinyin(['あ', '中'], errors='ignore') == [['zhōng']]


@pytest.mark.parametrize('heteronym,expected', [
    (True, [['a', 'b']]),
    # 非多音字模式下可调用对象返回的二维列表只取第一行、每字只取首项。
    (False, [['a']]),
])
def test_errors_callable_returning_2d_list(heteronym, expected):
    assert pinyin('ああ', heteronym=heteronym,
                  errors=lambda x: [['a', 'b']]) == expected


def test_errors_ascii_word_replace_and_ignore():
    # 纯 ASCII 词在 errors='replace' 下会被当作“无拼音字符”编码，
    # 而不是像默认模式那样原样保留。
    assert pinyin('abc', errors='replace') == [['616263']]
    assert pinyin('abc', errors='ignore') == []


def test_errors_exception_attributes():
    # 上游只断言抛异常；这里补 message / chars 属性的实测值。
    with pytest.raises(PinyinNotFoundException) as excinfo:
        pinyin('あ', errors='exception')
    assert excinfo.value.chars == 'あ'
    assert excinfo.value.message == 'No pinyin found for character "あ"'
    assert str(excinfo.value) == 'No pinyin found for character "あ"'
