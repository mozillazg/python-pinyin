#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pypinyin
from pypinyin import pinyin, slug


def test_pinyin():
    hans = u'中心'
    assert pinyin(hans) == [[u'zh\u014dng'], [u'x\u012bn']]
    assert pinyin(hans + 'abc') == [[u'zh\u014dng'], [u'x\u012bn'], ['abc']]
    assert pinyin(hans, pypinyin.STYLE_NORMAL) == [[u'zhong'], [u'xin']]
    assert pinyin(hans, pypinyin.STYLE_TONE) == [[u'zh\u014dng'], [u'x\u012bn']]
    assert pinyin(hans, pypinyin.STYLE_TONE2) == [[u'zho1ng'], [u'xi1n']]
    assert pinyin(hans, pypinyin.STYLE_INITIALS) == [['zh'], ['x']]
    assert pinyin(hans, pypinyin.STYLE_FIRST_LETTER) == [[u'z'], [u'x']]
    assert pinyin(hans, heteronym=True) == [[u'zh\u014dng', u'zh\xf2ng'],
                                            [u'x\u012bn']]


def test_slug():
    hans = u'中心'
    assert slug(hans) == 'zhong-xin'
