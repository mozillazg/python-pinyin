# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from pypinyin import pinyin, load_phrases_dict
from pypinyin.contrib import mmseg


seg_test = mmseg.Seg(mmseg.PrefixSet())
seg_test._prefix_set.train([
    'a',
    'ab',
    'abc',
    'abcd',
    'abd',
    'ac',
    'acd',
    'aff',
    'agf',
    'agfgef',
    'asdf',
    'bbs'
    '中国',
    '中国人',
    '中国人民',
    '中国人民银行',
    '我',
    '北京',
    '天安门',
    '员工',
])


@pytest.mark.parametrize(
    'input, expect', [
        ['', []],
        ['a', ['a']],
        ['abc', ['abc']],
        ['abcefg', ['abc', 'e', 'f', 'g']],
        ['bbcabce', ['bb', 'c', 'abc', 'e']],
        ['北京', ['北京']],
        ['北京,', ['北京', ',']],
        ['北京abc', ['北京', 'abc']],
        ['中国人民银行行长', ['中国人民银行', '行', '长']],
        ['中国人民银行员工', ['中国人民银行', '员工']],
        [
            'abcadbasfgafgasdabcagfaff我是中国人中国人民我爱北京天安门',
            [
                'abc',
                'a',
                'd',
                'b',
                'as',
                'f',
                'g',
                'af',
                'g',
                'asd',
                'abc',
                'agf',
                'aff',
                '我',
                '是',
                '中国人',
                '中国人民',
                '我',
                '爱',
                '北京',
                '天安门',
            ],
         ],
    ]
)
def test_mmseg(input, expect):
    assert list(seg_test.cut(input)) == expect


@pytest.mark.parametrize(
    'input, default_ret, mmseg_ret', [
        [
            '一语中的啊',
            [['yī'], ['yǔ'], ['zhōng'], ['de'], ['a']],
            [['yī'], ['yǔ'], ['zhòng'], ['dì'], ['a']],
        ],
    ]
)
def test_mmseg_for_pinyin(input, default_ret, mmseg_ret):
    assert pinyin(input) == mmseg_ret
    assert pinyin(mmseg.seg.cut(input)) == mmseg_ret


@pytest.mark.parametrize(
    'input, jieba_ret, mmseg_ret', [
        [
            '了局啊',
            [['le'], ['jú'], ['a']],
            [['liǎo'], ['jú'], ['a']],
        ],
    ]
)
def test_mmseg_and_jieba_for_pinyin(input, jieba_ret, mmseg_ret):
    assert pinyin(input) == mmseg_ret
    assert pinyin(mmseg.seg.cut(input)) == mmseg_ret


def test_retrain():
    seg = mmseg.seg
    assert list(seg.cut('啊啊啊')) == ['啊', '啊', '啊']

    load_phrases_dict({'啊啊啊': [['a'], ['a'], ['a']]})
    mmseg.retrain(seg)
    assert list(seg.cut('啊啊啊')) == ['啊啊啊']
