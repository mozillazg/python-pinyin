#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pytest

from pypinyin import (
    pinyin_group, load_phrases_dict, Style
)


def test_pinyin_group_basic():
    """测试基本的分组功能"""
    # 测试单个汉字
    result = pinyin_group('中')
    assert len(result) == 1
    assert result[0]['hanzi'] == '中'
    assert len(result[0]['pinyin']) == 1


def test_pinyin_group_with_phrase():
    """测试词语分组"""
    # 测试词语
    result = pinyin_group('你好')
    assert len(result) == 1
    assert result[0]['hanzi'] == '你好'
    assert len(result[0]['pinyin']) == 1


def test_pinyin_group_with_punctuation():
    """测试标点符号处理"""
    # 加载词语
    load_phrases_dict({
        '你好': [['nǐ'], ['hǎo']],
    })
    
    result = pinyin_group('你好吗？')
    assert len(result) == 3
    
    # 第一个分组：你好
    assert result[0]['hanzi'] == '你好'
    assert len(result[0]['pinyin']) == 1
    assert 'hǎo' in result[0]['pinyin'][0] or 'hao' in result[0]['pinyin'][0]
    
    # 第二个分组：吗
    assert result[1]['hanzi'] == '吗'
    assert len(result[1]['pinyin']) == 1
    
    # 第三个分组：？（标点）
    assert result[2]['hanzi'] == '？'
    assert result[2]['pinyin'] == []


def test_pinyin_group_with_apostrophe():
    """测试隔音符处理"""
    # 加载西安词语
    load_phrases_dict({
        '西安': [['xī'], ['ān']],
    })
    
    result = pinyin_group('西安', style=Style.NORMAL)
    assert len(result) == 1
    assert result[0]['hanzi'] == '西安'
    assert len(result[0]['pinyin']) == 1
    # 应该有隔音符
    assert "'" in result[0]['pinyin'][0]
    assert result[0]['pinyin'][0] == "xi'an"


def test_pinyin_group_with_erhua():
    """测试儿化音处理"""
    result = pinyin_group('花儿', style=Style.NORMAL)
    assert len(result) == 1
    assert result[0]['hanzi'] == '花儿'
    assert len(result[0]['pinyin']) == 1
    # 儿化音应该合并为 huar
    assert result[0]['pinyin'][0] == 'huar'


def test_pinyin_group_with_erhua_tone():
    """测试儿化音带声调"""
    result = pinyin_group('花儿', style=Style.TONE)
    assert len(result) == 1
    assert result[0]['hanzi'] == '花儿'
    assert len(result[0]['pinyin']) == 1
    # 儿化音应该合并
    assert 'r' in result[0]['pinyin'][0]


def test_pinyin_group_heteronym():
    """测试多音字模式"""
    result = pinyin_group('中', heteronym=True)
    assert len(result) == 1
    assert result[0]['hanzi'] == '中'
    # 中有多个读音
    assert len(result[0]['pinyin']) > 1


def test_pinyin_group_style_normal():
    """测试 NORMAL 风格"""
    result = pinyin_group('你好', style=Style.NORMAL)
    assert len(result) == 1
    # NORMAL 风格没有声调
    pinyin_str = result[0]['pinyin'][0]
    # 检查是否没有声调符号
    assert all(c not in pinyin_str for c in 'āáǎàēéěèīíǐìōóǒòūúǔù')


def test_pinyin_group_style_tone():
    """测试 TONE 风格（默认）"""
    result = pinyin_group('你好', style=Style.TONE)
    assert len(result) == 1
    # TONE 风格有声调
    pinyin_str = result[0]['pinyin'][0]
    # 应该包含声调符号
    has_tone = any(c in pinyin_str for c in 'āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ')
    assert has_tone


def test_pinyin_group_multiple_erhua():
    """测试多个字带儿化音"""
    # 测试 小孩儿
    load_phrases_dict({
        '小孩': [['xiǎo'], ['hái']],
    })
    
    result = pinyin_group('小孩儿', style=Style.NORMAL)
    assert len(result) == 1
    assert result[0]['hanzi'] == '小孩儿'
    assert len(result[0]['pinyin']) == 1
    # 应该是 xiao hair
    assert 'hair' in result[0]['pinyin'][0]


def test_pinyin_group_mixed():
    """测试混合场景"""
    load_phrases_dict({
        '天安门': [['tiān'], ['ān'], ['mén']],
    })
    
    result = pinyin_group('天安门', style=Style.NORMAL)
    assert len(result) == 1
    assert result[0]['hanzi'] == '天安门'
    assert len(result[0]['pinyin']) == 1
    # 应该有隔音符和空格
    pinyin_str = result[0]['pinyin'][0]
    assert "'" in pinyin_str  # 隔音符
    assert ' ' in pinyin_str  # 空格


def test_pinyin_group_with_english():
    """测试包含英文的情况"""
    result = pinyin_group('你好world')
    # 应该有两个分组
    assert len(result) >= 2
    # 找到 world 的分组
    world_group = [g for g in result if 'world' in g['hanzi'].lower()]
    assert len(world_group) == 1
    # 英文应该没有拼音
    assert world_group[0]['pinyin'] == []


def test_pinyin_group_with_list_input():
    """测试列表输入（跳过分词）"""
    # 测试字符串列表输入
    result = pinyin_group(['你好', '吗'], style=Style.NORMAL)
    assert len(result) == 2
    assert result[0]['hanzi'] == '你好'
    assert result[1]['hanzi'] == '吗'


def test_pinyin_group_with_list_erhua():
    """测试列表输入的儿化音处理"""
    result = pinyin_group(['玩', '儿'], style=Style.NORMAL)
    # 儿化音应该被合并
    assert len(result) == 1
    assert result[0]['hanzi'] == '玩儿'
    assert 'r' in result[0]['pinyin'][0]


def test_pinyin_group_method_exists():
    """测试 Pinyin 类有 pinyin_group 方法"""
    from pypinyin.core import Pinyin
    from pypinyin.converter import DefaultConverter
    
    p = Pinyin(DefaultConverter())
    assert hasattr(p, 'pinyin_group')
    
    # 测试方法可以调用
    result = p.pinyin_group('你好', style=Style.NORMAL)
    assert len(result) == 1
    assert result[0]['hanzi'] == '你好'

