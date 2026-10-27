# -*- coding: utf-8 -*-
"""风格矩阵缺口：上游已大面积覆盖中心/中国等常用字，
本文件只用上游各风格表里没有出现过的字与组合。

- WADEGILES/GWOYEU/BRAILLE：吕/绿/学/雪（句已在上游 wadegiles_v_u 里出现，故不用）
- FINALS_TONE2 strict：丢/刘（iou 表只有牛/归/论）、贵/对（uei 表只有鬼）、孙（uen 表只有论）
- 零声母 INITIALS/FINALS：啊/欧/安（不在上游 zero_consonant 表的字集里）
- 多音字：行/乐/长/重、词组重庆/长沙（上游 heteronym 表只用中心/朝阳）
"""
from __future__ import unicode_literals

import pytest

from pypinyin import pinyin, lazy_pinyin, Style


@pytest.mark.parametrize('han,style,kwargs,expected', [
    ('吕', Style.WADEGILES, {}, ['lv']),
    ('吕', Style.WADEGILES, dict(v_to_u=True), ['lü']),
    ('吕', Style.GWOYEU, {}, ['leu']),
    ('吕', Style.BRAILLE_MAINLAND, {}, ['⠇⠬']),
    ('吕', Style.BRAILLE_MAINLAND_TONE, {}, ['⠇⠬⠄']),
    ('绿', Style.WADEGILES, {}, ['lv']),
    ('绿', Style.WADEGILES, dict(v_to_u=True), ['lü']),
    ('绿', Style.GWOYEU, {}, ['liuh']),
    ('绿', Style.BRAILLE_MAINLAND, {}, ['⠇⠬']),
    ('绿', Style.BRAILLE_MAINLAND_TONE, {}, ['⠇⠬⠆']),
    ('学', Style.WADEGILES, {}, ['hsveh']),
    ('学', Style.WADEGILES, dict(v_to_u=True), ['hsüeh']),
    ('学', Style.GWOYEU, {}, ['shyue']),
    ('学', Style.BRAILLE_MAINLAND, {}, ['⠓⠾']),
    ('学', Style.BRAILLE_MAINLAND_TONE, {}, ['⠓⠾⠂']),
    ('雪', Style.WADEGILES, {}, ['hsveh']),
    ('雪', Style.WADEGILES, dict(v_to_u=True), ['hsüeh']),
    ('雪', Style.GWOYEU, {}, ['sheue']),
    ('雪', Style.BRAILLE_MAINLAND, {}, ['⠓⠾']),
    ('雪', Style.BRAILLE_MAINLAND_TONE, {}, ['⠓⠾⠄']),
])
def test_rare_chars_in_wadegiles_gwoyeu_braille(han, style, kwargs, expected):
    assert lazy_pinyin(han, style=style, **kwargs) == expected


@pytest.mark.parametrize('han,strict,expected', [
    ('丢', True, ['iou1']),
    ('丢', False, ['iu1']),
    ('刘', True, ['iou2']),
    ('刘', False, ['iu2']),
    ('贵', True, ['uei4']),
    ('贵', False, ['ui4']),
    ('对', True, ['uei4']),
    ('对', False, ['ui4']),
    ('孙', True, ['u1en']),
    ('孙', False, ['u1n']),
])
def test_finals_tone2_strict_for_iou_uei_uen(han, strict, expected):
    assert lazy_pinyin(han, style=Style.FINALS_TONE2,
                       strict=strict) == expected


@pytest.mark.parametrize('han,style,strict,expected', [
    # 啊/欧/安即使 strict=False 也没有 y/w 声母（与衣→y、乌→w 不同）。
    ('啊', Style.INITIALS, True, ['']),
    ('啊', Style.INITIALS, False, ['']),
    ('啊', Style.FINALS, False, ['a']),
    ('欧', Style.INITIALS, True, ['']),
    ('欧', Style.INITIALS, False, ['']),
    ('欧', Style.FINALS, False, ['ou']),
    ('安', Style.INITIALS, True, ['']),
    ('安', Style.INITIALS, False, ['']),
    ('安', Style.FINALS, False, ['an']),
])
def test_zero_initial_chars_without_glide(han, style, strict, expected):
    assert lazy_pinyin(han, style=style, strict=strict) == expected


@pytest.mark.parametrize('han,expected', [
    ('行', [['xíng', 'háng', 'héng', 'xìng', 'hàng']]),
    ('乐', [['lè', 'yuè']]),
    ('长', [['zhǎng', 'cháng']]),
    ('重', [['zhòng', 'chóng', 'tóng']]),
])
def test_heteronym_single_chars(han, expected):
    assert pinyin(han, heteronym=True) == expected


@pytest.mark.parametrize('han,expected', [
    # 词组级多音字：词组读音优先于单字读音，heteronym=True 也不展开。
    ('重庆', [['chóng'], ['qìng']]),
    ('长沙', [['cháng'], ['shā']]),
])
def test_heteronym_phrases_keep_phrase_reading(han, expected):
    assert pinyin(han, heteronym=True) == expected


def test_unknown_style_int_and_name_fall_back_to_tone():
    # 上游只测了 style='unknown'；整数 999 与风格名字符串同样回落到 TONE。
    assert lazy_pinyin('中国', style=999) == ['zhōng', 'guó']
    assert lazy_pinyin('中国', style='NORMAL') == ['zhōng', 'guó']
