#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from copy import deepcopy
from itertools import chain
import os

from pypinyin.compat import text_type, callable_check
from pypinyin.constants import (
    PHRASES_DICT, PINYIN_DICT,
    RE_HANS, TONE, NORMAL
)
from pypinyin.utils import simple_seg, _replace_tone2_style_dict_to_default
from pypinyin.style import auto_discover, convert

auto_discover()


def seg(hans):
    if getattr(seg, 'no_jieba', None):
        ret = hans
        return simple_seg(ret)

    if seg.jieba is None:
        try:
            import jieba
            seg.jieba = jieba
        except ImportError:
            seg.no_jieba = True
        return seg(hans)
    else:
        hans = simple_seg(hans)
        ret = []
        for x in hans:
            if not RE_HANS.match(x):   # 没有拼音的字符，不再参与二次分词
                ret.append(x)
            else:
                ret.extend(list(seg.jieba.cut(x)))
        return ret


seg.jieba = None
if os.environ.get('PYPINYIN_NO_JIEBA'):
    seg.no_jieba = True


def load_single_dict(pinyin_dict, style='default'):
    """载入用户自定义的单字拼音库

    :param pinyin_dict: 单字拼音库。比如： ``{0x963F: u"ā,ē"}``
    :param style: pinyin_dict 参数值的拼音库风格. 支持 'default', 'tone2'
    :type pinyin_dict: dict
    """
    if style == 'tone2':
        for k, v in pinyin_dict.items():
            v = _replace_tone2_style_dict_to_default(v)
            PINYIN_DICT[k] = v
    else:
        PINYIN_DICT.update(pinyin_dict)


def load_phrases_dict(phrases_dict, style='default'):
    """载入用户自定义的词语拼音库

    :param phrases_dict: 词语拼音库。比如： ``{u"阿爸": [[u"ā"], [u"bà"]]}``
    :param style: phrases_dict 参数值的拼音库风格. 支持 'default', 'tone2'
    :type phrases_dict: dict
    """
    if style == 'tone2':
        for k, value in phrases_dict.items():
            v = [
                list(map(_replace_tone2_style_dict_to_default, pys))
                for pys in value
            ]
            PHRASES_DICT[k] = v
    else:
        PHRASES_DICT.update(phrases_dict)


def to_fixed(pinyin, style, strict=True):
    """根据拼音风格格式化带声调的拼音.

    :param pinyin: 单个拼音
    :param style: 拼音风格
    :param strict: 是否严格遵照《汉语拼音方案》来处理声母和韵母
    :return: 根据拼音风格格式化后的拼音字符串
    :rtype: unicode
    """
    return convert(pinyin, style=style, strict=strict, default=pinyin)

    # # 韵母
    # elif style in [FINALS, FINALS_TONE, FINALS_TONE2, FINALS_TONE3]:
    #     # 不处理鼻音: 'ḿ', 'ń', 'ň', 'ǹ'
    #     if pinyin and pinyin[0] not in [
    #         '\u1e3f', '\u0144', '\u0148', '\u01f9'
    #     ]:
    #         py = final(py, strict=strict)


def _handle_nopinyin_char(chars, errors='default'):
    """处理没有拼音的字符"""
    if callable_check(errors):
        return errors(chars)

    if errors == 'default':
        return chars
    elif errors == 'ignore':
        return None
    elif errors == 'replace':
        if len(chars) > 1:
            return ''.join(text_type('%x' % ord(x)) for x in chars)
        else:
            return text_type('%x' % ord(chars))


def handle_nopinyin(chars, errors='default'):
    py = _handle_nopinyin_char(chars, errors=errors)
    if not py:
        return []
    if isinstance(py, list):
        return py
    else:
        return [py]


def single_pinyin(han, style, heteronym, errors='default', strict=True):
    """单字拼音转换.

    :param han: 单个汉字
    :param errors: 指定如何处理没有拼音的字符，详情请参考
                   :py:func:`~pypinyin.pinyin`
    :param strict: 是否严格遵照《汉语拼音方案》来处理声母和韵母
    :return: 返回拼音列表，多音字会有多个拼音项
    :rtype: list
    """
    num = ord(han)
    # 处理没有拼音的字符
    if num not in PINYIN_DICT:
        return handle_nopinyin(han, errors=errors)

    pys = PINYIN_DICT[num].split(',')  # 字的拼音列表
    if not heteronym:
        return [to_fixed(pys[0], style, strict=strict)]

    # 输出多音字的多个读音
    # 临时存储已存在的拼音，避免多音字拼音转换为非音标风格出现重复。
    # TODO: change to use set
    # TODO: add test for cache
    py_cached = {}
    pinyins = []
    for i in pys:
        py = to_fixed(i, style, strict=strict)
        if py in py_cached:
            continue
        py_cached[py] = py
        pinyins.append(py)
    return pinyins


def phrase_pinyin(phrase, style, heteronym, errors='default', strict=True):
    """词语拼音转换.

    :param phrase: 词语
    :param errors: 指定如何处理没有拼音的字符
    :param strict: 是否严格遵照《汉语拼音方案》来处理声母和韵母
    :return: 拼音列表
    :rtype: list
    """
    py = []
    if phrase in PHRASES_DICT:
        py = deepcopy(PHRASES_DICT[phrase])
        for idx, item in enumerate(py):
            py[idx] = [to_fixed(item[0], style=style, strict=strict)]
    else:
        for i in phrase:
            single = single_pinyin(i, style=style, heteronym=heteronym,
                                   errors=errors, strict=strict)
            if single:
                py.append(single)
    return py


def _pinyin(words, style, heteronym, errors, strict=True):
    pys = []
    # 初步过滤没有拼音的字符
    if RE_HANS.match(words):
        pys = phrase_pinyin(words, style=style, heteronym=heteronym,
                            errors=errors, strict=strict)
        return pys

    for word in simple_seg(words):
        if not (RE_HANS.match(word)):
            py = handle_nopinyin(word, errors=errors)
            pys.append(py) if py else None
        else:
            pys.extend(_pinyin(word, style, heteronym, errors, strict=strict))
    return pys


def pinyin(hans, style=TONE, heteronym=False, errors='default', strict=False):
    """将汉字转换为拼音.

    :param hans: 汉字字符串( ``'你好吗'`` )或列表( ``['你好', '吗']`` ).

                 如果用户安装了 ``jieba`` , 将使用 ``jieba`` 对字符串进行
                 分词处理。可以通过传入列表的方式禁用这种行为。

                 也可以使用自己喜爱的分词模块对字符串进行分词处理,
                 只需将经过分词处理的字符串列表传进来就可以了。
    :type hans: unicode 字符串或字符串列表
    :param style: 指定拼音风格，默认是 ``TONE`` 风格
    :param errors: 指定如何处理没有拼音的字符

                   * ``'default'``: 保留原始字符
                   * ``'ignore'``: 忽略该字符
                   * ``'replace'``: 替换为去掉 ``\\u`` 的 unicode 编码字符串
                     (``'\\u90aa'`` => ``'90aa'``)
                   * callable 对象: 回调函数之类的可调用对象。如果 ``erros``
                     参数 的值是个可调用对象，那么程序会回调这个函数:
                     ``func(char)``::

                         def foobar(char):
                             return 'a'
                         pinyin('あ', errors=foobar)

    :param heteronym: 是否启用多音字
    :param strict: 是否严格遵照《汉语拼音方案》来处理声母和韵母
    :return: 拼音列表
    :rtype: list

    Usage::

      >>> from pypinyin import pinyin
      >>> import pypinyin
      >>> pinyin('中心')
      [['zhōng'], ['xīn']]
      >>> pinyin('中心', heteronym=True)  # 启用多音字模式
      [['zhōng', 'zhòng'], ['xīn']]
      >>> pinyin('中心', style=pypinyin.FIRST_LETTER)  # 设置拼音风格
      [['z'], ['x']]
      >>> pinyin('中心', style=pypinyin.TONE2)
      [['zho1ng'], ['xi1n']]
      >>> pinyin('中心', style=pypinyin.CYRILLIC)
      [['чжун1'], ['синь1']]
    """
    # 对字符串进行分词处理
    if isinstance(hans, text_type):
        hans = seg(hans)
    pys = []
    for words in hans:
        pys.extend(_pinyin(words, style, heteronym, errors, strict=strict))
    return pys


def slug(hans, style=NORMAL, heteronym=False, separator='-',
         errors='default', strict=True):
    """生成 slug 字符串.

    :param hans: 汉字
    :type hans: unicode or list
    :param style: 指定拼音风格，默认是 ``NORMAL`` 风格
    :param heteronym: 是否启用多音字
    :param separstor: 两个拼音间的分隔符/连接符
    :param errors: 指定如何处理没有拼音的字符，详情请参考
                   :py:func:`~pypinyin.pinyin`
    :param strict: 是否严格遵照《汉语拼音方案》来处理声母和韵母
    :return: slug 字符串.

    ::

      >>> import pypinyin
      >>> pypinyin.slug('中国人')
      'zhong-guo-ren'
      >>> pypinyin.slug('中国人', separator=' ')
      'zhong guo ren'
      >>> pypinyin.slug('中国人', style=pypinyin.FIRST_LETTER)
      'z-g-r'
      >>> pypinyin.slug('中国人', style=pypinyin.CYRILLIC)
      'чжун1-го2-жэнь2'
    """
    return separator.join(chain(*pinyin(hans, style=style, heteronym=heteronym,
                                        errors=errors, strict=strict)
                                ))


def lazy_pinyin(hans, style=NORMAL, errors='default', strict=True):
    """不包含多音字的拼音列表.

    与 :py:func:`~pypinyin.pinyin` 的区别是返回的拼音是个字符串，
    并且每个字只包含一个读音.

    :param hans: 汉字
    :type hans: unicode or list
    :param style: 指定拼音风格，默认是 ``NORMAL`` 风格
    :param errors: 指定如何处理没有拼音的字符，详情请参考
                   :py:func:`~pypinyin.pinyin`
    :param strict: 是否严格遵照《汉语拼音方案》来处理声母和韵母
    :return: 拼音列表(e.g. ``['zhong', 'guo', 'ren']``)
    :rtype: list

    Usage::

      >>> from pypinyin import lazy_pinyin
      >>> import pypinyin
      >>> lazy_pinyin('中心')
      ['zhong', 'xin']
      >>> lazy_pinyin('中心', style=pypinyin.TONE)
      ['zhōng', 'xīn']
      >>> lazy_pinyin('中心', style=pypinyin.FIRST_LETTER)
      ['z', 'x']
      >>> lazy_pinyin('中心', style=pypinyin.TONE2)
      ['zho1ng', 'xi1n']
      >>> lazy_pinyin('中心', style=pypinyin.CYRILLIC)
      ['чжун1', 'синь1']
    """
    return list(chain(*pinyin(hans, style=style, heteronym=False,
                              errors=errors, strict=strict)))
