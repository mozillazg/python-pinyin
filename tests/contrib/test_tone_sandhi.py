# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pytest import mark

from pypinyin import lazy_pinyin
from pypinyin.constants import Style
from pypinyin.contrib.tone_sandhi import ToneSandhiMixin
from pypinyin.converter import DefaultConverter
from pypinyin.core import Pinyin


class MyConverter(ToneSandhiMixin, DefaultConverter):
    pass


my_pinyin = Pinyin(MyConverter())


@mark.parametrize('han,normal_output, sandhi_output', [
    # 三声变调
    [['你好'], ['ni3', 'ha3o'], ['ni2', 'ha3o']],
    [['老鼠'], ['la3o', 'shu3'], ['la2o', 'shu3']],
    [['保管好'], ['ba3o', 'gua3n', 'ha3o'], ['ba2o', 'gua2n', 'ha3o']],
    # [['保管', '好'], ['ba3o', 'gua3n', 'ha3o'], ['ba2o', 'gua2n', 'ha3o']],
    # [['老保管'], ['la3o', 'ba3o', 'gua3n'], ['la3o', 'ba2o', 'gua3n']],
    [['老', '保管'], ['la3o', 'ba3o', 'gua3n'], ['la3o', 'ba2o', 'gua3n']],
    [['九九九'], ['jiu3', 'jiu3', 'jiu3'], ['jiu2', 'jiu2', 'jiu3']],

    # 不满足变调条件
    [['你这'], ['ni3', 'zhe4'], ['ni3', 'zhe4']],
    [['你'], ['ni3'], ['ni3']],

    # 【不】 变调
    [['不是'], ['bu4', 'shi4'], ['bu2', 'shi4']],
    [['不对'], ['bu4', 'dui4'], ['bu2', 'dui4']],

    # 不满足变调条件
    [['不好'], ['bu4', 'ha3o'], ['bu4', 'ha3o']],
    [['是不'], ['shi4', 'bu4'], ['shi4', 'bu4']],
    [['不'], ['bu4'], ['bu4']],

    # 【一】 变调
    [['一个'], ['yi1', 'ge4'], ['yi2', 'ge4']],
    [['一定'], ['yi1', 'di4ng'], ['yi2', 'di4ng']],
    [['一天'], ['yi1', 'tia1n'], ['yi4', 'tia1n']],
    [['一年'], ['yi1', 'nia2n'], ['yi4', 'nia2n']],
    [['一起'], ['yi1', 'qi3'], ['yi4', 'qi3']],

    # 不满足变调条件
    [['之一'], ['zhi1', 'yi1'], ['zhi1', 'yi1']],
    [['一'], ['yi1'], ['yi1']],
])
def test_tone_sandhi(han, normal_output, sandhi_output):
    assert lazy_pinyin(han, style=Style.TONE2) == normal_output or \
           lazy_pinyin(han, style=Style.TONE2) == sandhi_output

    assert my_pinyin.lazy_pinyin(han, style=Style.TONE2) == sandhi_output
    # 测试关键字参数
    assert lazy_pinyin(han, style=Style.TONE2,
                       tone_sandhi=True) == sandhi_output
    assert lazy_pinyin(han, style=Style.TONE2, v_to_u=True,
                       neutral_tone_with_five=True,
                       tone_sandhi=True) == sandhi_output
