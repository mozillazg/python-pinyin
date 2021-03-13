# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from pypinyin.contrib._tone_rule import right_mark_index
from pypinyin.style._constants import RE_TONE3
from pypinyin.style.tone import converter
from pypinyin.utils import _replace_tone2_style_dict_to_default

_re_number = re.compile(r'\d')


def to_normal(pinyin, v_to_u=False):
    """将 :py:attr:`~pypinyin.Style.TONE`、
    :py:attr:`~pypinyin.Style.TONE2` 或
    :py:attr:`~pypinyin.Style.TONE3` 风格的拼音转换为
    :py:attr:`~pypinyin.Style.NORMAL` 风格的拼音

    :param pinyin: :py:attr:`~pypinyin.Style.TONE`、
                   :py:attr:`~pypinyin.Style.TONE2` 或
                   :py:attr:`~pypinyin.Style.TONE3` 风格的拼音
    :param v_to_u: 是否使用 ``ü`` 代替原来的 ``v``
    :return: :py:attr:`~pypinyin.Style.NORMAL` 风格的拼音

    Usage::

        >>> from pypinyin.contrib.tone_convert import to_normal
        >>> to_normal('zhōng')
        'zhong'
        >>> to_normal('zho1ng')
        'zhong'
        >>> to_normal('zhong1')
        'zhong'
        >>> to_normal('lüè', v_to_u=True)
        'lüe'
    """
    s = tone_to_tone2(pinyin, v_to_u=True)
    s = tone2_to_normal(s)
    return _fix_v_u(pinyin, s, v_to_u)


def to_tone(pinyin):
    """将 :py:attr:`~pypinyin.Style.TONE2` 或
    :py:attr:`~pypinyin.Style.TONE3` 风格的拼音转换为
    :py:attr:`~pypinyin.Style.TONE` 风格的拼音

    :param pinyin: :py:attr:`~pypinyin.Style.TONE2` 或
                   :py:attr:`~pypinyin.Style.TONE3` 风格的拼音
    :return: :py:attr:`~pypinyin.Style.TONE` 风格的拼音

    Usage::

        >>> from pypinyin.contrib.tone_convert import to_tone
        >>> to_tone('zho1ng')
        'zhōng'
        >>> to_tone('zhong1')
        'zhōng'
    """
    if not _re_number.search(pinyin):
        return pinyin

    s = tone_to_tone2(pinyin)
    s = tone2_to_tone(s)
    return s


def to_tone2(pinyin, v_to_u=False, neutral_tone_with_5=False):
    """将 :py:attr:`~pypinyin.Style.TONE` 或
    :py:attr:`~pypinyin.Style.TONE3` 风格的拼音转换为
    :py:attr:`~pypinyin.Style.TONE2` 风格的拼音

    :param pinyin: :py:attr:`~pypinyin.Style.TONE` 或
                   :py:attr:`~pypinyin.Style.TONE3` 风格的拼音
    :param v_to_u: 是否使用 ``ü`` 代替原来的 ``v``
    :param neutral_tone_with_5: 是否使用 ``5`` 标识轻声
    :return: :py:attr:`~pypinyin.Style.TONE2` 风格的拼音

    Usage::

        >>> from pypinyin.contrib.tone_convert import to_tone2
        >>> to_tone2('zhōng')
        'zho1ng'
        >>> to_tone2('zhong1')
        'zho1ng'
        >>> to_tone2('shang', neutral_tone_with_5=True)
        'sha5ng'
        >>> to_tone2('lüè', v_to_u=True)
        'lüe4'
    """
    s = tone_to_tone3(
        pinyin, v_to_u=True, neutral_tone_with_5=neutral_tone_with_5)
    s = tone3_to_tone2(s)
    return _fix_v_u(pinyin, s, v_to_u)


def to_tone3(pinyin, v_to_u=False, neutral_tone_with_5=False):
    """将 :py:attr:`~pypinyin.Style.TONE` 或
    :py:attr:`~pypinyin.Style.TONE2` 风格的拼音转换为
    :py:attr:`~pypinyin.Style.TONE3` 风格的拼音

    :param pinyin: :py:attr:`~pypinyin.Style.TONE` 或
                   :py:attr:`~pypinyin.Style.TONE2` 风格的拼音
    :param v_to_u: 是否使用 ``ü`` 代替原来的 ``v``
    :param neutral_tone_with_5: 是否使用 ``5`` 标识轻声
    :return: :py:attr:`~pypinyin.Style.TONE2` 风格的拼音

    Usage::

        >>> from pypinyin.contrib.tone_convert import to_tone3
        >>> to_tone3('zhōng')
        'zhong1'
        >>> to_tone3('zho1ng')
        'zhong1'
        >>> to_tone3('shang', neutral_tone_with_5=True)
        'shang5'
        >>> to_tone3('lüè', v_to_u=True)
        'lüe4'
    """
    s = tone_to_tone2(
        pinyin, v_to_u=True, neutral_tone_with_5=neutral_tone_with_5)
    s = tone2_to_tone3(s)
    return _fix_v_u(pinyin, s, v_to_u)


def tone_to_normal(tone, v_to_u=False):
    """将 :py:attr:`~pypinyin.Style.TONE` 风格的拼音转换为
    :py:attr:`~pypinyin.Style.NORMAL` 风格的拼音

    :param tone: :py:attr:`~pypinyin.Style.TONE` 风格的拼音
    :param v_to_u: 是否使用 ``ü`` 代替原来的 ``v``
    :return: :py:attr:`~pypinyin.Style.NORMAL` 风格的拼音

    Usage::

        >>> from pypinyin.contrib.tone_convert import tone_to_normal
        >>> tone_to_normal('zhōng')
        'zhong'
        >>> tone_to_normal('lüè', v_to_u=True)
        'lüe'
    """
    s = tone_to_tone2(tone, v_to_u=v_to_u)
    s = _re_number.sub('', s)
    return _v_to_u(s, v_to_u)


def tone_to_tone2(tone, v_to_u=False, neutral_tone_with_5=False):
    """将 :py:attr:`~pypinyin.Style.TONE` 风格的拼音转换为
    :py:attr:`~pypinyin.Style.TONE2` 风格的拼音

    :param tone: :py:attr:`~pypinyin.Style.TONE` 风格的拼音
    :param v_to_u: 是否使用 ``ü`` 代替原来的 ``v``
    :param neutral_tone_with_5: 是否使用 ``5`` 标识轻声
    :return: :py:attr:`~pypinyin.Style.TONE2` 风格的拼音

    Usage::

        >>> from pypinyin.contrib.tone_convert import tone_to_tone2
        >>> tone_to_tone2('zhōng')
        'zho1ng'
        >>> tone_to_tone2('shang', neutral_tone_with_5=True)
        'sha5ng'
        >>> tone_to_tone2('lüè', v_to_u=True)
        'lüe4'
    """
    tone3 = tone_to_tone3(
        tone, v_to_u=v_to_u, neutral_tone_with_5=neutral_tone_with_5)
    s = tone3_to_tone2(tone3)
    return _v_to_u(s, v_to_u)


def tone_to_tone3(tone, v_to_u=False, neutral_tone_with_5=False):
    """将 :py:attr:`~pypinyin.Style.TONE` 风格的拼音转换为
    :py:attr:`~pypinyin.Style.TONE3` 风格的拼音

    :param tone: :py:attr:`~pypinyin.Style.TONE` 风格的拼音
    :param v_to_u: 是否使用 ``ü`` 代替原来的 ``v``
    :param neutral_tone_with_5: 是否使用 ``5`` 标识轻声
    :return: :py:attr:`~pypinyin.Style.TONE3` 风格的拼音

    Usage::

        >>> from pypinyin.contrib.tone_convert import tone_to_tone3
        >>> tone_to_tone3('zhōng')
        'zhong1'
        >>> tone_to_tone3('shang', neutral_tone_with_5=True)
        'shang5'
        >>> tone_to_tone3('lüè', v_to_u=True)
        'lüe4'
    """
    tone3 = converter.to_tone3(tone)
    s = _improve_tone3(tone3, neutral_tone_with_5=neutral_tone_with_5)
    return _v_to_u(s, v_to_u)


def tone2_to_normal(tone2, v_to_u=False):
    """将 :py:attr:`~pypinyin.Style.TONE2` 风格的拼音转换为
    :py:attr:`~pypinyin.Style.NORMAL` 风格的拼音

    :param tone2: :py:attr:`~pypinyin.Style.TONE2` 风格的拼音
    :param v_to_u: 是否使用 ``ü`` 代替原来的 ``v``
    :return: Style.NORMAL 风格的拼音

    Usage::

        >>> from pypinyin.contrib.tone_convert import tone2_to_normal
        >>> tone2_to_normal('zho1ng')
        'zhong'
        >>> tone2_to_normal('lüe4', v_to_u=True)
        'lüe'
    """
    s = _re_number.sub('', tone2)
    return _v_to_u(s, v_to_u)


def tone2_to_tone(tone2):
    """将 :py:attr:`~pypinyin.Style.TONE2` 风格的拼音转换为
    :py:attr:`~pypinyin.Style.TONE` 风格的拼音

    :param tone2: :py:attr:`~pypinyin.Style.TONE2` 风格的拼音
    :return: Style.TONE 风格的拼音

    Usage::

        >>> from pypinyin.contrib.tone_convert import tone2_to_tone
        >>> tone2_to_tone('zho1ng')
        'zhōng'
    """
    return _replace_tone2_style_dict_to_default(tone2)


def tone2_to_tone3(tone2):
    """将 :py:attr:`~pypinyin.Style.TONE2` 风格的拼音转换为
    :py:attr:`~pypinyin.Style.TONE3` 风格的拼音

    :param tone2: :py:attr:`~pypinyin.Style.TONE2` 风格的拼音
    :return: :py:attr:`~pypinyin.Style.TONE3` 风格的拼音

    Usage::

        >>> from pypinyin.contrib.tone_convert import tone2_to_tone3
        >>> tone2_to_tone3('zho1ng')
        'zhong1'
    """
    tone3 = RE_TONE3.sub(r'\1\3\2', tone2)
    return tone3


def tone3_to_normal(tone3, v_to_u=False):
    """将 :py:attr:`~pypinyin.Style.TONE3` 风格的拼音转换为
    :py:attr:`~pypinyin.Style.NORMAL` 风格的拼音

    :param tone3: :py:attr:`~pypinyin.Style.TONE3` 风格的拼音
    :param v_to_u: 是否使用 ``ü`` 代替原来的 ``v``
    :return: :py:attr:`~pypinyin.Style.NORMAL` 风格的拼音

    Usage::

        >>> from pypinyin.contrib.tone_convert import tone3_to_normal
        >>> tone3_to_normal('zhong1')
        'zhong'
        >>> tone3_to_normal('lüe4', v_to_u=True)
        'lüe'
    """
    s = _re_number.sub('', tone3)
    return _v_to_u(s, v_to_u)


def tone3_to_tone(tone3):
    """将 :py:attr:`~pypinyin.Style.TONE3` 风格的拼音转换为
    :py:attr:`~pypinyin.Style.TONE` 风格的拼音

    :param tone3: :py:attr:`~pypinyin.Style.TONE3` 风格的拼音
    :return: :py:attr:`~pypinyin.Style.TONE` 风格的拼音

    Usage::

        >>> from pypinyin.contrib.tone_convert import tone3_to_tone
        >>> tone3_to_tone('zhong1')
        'zhōng'
    """
    tone2 = tone3_to_tone2(tone3)
    return tone2_to_tone(tone2)


def tone3_to_tone2(tone3):
    """将 :py:attr:`~pypinyin.Style.TONE3` 风格的拼音转换为
    :py:attr:`~pypinyin.Style.TONE2` 风格的拼音

    :param tone3: :py:attr:`~pypinyin.Style.TONE3` 风格的拼音
    :return: :py:attr:`~pypinyin.Style.TONE2` 风格的拼音

    Usage::

        >>> from pypinyin.contrib.tone_convert import tone3_to_tone2
        >>> tone3_to_tone2('zhong1')
        'zho1ng'
    """
    no_number_tone3 = tone3_to_normal(tone3)
    mark_index = right_mark_index(no_number_tone3)
    if mark_index is None:
        mark_index = len(no_number_tone3) - 1
    before = no_number_tone3[:mark_index + 1]
    after = no_number_tone3[mark_index + 1:]

    number = _get_number_from_pinyin(tone3)
    if number is None:
        return tone3

    return '{}{}{}'.format(before, number, after)


def _improve_tone3(tone3, neutral_tone_with_5=False):
    number = _get_number_from_pinyin(tone3)
    if number is None and neutral_tone_with_5:
        tone3 = '{}5'.format(tone3)
    return tone3


def _get_number_from_pinyin(pinyin):
    numbers = _re_number.findall(pinyin)
    if numbers:
        number = numbers[0]
    else:
        number = None
    return number


def _v_to_u(pinyin, replace=False):
    if not replace:
        return pinyin
    return pinyin.replace('v', 'ü')


def _fix_v_u(origin_py, new_py, v_to_u):
    if not v_to_u:
        if 'ü' in new_py and 'ü' not in origin_py:
            return new_py.replace('ü', 'v')

    return _v_to_u(new_py, replace=True)
