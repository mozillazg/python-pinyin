#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from pypinyin import (
    pinyin_group, lazy_pinyin_group, load_phrases_dict, Style
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


def test_lazy_pinyin_group_basic():
    """测试 lazy_pinyin_group 基本功能"""
    result = lazy_pinyin_group('你好', style=Style.NORMAL)
    assert len(result) == 1
    assert result[0]['hanzi'] == '你好'
    # lazy_pinyin_group 的 pinyin 应该是字符串而不是列表
    assert isinstance(result[0]['pinyin'], str)
    assert result[0]['pinyin'] == 'ni hao'


def test_lazy_pinyin_group_with_punctuation():
    """测试 lazy_pinyin_group 标点符号处理"""
    load_phrases_dict({
        '你好': [['nǐ'], ['hǎo']],
    })

    result = lazy_pinyin_group('你好吗？', style=Style.NORMAL)
    assert len(result) == 3

    # 第一个分组：你好
    assert result[0]['hanzi'] == '你好'
    assert isinstance(result[0]['pinyin'], str)

    # 第二个分组：吗
    assert result[1]['hanzi'] == '吗'
    assert isinstance(result[1]['pinyin'], str)

    # 第三个分组：？（标点）
    assert result[2]['hanzi'] == '？'
    assert result[2]['pinyin'] == ''  # 空字符串而不是空列表


def test_lazy_pinyin_group_with_apostrophe():
    """测试 lazy_pinyin_group 隔音符处理"""
    load_phrases_dict({
        '西安': [['xī'], ['ān']],
    })

    result = lazy_pinyin_group('西安', style=Style.NORMAL)
    assert len(result) == 1
    assert result[0]['hanzi'] == '西安'
    assert isinstance(result[0]['pinyin'], str)
    assert "'" in result[0]['pinyin']
    assert result[0]['pinyin'] == "xi'an"


def test_lazy_pinyin_group_with_list_input():
    """测试 lazy_pinyin_group 列表输入"""
    result = lazy_pinyin_group(['你好', '吗'], style=Style.NORMAL)
    assert len(result) == 2
    assert result[0]['hanzi'] == '你好'
    assert isinstance(result[0]['pinyin'], str)
    assert result[1]['hanzi'] == '吗'
    assert isinstance(result[1]['pinyin'], str)


def test_lazy_pinyin_group_method_exists():
    """测试 Pinyin 类有 lazy_pinyin_group 方法"""
    from pypinyin.core import Pinyin
    from pypinyin.converter import DefaultConverter

    p = Pinyin(DefaultConverter())
    assert hasattr(p, 'lazy_pinyin_group')

    # 测试方法可以调用
    result = p.lazy_pinyin_group('你好', style=Style.NORMAL)
    assert len(result) == 1
    assert result[0]['hanzi'] == '你好'
    assert isinstance(result[0]['pinyin'], str)


def test_lazy_pinyin_group_vs_pinyin_group():
    """测试 lazy_pinyin_group 和 pinyin_group 的区别"""
    from pypinyin import pinyin_group

    text = '你好'
    result_lazy = lazy_pinyin_group(text, style=Style.NORMAL)
    result_normal = pinyin_group(text, style=Style.NORMAL)

    # 两者的汉字部分应该相同
    assert result_lazy[0]['hanzi'] == result_normal[0]['hanzi']

    # lazy_pinyin_group 返回字符串
    assert isinstance(result_lazy[0]['pinyin'], str)

    # pinyin_group 返回列表
    assert isinstance(result_normal[0]['pinyin'], list)

    # 内容应该相同（lazy 的字符串等于 normal 的第一个元素）
    assert result_lazy[0]['pinyin'] == result_normal[0]['pinyin'][0]


def test_pinyin_group_disable_apostrophe():
    """测试禁用隔音符"""
    # 加载西安词语
    load_phrases_dict({
        '西安': [['xī'], ['ān']],
    })

    result = pinyin_group(
        '西安', style=Style.NORMAL, enable_apostrophe=False)
    assert len(result) == 1
    assert result[0]['hanzi'] == '西安'
    assert len(result[0]['pinyin']) == 1
    # 应该没有隔音符，而是用空格
    assert "'" not in result[0]['pinyin'][0]
    assert result[0]['pinyin'][0] == 'xi an'


def test_lazy_pinyin_group_disable_apostrophe():
    """测试 lazy_pinyin_group 禁用隔音符"""
    load_phrases_dict({
        '西安': [['xī'], ['ān']],
    })

    result = lazy_pinyin_group(
        '西安', style=Style.NORMAL, enable_apostrophe=False)
    assert len(result) == 1
    assert result[0]['hanzi'] == '西安'
    assert isinstance(result[0]['pinyin'], str)
    # 应该没有隔音符
    assert "'" not in result[0]['pinyin']
    assert result[0]['pinyin'] == 'xi an'


def test_pinyin_group_chaoyang():
    """测试朝阳的分组拼音"""
    # 朝阳是一个词，且第一个字是多音字
    result = pinyin_group('朝阳', style=Style.NORMAL)
    assert len(result) == 1
    assert result[0]['hanzi'] == '朝阳'
    assert result[0]['pinyin'] == ['zhao yang']

    # 测试 lazy_pinyin_group
    result = lazy_pinyin_group('朝阳', style=Style.NORMAL)
    assert len(result) == 1
    assert result[0]['hanzi'] == '朝阳'
    assert result[0]['pinyin'] == 'zhao yang'
