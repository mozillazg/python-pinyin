#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pytest

from pypinyin import (
    lazy_pinyin, NORMAL, TONE, TONE2, TONE3, INITIALS,
    FIRST_LETTER, FINALS, FINALS_TONE, FINALS_TONE2, FINALS_TONE3
)

# 零声母
data_for_zero_consonant = [
    # ü行的韵母，前面没有声母的时候，写成yu(迂)，yue(约)，yuan(冤)，
    ['鱼', {'style': NORMAL}, ['yu']],
    ['鱼', {'style': TONE}, ['yú']],
    ['鱼', {'style': TONE2}, ['yu2']],
    ['鱼', {'style': TONE3}, ['yu2']],
    ['鱼', {'style': INITIALS}, ['']],
    ['鱼', {'style': FIRST_LETTER}, ['y']],
    ['鱼', {'style': FINALS}, ['v']],
    ['鱼', {'style': FINALS_TONE}, ['ǘ']],
    ['鱼', {'style': FINALS_TONE2}, ['v2']],
    ['鱼', {'style': FINALS_TONE3}, ['v2']],

    ['约', {'style': NORMAL}, ['yue']],
    ['约', {'style': TONE}, ['yuē']],
    ['约', {'style': TONE2}, ['yue1']],
    ['约', {'style': TONE3}, ['yue1']],
    ['约', {'style': INITIALS}, ['']],
    ['约', {'style': FIRST_LETTER}, ['y']],
    ['约', {'style': FINALS}, ['ve']],
    ['约', {'style': FINALS_TONE}, ['üē']],
    ['约', {'style': FINALS_TONE2}, ['ve1']],
    ['约', {'style': FINALS_TONE3}, ['ve1']],

    ['元', {'style': NORMAL}, ['yuan']],
    ['元', {'style': TONE}, ['yuán']],
    ['元', {'style': TONE2}, ['yua2n']],
    ['元', {'style': TONE3}, ['yuan2']],
    ['元', {'style': INITIALS}, ['']],
    ['元', {'style': FIRST_LETTER}, ['y']],
    ['元', {'style': FINALS}, ['van']],
    ['元', {'style': FINALS_TONE}, ['üán']],
    ['元', {'style': FINALS_TONE2}, ['va2n']],
    ['元', {'style': FINALS_TONE3}, ['van2']],

    # yun 不应该受 un -> uen 规则的影响
    ['晕', {'style': NORMAL}, ['yun']],
    ['晕', {'style': TONE}, ['yūn']],
    ['晕', {'style': TONE2}, ['yu1n']],
    ['晕', {'style': TONE3}, ['yun1']],
    ['晕', {'style': INITIALS}, ['']],
    ['晕', {'style': FIRST_LETTER}, ['y']],
    ['晕', {'style': FINALS}, ['vn']],
    ['晕', {'style': FINALS_TONE}, ['ǖn']],
    ['晕', {'style': FINALS_TONE2}, ['v1n']],
    ['晕', {'style': FINALS_TONE3}, ['vn1']],

    # u行的韵母，前面没有声母的时候，写成wu(乌)，wa(蛙)，wo(窝)，wai(歪)，
    # wei(威)，wan(弯)，wen(温)，wang(汪)，weng(翁)。
    ['武', {'style': NORMAL}, ['wu']],
    ['武', {'style': TONE}, ['wǔ']],
    ['武', {'style': TONE2}, ['wu3']],
    ['武', {'style': TONE3}, ['wu3']],
    ['武', {'style': INITIALS}, ['']],
    ['武', {'style': FIRST_LETTER}, ['w']],
    ['武', {'style': FINALS}, ['u']],
    ['武', {'style': FINALS_TONE}, ['ǔ']],
    ['武', {'style': FINALS_TONE2}, ['u3']],
    ['武', {'style': FINALS_TONE3}, ['u3']],

    ['旺', {'style': NORMAL}, ['wang']],
    ['旺', {'style': TONE}, ['wàng']],
    ['旺', {'style': TONE2}, ['wa4ng']],
    ['旺', {'style': TONE3}, ['wang4']],
    ['旺', {'style': INITIALS}, ['']],
    ['旺', {'style': FIRST_LETTER}, ['w']],
    ['旺', {'style': FINALS}, ['uang']],
    ['旺', {'style': FINALS_TONE}, ['uàng']],
    ['旺', {'style': FINALS_TONE2}, ['ua4ng']],
    ['旺', {'style': FINALS_TONE3}, ['uang4']],

    # i行的韵母，前面没有声母的时候，写成yi(衣)，ya(呀)，ye(耶)，yao(腰)，
    # you(忧)，yan(烟)，yin(因)，yang(央)，ying(英)，yong(雍)。
    ['宜', {'style': NORMAL}, ['yi']],
    ['宜', {'style': TONE}, ['yí']],
    ['宜', {'style': TONE2}, ['yi2']],
    ['宜', {'style': TONE3}, ['yi2']],
    ['宜', {'style': INITIALS}, ['']],
    ['宜', {'style': FIRST_LETTER}, ['y']],
    ['宜', {'style': FINALS}, ['i']],
    ['宜', {'style': FINALS_TONE}, ['í']],
    ['宜', {'style': FINALS_TONE2}, ['i2']],
    ['宜', {'style': FINALS_TONE3}, ['i2']],

    ['盐', {'style': NORMAL}, ['yan']],
    ['盐', {'style': TONE}, ['yán']],
    ['盐', {'style': TONE2}, ['ya2n']],
    ['盐', {'style': TONE3}, ['yan2']],
    ['盐', {'style': INITIALS}, ['']],
    ['盐', {'style': FIRST_LETTER}, ['y']],
    ['盐', {'style': FINALS}, ['ian']],
    ['盐', {'style': FINALS_TONE}, ['ián']],
    ['盐', {'style': FINALS_TONE2}, ['ia2n']],
    ['盐', {'style': FINALS_TONE3}, ['ian2']],
]


@pytest.mark.parametrize('hans, kwargs, result', data_for_zero_consonant)
def test_zero_consonant(hans, kwargs, result):
    assert lazy_pinyin(hans, **kwargs) == result


data_for_uv = [
    # ü行的韵跟声母j，q，x拼的时候，写成ju(居)，qu(区)，xu(虚)，
    # ü上两点也省略；但是跟声母n，l拼的时候，仍然写成nü(女)，lü(吕)。
    ['具', {'style': NORMAL}, ['ju']],
    ['具', {'style': TONE}, ['jù']],
    ['具', {'style': TONE2}, ['ju4']],
    ['具', {'style': TONE3}, ['ju4']],
    ['具', {'style': INITIALS}, ['j']],
    ['具', {'style': FIRST_LETTER}, ['j']],
    ['具', {'style': FINALS}, ['v']],
    ['具', {'style': FINALS_TONE}, ['ǜ']],
    ['具', {'style': FINALS_TONE2}, ['v4']],
    ['具', {'style': FINALS_TONE3}, ['v4']],

    ['取', {'style': NORMAL}, ['qu']],
    ['取', {'style': TONE}, ['qǔ']],
    ['取', {'style': TONE2}, ['qu3']],
    ['取', {'style': TONE3}, ['qu3']],
    ['取', {'style': INITIALS}, ['q']],
    ['取', {'style': FIRST_LETTER}, ['q']],
    ['取', {'style': FINALS}, ['v']],
    ['取', {'style': FINALS_TONE}, ['ǚ']],
    ['取', {'style': FINALS_TONE2}, ['v3']],
    ['取', {'style': FINALS_TONE3}, ['v3']],

    ['徐', {'style': NORMAL}, ['xu']],
    ['徐', {'style': TONE}, ['xú']],
    ['徐', {'style': TONE2}, ['xu2']],
    ['徐', {'style': TONE3}, ['xu2']],
    ['徐', {'style': INITIALS}, ['x']],
    ['徐', {'style': FIRST_LETTER}, ['x']],
    ['徐', {'style': FINALS}, ['v']],
    ['徐', {'style': FINALS_TONE}, ['ǘ']],
    ['徐', {'style': FINALS_TONE2}, ['v2']],
    ['徐', {'style': FINALS_TONE3}, ['v2']],

    ['女', {'style': NORMAL}, ['nv']],
    ['女', {'style': TONE}, ['nǚ']],
    ['女', {'style': TONE2}, ['nv3']],
    ['女', {'style': TONE3}, ['nv3']],
    ['女', {'style': INITIALS}, ['n']],
    ['女', {'style': FIRST_LETTER}, ['n']],
    ['女', {'style': FINALS}, ['v']],
    ['女', {'style': FINALS_TONE}, ['ǚ']],
    ['女', {'style': FINALS_TONE2}, ['v3']],
    ['女', {'style': FINALS_TONE3}, ['v3']],

    ['吕', {'style': NORMAL}, ['lv']],
    ['吕', {'style': TONE}, ['lǚ']],
    ['吕', {'style': TONE2}, ['lv3']],
    ['吕', {'style': TONE3}, ['lv3']],
    ['吕', {'style': INITIALS}, ['l']],
    ['吕', {'style': FIRST_LETTER}, ['l']],
    ['吕', {'style': FINALS}, ['v']],
    ['吕', {'style': FINALS_TONE}, ['ǚ']],
    ['吕', {'style': FINALS_TONE2}, ['v3']],
    ['吕', {'style': FINALS_TONE3}, ['v3']],
]


@pytest.mark.parametrize('hans, kwargs, result', data_for_uv)
def test_uv(hans, kwargs, result):
    assert lazy_pinyin(hans, **kwargs) == result


data_for_iou = [
    # iou，uei，uen前面加声母的时候，写成iu，ui，un。
    # 例如niu(牛)，gui(归)，lun(论)。
    ['牛', {'style': NORMAL}, ['niu']],
    ['牛', {'style': TONE}, ['niú']],
    ['牛', {'style': TONE2}, ['niu2']],
    ['牛', {'style': TONE3}, ['niu2']],
    ['牛', {'style': INITIALS}, ['n']],
    ['牛', {'style': FIRST_LETTER}, ['n']],
    ['牛', {'style': FINALS}, ['iou']],
    ['牛', {'style': FINALS_TONE}, ['ioú']],
    ['牛', {'style': FINALS_TONE2}, ['iou2']],
    ['牛', {'style': FINALS_TONE3}, ['iou2']],
]


@pytest.mark.parametrize('hans, kwargs, result', data_for_iou)
def test_iou(hans, kwargs, result):
    assert lazy_pinyin(hans, **kwargs) == result


data_for_uei = [
    # iou，uei，uen前面加声母的时候，写成iu，ui，un。
    # 例如niu(牛)，gui(归)，lun(论)。
    ['鬼', {'style': NORMAL}, ['gui']],
    ['鬼', {'style': TONE}, ['guǐ']],
    ['鬼', {'style': TONE2}, ['gui3']],
    ['鬼', {'style': TONE3}, ['gui3']],
    ['鬼', {'style': INITIALS}, ['g']],
    ['鬼', {'style': FIRST_LETTER}, ['g']],
    ['鬼', {'style': FINALS}, ['uei']],
    ['鬼', {'style': FINALS_TONE}, ['ueǐ']],
    ['鬼', {'style': FINALS_TONE2}, ['uei3']],
    ['鬼', {'style': FINALS_TONE3}, ['uei3']],
]


@pytest.mark.parametrize('hans, kwargs, result', data_for_uei)
def test_uei(hans, kwargs, result):
    assert lazy_pinyin(hans, **kwargs) == result


data_for_uen = [
    # iou，uei，uen前面加声母的时候，写成iu，ui，un。
    # 例如niu(牛)，gui(归)，lun(论)。
    ['论', {'style': NORMAL}, ['lun']],
    ['论', {'style': TONE}, ['lùn']],
    ['论', {'style': TONE2}, ['lu4n']],
    ['论', {'style': TONE3}, ['lun4']],
    ['论', {'style': INITIALS}, ['l']],
    ['论', {'style': FIRST_LETTER}, ['l']],
    ['论', {'style': FINALS}, ['uen']],
    ['论', {'style': FINALS_TONE}, ['ùen']],
    ['论', {'style': FINALS_TONE2}, ['u4en']],
    ['论', {'style': FINALS_TONE3}, ['uen4']],
]


@pytest.mark.parametrize('hans, kwargs, result', data_for_uen)
def test_uen(hans, kwargs, result):
    assert lazy_pinyin(hans, **kwargs) == result
