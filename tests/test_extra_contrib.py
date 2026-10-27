# -*- coding: utf-8 -*-
"""contrib 缺口：上游 tone_sandhi/neutral_tone/uv 各自测了正向用例，
本文件补“分词边界决定变调是否生效”这一组对比，以及
neutral_tone 在 TONE3 系、V2UMixin 直接作转换器的行为。

关键实测结论（seg() 结果附在各测试注释里）：
变调只在单个分词片段内部生效；字符串输入先经 mmseg 分词，
不在同一词组里的字不会互相变调，列表输入则把整串当作一个片段。
"""
from __future__ import unicode_literals

import pytest

from pypinyin import lazy_pinyin, Style
from pypinyin.contrib.neutral_tone import NeutralToneWith5Mixin
from pypinyin.contrib.uv import V2UMixin
from pypinyin.converter import DefaultConverter
from pypinyin.core import Pinyin
from pypinyin.seg.simpleseg import seg


class V2UConverter(V2UMixin, DefaultConverter):
    pass


class NeutralConverter(NeutralToneWith5Mixin, DefaultConverter):
    pass


V2U_PINYIN = Pinyin(V2UConverter())
NEUTRAL_PINYIN = Pinyin(NeutralConverter())


@pytest.mark.parametrize('hans,expected_seg', [
    ('一天', ['一', '天']),
    ('老鼠', ['老', '鼠']),
    ('保管好', ['保', '管', '好']),
    ('一一', ['一', '一']),
    ('不不', ['不', '不']),
    ('不是', ['不是']),
    ('你好', ['你好']),
])
def test_seg_explains_sandhi_scope(hans, expected_seg):
    assert seg(hans) == expected_seg


@pytest.mark.parametrize('hans,expected', [
    # 字符串被切成单字，跨字变调不生效；列表输入整串为一个片段，变调生效。
    ('一天', ['yi1', 'tia1n']),
    ('老鼠', ['la3o', 'shu3']),
    ('保管好', ['ba3o', 'gua3n', 'ha3o']),
    ('一一', ['yi1', 'yi1']),
    ('不不', ['bu4', 'bu4']),
])
def test_sandhi_string_input_no_cross_char_change(hans, expected):
    assert lazy_pinyin(hans, style=Style.TONE2,
                       tone_sandhi=True) == expected


@pytest.mark.parametrize('hans,expected', [
    (['一天'], ['yi4', 'tia1n']),
    (['老鼠'], ['la2o', 'shu3']),
    (['保管好'], ['ba2o', 'gua2n', 'ha3o']),
    (['一一'], ['yi4', 'yi1']),
    (['不不'], ['bu2', 'bu4']),
    (['不是不'], ['bu2', 'shi4', 'bu4']),
    (['第一'], ['di4', 'yi1']),
])
def test_sandhi_list_input_applies_within_segment(hans, expected):
    assert lazy_pinyin(hans, style=Style.TONE2,
                       tone_sandhi=True) == expected


def test_sandhi_phrase_segments_do_change_in_string_input():
    # 不是/你好本身就是词组，分词后仍为一个片段，字符串输入也会变调。
    assert lazy_pinyin('不是', style=Style.TONE2,
                       tone_sandhi=True) == ['bu2', 'shi4']
    assert lazy_pinyin('你好', style=Style.TONE2,
                       tone_sandhi=True) == ['ni2', 'ha3o']


def test_sandhi_trailing_run_only():
    # 第三声变调只看片段末尾的连续三声串：你好他末尾是 ta1，
    # 前面两个三声实测不变（实现只处理 trailing run）。
    assert lazy_pinyin(['你好他'], style=Style.TONE2,
                       tone_sandhi=True) == ['ni3', 'ha3o', 'ta1']


def test_sandhi_yi_before_fourth_tone_keeps_yi1():
    # 一二三：底层读音是 yi1（不是 yi4），_yi 只做 4→2 替换，
    # 无 4 可换时实测保持 yi1，不会“变成二声”。
    assert lazy_pinyin(['一二三'], style=Style.TONE2,
                       tone_sandhi=True) == ['yi1', 'e4r', 'sa1n']
    assert lazy_pinyin(['一二三'], style=Style.TONE2) == ['yi1', 'e4r', 'sa1n']


# ---------------- neutral_tone / uv ----------------

def test_neutral_tone_with_5_in_tone3_family():
    # 上游 neutral_tone 多例覆盖 TONE2/FINALS_TONE2；TONE3 系只在表里出现，
    # 这里单独断言：TONE3 在词尾加 5，FINALS_TONE3 同样在词尾加 5。
    assert NEUTRAL_PINYIN.lazy_pinyin('好了', style=Style.TONE3) == [
        'hao3', 'le5']
    assert NEUTRAL_PINYIN.lazy_pinyin('好了', style=Style.FINALS_TONE3) == [
        'ao3', 'e5']
    assert lazy_pinyin('好了', style=Style.TONE3,
                       neutral_tone_with_five=True) == ['hao3', 'le5']


def test_neutral_tone_mixin_leaves_tone_style_alone():
    # 非数字声调风格不受 NeutralToneWith5Mixin 影响。
    assert NEUTRAL_PINYIN.lazy_pinyin('好了', style=Style.TONE) == [
        'hǎo', 'le']


def test_neutral_tone_mixin_keeps_empty_finals_empty():
    assert NEUTRAL_PINYIN.lazy_pinyin('嗯', style=Style.FINALS_TONE2) == ['']


def test_v2u_mixin_direct_converter():
    assert V2U_PINYIN.lazy_pinyin('绿') == ['lü']
    # TONE2 下 v→ü 同样生效；非汉字原样保留，不会被替换。
    assert V2U_PINYIN.lazy_pinyin('战略', style=Style.TONE2) == [
        'zha4n', 'lüe4']
    assert V2U_PINYIN.lazy_pinyin('v') == ['v']
    assert V2U_PINYIN.lazy_pinyin('女', style=Style.FIRST_LETTER) == ['n']


def test_combined_flags_on_one_input():
    assert lazy_pinyin('战略好了', style=Style.TONE2, v_to_u=True,
                       neutral_tone_with_five=True,
                       tone_sandhi=True) == ['zha4n', 'lüe4', 'ha3o', 'le5']
