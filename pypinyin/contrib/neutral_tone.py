# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from pypinyin import Style
from pypinyin.contrib._tone_rule import right_mark_index

_NUMBER_TONE = (Style.TONE2, Style.TONE3, Style.FINALS_TONE2,
                Style.FINALS_TONE3)

_re_number = re.compile(r'\d')


class NeutralToneWith5Mixin(object):
    """声调使用数字表示的相关拼音风格下的结果使用 5 标识轻声。

    使用方法::

        from pypinyin import lazy_pinyin, Style
        from pypinyin.contrib.neutral_tone import NeutralToneWith5Mixin
        from pypinyin.converter import DefaultConverter
        from pypinyin.core import Pinyin

        # 原来的结果中不会标识轻声
        print(lazy_pinyin('好了', style=Style.TONE2))
        # 输出: ['ha3o', 'le']


        class MyConverter(NeutralToneWith5Mixin, DefaultConverter):
            pass

        my_pinyin = Pinyin(MyConverter())
        pinyin = my_pinyin.pinyin
        lazy_pinyin = my_pinyin.lazy_pinyin

        #  新的结果中使用 ``5`` 标识轻声
        print(lazy_pinyin('好了', style=Style.TONE2))
        # 输出: ['ha3o', 'le5']

        print(pinyin('好了', style=Style.TONE2))
        # 输出：[['ha3o'], ['le5']]


    """

    def post_convert_style(self, han, orig_pinyin, converted_pinyin,
                           style, strict, **kwargs):
        data = super(NeutralToneWith5Mixin, self).post_convert_style(
            han, orig_pinyin, converted_pinyin, style, strict, **kwargs)

        if style not in _NUMBER_TONE:
            return data

        converted_pinyin = data or converted_pinyin
        if _re_number.search(converted_pinyin):
            if data is None:
                return data
            return converted_pinyin

        mark_index = right_mark_index(converted_pinyin)
        return '{}5{}'.format(converted_pinyin[:mark_index + 1],
                              converted_pinyin[mark_index + 1:])
