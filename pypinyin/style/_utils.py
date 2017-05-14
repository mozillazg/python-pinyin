# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pypinyin.standard import convert_finals
from pypinyin.style._constants import (
    _INITIALS, _INITIALS_NOT_STRICT,
    RE_PHONETIC_SYMBOL, PHONETIC_SYMBOL_DICT,
    RE_NUMBER
)


def get_initials(pinyin, strict):
    """获取单个拼音中的声母.

    :param pinyin: 单个拼音
    :type pinyin: unicode
    :param strict: 是否严格遵照《汉语拼音方案》来处理声母和韵母
    :return: 声母
    :rtype: unicode
    """
    if strict:
        _initials = _INITIALS
    else:
        _initials = _INITIALS_NOT_STRICT

    for i in _initials:
        if pinyin.startswith(i):
            return i
    return ''


def get_finals(pinyin, strict):
    """获取单个拼音中的韵母.

    :param pinyin: 单个拼音
    :type pinyin: unicode
    :param strict: 是否严格遵照《汉语拼音方案》来处理声母和韵母
    :return: 韵母
    :rtype: unicode
    """
    if strict:
        pinyin = convert_finals(pinyin)

    initials = get_initials(pinyin, strict=strict) or ''
    # 没有声母，整个都是韵母
    if not initials:
        return pinyin
    # 按声母分割，剩下的就是韵母
    return ''.join(pinyin.split(initials, 1))


def replace_symbol_to_number(pinyin):
    """把声调替换为数字"""
    def _replace(match):
        symbol = match.group(0)  # 带声调的字符
        # 返回使用数字标识声调的字符
        return PHONETIC_SYMBOL_DICT[symbol]

    # 替换拼音中的带声调字符
    return RE_PHONETIC_SYMBOL.sub(_replace, pinyin)


def replace_symbol_to_no_symbol(pinyin):
    """把带声调字符替换为没有声调的字符"""
    def _replace(match):
        symbol = match.group(0)  # 带声调的字符
        # 去掉声调: a1 -> a
        return RE_NUMBER.sub(r'', PHONETIC_SYMBOL_DICT[symbol])

    # 替换拼音中的带声调字符
    return RE_PHONETIC_SYMBOL.sub(_replace, pinyin)


def has_finals(pinyin):
    """判断是否有韵母"""
    # 鼻音: 'ḿ', 'ń', 'ň', 'ǹ ' 没有韵母
    for symbol in ['\u1e3f', '\u0144', '\u0148', '\u01f9']:
        if symbol in pinyin:
            return False

    return True
