# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pypinyin.standard import convert_finals
from pypinyin.style._constants import (
    _INITIALS, _INITIALS_NOT_STRICT, _FINALS,
    RE_PHONETIC_SYMBOL, PHONETIC_SYMBOL_DICT,
    PHONETIC_SYMBOL_DICT_KEY_LENGTH_NOT_ONE,
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

    :param pinyin: 单个拼音，无声调拼音
    :type pinyin: unicode
    :param strict: 是否严格遵照《汉语拼音方案》来处理声母和韵母
    :return: 韵母
    :rtype: unicode
    """
    if strict:
        pinyin = convert_finals(pinyin)

    initials = get_initials(pinyin, strict=strict) or ''

    # 按声母分割，剩下的就是韵母
    finals = pinyin[len(initials):]

    # 处理既没有声母也没有韵母的情况
    if strict and finals not in _FINALS:
        # 处理 y, w 导致误判的问题，比如 yo
        initials = get_initials(pinyin, strict=False)
        finals = pinyin[len(initials):]
        if finals in _FINALS:
            return finals
        return ''

    # ń, ḿ, ńg（嗯 等）：非严格模式下整个音节作为韵母。
    # 其中 ńg 会被切出声母 n，剩下的 'g' 不是有效韵母，需要特殊处理；
    # get_initials('ng', strict=False) 仍会返回 'n'，这里与 m/n 的现有行为一致。
    if not strict and (not finals or pinyin == 'ng'):
        return pinyin

    return finals


def replace_symbol_to_number(pinyin):
    """把声调替换为数字"""
    def _replace(match):
        symbol = match.group(0)  # 带声调的字符
        # 返回使用数字标识声调的字符
        return PHONETIC_SYMBOL_DICT[symbol]

    # 替换拼音中的带声调字符
    value = RE_PHONETIC_SYMBOL.sub(_replace, pinyin)
    for symbol, to in PHONETIC_SYMBOL_DICT_KEY_LENGTH_NOT_ONE.items():
        value = value.replace(symbol, to)

    return value


def replace_symbol_to_no_symbol(pinyin):
    """把带声调字符替换为没有声调的字符"""
    value = replace_symbol_to_number(pinyin)
    return RE_NUMBER.sub('', value)


# 鼻音: 'm̄', 'ḿ', 'm̀', 'ń', 'ň', 'ǹ' 没有韵母
_NO_FINALS_SYMBOLS = ('m̄', 'ḿ', 'm̀', 'ń', 'ň', 'ǹ')


def has_finals(pinyin):
    """判断是否有韵母"""
    for symbol in _NO_FINALS_SYMBOLS:
        if symbol in pinyin:
            return False

    return True
