# -*- coding: utf-8 -*-
"""韵母相关拼音风格:

Style.FINALS
Style.FINALS_TONE
Style.FINALS_TONE2
Style.FINALS_TONE3
"""
from __future__ import unicode_literals

from pypinyin.constants import Style
from pypinyin.style import register
from pypinyin.style._constants import RE_NUMBER
from pypinyin.style._tone_convert import (
    tone3_to_tone2, tone2_to_tone, to_finals
)
from pypinyin.style._utils import replace_symbol_to_number


class FinalsConverter(object):
    def to_finals(self, pinyin, **kwargs):
        """无声调韵母"""
        return to_finals(pinyin, strict=kwargs.get('strict', True))

    def to_finals_tone(self, pinyin, **kwargs):
        """声调在韵母头上"""
        finals = self.to_finals_tone2(pinyin, **kwargs)

        finals = tone2_to_tone(finals)

        return finals

    def to_finals_tone2(self, pinyin, **kwargs):
        """数字声调"""
        finals = self.to_finals_tone3(pinyin, **kwargs)

        finals = tone3_to_tone2(finals)

        return finals

    def to_finals_tone3(self, pinyin, **kwargs):
        """数字声调"""
        finals = self.to_finals(pinyin, **kwargs)
        if not finals:
            return finals

        numbers = RE_NUMBER.findall(replace_symbol_to_number(pinyin))
        if not numbers:
            return finals

        number = numbers[0]
        finals = finals + number

        return finals


converter = FinalsConverter()
register(Style.FINALS, func=converter.to_finals)
register(Style.FINALS_TONE, func=converter.to_finals_tone)
register(Style.FINALS_TONE2, func=converter.to_finals_tone2)
register(Style.FINALS_TONE3, func=converter.to_finals_tone3)
