#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pypinyin import pinyin, slug
from pypinyin import STYLE_NORMAL, STYLE_TONE, STYLE_TONE2, STYLE_INITIALS
from pypinyin import STYLE_FIRST_LETTER, STYLE_FINALS, STYLE_FINALS_TONE
from pypinyin import STYLE_FINALS_TONE2


def test_pinyin_initials():
    hans = u'中心'
    assert pinyin(hans) == [[u'zh\u014dng'], [u'x\u012bn']]
    assert pinyin(hans + 'abc') == [[u'zh\u014dng'], [u'x\u012bn'], ['abc']]
    assert pinyin(hans, STYLE_NORMAL) == [[u'zhong'], [u'xin']]
    assert pinyin(hans, STYLE_TONE) == [[u'zh\u014dng'], [u'x\u012bn']]
    assert pinyin(hans, STYLE_TONE2) == [[u'zho1ng'], [u'xi1n']]
    assert pinyin(hans, STYLE_INITIALS) == [['zh'], ['x']]
    assert pinyin(hans, STYLE_FIRST_LETTER) == [[u'z'], [u'x']]
    assert pinyin(hans, heteronym=True) == [[u'zh\u014dng', u'zh\xf2ng'],
                                            [u'x\u012bn']]
    assert pinyin(hans, style=STYLE_FINALS) == [['ong'], ['in']]
    assert pinyin(hans, style=STYLE_FINALS_TONE) == [[u'\u014dng'],
                                                     [u'\u012bn']]
    assert pinyin(hans, style=STYLE_FINALS_TONE2) == [[u'o1ng'], [u'i1n']]


def test_pinyin_finals():
    hans = u'嗷嗷'
    assert pinyin(hans) == [[u'\xe1o'], [u'\xe1o']]
    assert pinyin(hans + 'abc') == [[u'\xe1o'], [u'\xe1o'], [u'abc']]
    assert pinyin(hans, STYLE_NORMAL) == [[u'ao'], [u'ao']]
    assert pinyin(hans, STYLE_TONE) == [[u'\xe1o'], [u'\xe1o']]
    assert pinyin(hans, STYLE_TONE2) == [[u'a2o'], [u'a2o']]
    assert pinyin(hans, STYLE_INITIALS) == [[''], ['']]
    assert pinyin(hans, STYLE_FIRST_LETTER) == [[u'a'], [u'a']]
    assert pinyin(hans, heteronym=True) == [[u'\xe1o'], [u'\xe1o']]
    assert pinyin(u'啊', heteronym=True) == [[u'\u0101', u'\xe1',
                                              u'\u01ce', u'\xe0', u'a']]
    assert pinyin(hans, style=STYLE_FINALS) == [['ao'], ['ao']]
    assert pinyin(hans, style=STYLE_FINALS_TONE) == [[u'\xe1o'], [u'\xe1o']]
    assert pinyin(hans, style=STYLE_FINALS_TONE2) == [[u'a2o'], [u'a2o']]


def test_slug():
    hans = u'中心'
    assert slug(hans) == 'zhong-xin'
