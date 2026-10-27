# -*- coding: utf-8 -*-
"""自定义词典与多音字组合：上游只测了桔/同行的基础覆盖，
本文件用上游从未用过的生僻字 㐀/㐁（默认读音 qiū/tiàn），
每个测试开头先把自己需要的词典状态写回去，保证单测可独立运行、
且不影响上游其他测试（上游全文无 㐀/㐁）。

文件名带 zz：本目录内最后执行，进一步降低对其他文件的干扰。
"""
from __future__ import unicode_literals

from pypinyin import pinyin, lazy_pinyin, Style, load_single_dict, load_phrases_dict
from pypinyin.seg.simpleseg import seg


def test_custom_single_dict_default_reading_first():
    load_single_dict({ord('㐀'): 'qiū'})
    assert lazy_pinyin('㐀') == ['qiu']


def test_custom_single_dict_heteronym_all_readings():
    load_single_dict({ord('㐀'): 'ā,ē,à'})
    assert pinyin('㐀', heteronym=True) == [['ā', 'ē', 'à']]
    assert pinyin('㐀') == [['ā']]
    assert pinyin('㐀', heteronym=True, style=Style.TONE2) == [
        ['a1', 'e1', 'a4']]


def test_custom_single_dict_unknown_style_falls_back_to_default():
    # 实测：style 传未知值不报错，按 default 分支直接更新词典。
    load_single_dict({ord('㐁'): 'bà'}, style='bogus')
    assert lazy_pinyin('㐁') == ['ba']


def test_custom_phrases_dict_basic_and_seg():
    load_single_dict({ord('㐀'): 'ā'})
    load_single_dict({ord('㐁'): 'bà'})
    load_phrases_dict({'㐀㐁': [['ā'], ['bà']]})
    assert pinyin('㐀㐁') == [['ā'], ['bà']]
    # 载入词组后分词会把两字切成一个片段（载入前是 ['㐀', '㐁']）。
    assert seg('㐀㐁') == ['㐀㐁']


def test_custom_phrases_dict_heteronym_multi_reading():
    load_phrases_dict({'㐀㐁': [['ā', 'á'], ['bà']]})
    assert pinyin('㐀㐁', heteronym=True) == [['ā', 'á'], ['bà']]
    assert pinyin('㐀㐁') == [['ā'], ['bà']]


def test_custom_phrases_dict_tone2_style():
    load_phrases_dict({'㐀㐁': [['to4ng'], ['ku1']]}, style='tone2')
    assert pinyin('㐀㐁') == [['tòng'], ['kū']]
