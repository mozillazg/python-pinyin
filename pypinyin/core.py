#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from copy import deepcopy
from itertools import chain
import os
import re
import warnings

from .compat import text_type, callable_check
from .constants import (
    PHRASES_DICT, PINYIN_DICT, _INITIALS, PHONETIC_SYMBOL, RE_PHONETIC_SYMBOL,
    RE_TONE2, RE_TONE3, RE_HANS, U_FINALS_EXCEPTIONS_MAP,
    BOPOMOFO_REPLACE, BOPOMOFO_TABLE,
    CYRILLIC_REPLACE, CYRILLIC_TABLE,
    NORMAL, TONE, TONE2, TONE3, INITIALS, FIRST_LETTER,
    FINALS, FINALS_TONE, FINALS_TONE2, FINALS_TONE3,
    BOPOMOFO, BOPOMOFO_FIRST,
    CYRILLIC, CYRILLIC_FIRST
)
from .utils import simple_seg, _replace_tone2_style_dict_to_default


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


def initial(pinyin):
    """获取单个拼音中的声母.

    :param pinyin: 单个拼音
    :type pinyin: unicode
    :return: 声母
    :rtype: unicode
    """
    for i in _INITIALS:
        if pinyin.startswith(i):
            return i
    return ''


def final(pinyin):
    """获取单个拼音中的韵母.

    :param pinyin: 单个拼音
    :type pinyin: unicode
    :return: 韵母
    :rtype: unicode
    """
    initial_ = initial(pinyin) or None
    if not initial_:
        return no_initial_final(pinyin)
    # 特例 j/q/x
    m = re.match(r'^(j|q|x)(ū|ú|ǔ|ù)$', pinyin)
    if m:
        return (U_FINALS_EXCEPTIONS_MAP[m.group(2)])
    pinyin = re.sub(r'^(j|q|x)u(\d?)$', r'\1v\2', pinyin)
    return ''.join(pinyin.split(initial_, 1))


def no_initial_final(pinyin):
    # 特例 y/w
    if pinyin.startswith('y'):
        if pinyin.startswith('yu'):
            pinyin = 'v' + pinyin[2:]
        elif pinyin.startswith('yi'):
            pinyin = pinyin[1:]
        else:
            pinyin = 'i' + pinyin[1:]
    elif pinyin.startswith('w'):
        if pinyin.startswith('wu'):
            pinyin = pinyin[1:]
        else:
            pinyin = 'u' + pinyin[1:]
    return pinyin


def to_fixed(pinyin, style):
    """根据拼音风格格式化带声调的拼音.

    :param pinyin: 单个拼音
    :param style: 拼音风格
    :return: 根据拼音风格格式化后的拼音字符串
    :rtype: unicode
    """
    # 声母
    if style == INITIALS:
        return initial(pinyin)

    def _replace(m):
        symbol = m.group(0)  # 带声调的字符
        # 不包含声调
        if style in [NORMAL, FIRST_LETTER, FINALS]:
            # 去掉声调: a1 -> a
            # 鼻音: 'ḿ', 'ń', 'ň', 'ǹ '
            if symbol in ['\u1e3f', '\u0144', '\u0148', '\u01f9']:
                return re.sub(r'\d', r'', PHONETIC_SYMBOL[symbol])
            else:
                return re.sub(RE_TONE2, r'\1', PHONETIC_SYMBOL[symbol])
        # 使用数字标识声调
        elif style in [TONE2, TONE3, FINALS_TONE2, FINALS_TONE3,
                       BOPOMOFO, BOPOMOFO_FIRST, CYRILLIC, CYRILLIC_FIRST]:
            # 返回使用数字标识声调的字符
            return PHONETIC_SYMBOL[symbol]
        # 声调在头上
        else:
            return symbol

    # 替换拼音中的带声调字符
    py = re.sub(RE_PHONETIC_SYMBOL, _replace, pinyin)
    # 将声调移动到最后
    if style in [TONE3, FINALS_TONE3,
                 BOPOMOFO, BOPOMOFO_FIRST,
                 CYRILLIC, CYRILLIC_FIRST]:
        py = RE_TONE3.sub(r'\1\3\2', py)

    # 首字母
    if style == FIRST_LETTER:
        py = py[0]
    # 韵母
    elif style in [FINALS, FINALS_TONE, FINALS_TONE2, FINALS_TONE3]:
        # 不处理鼻音: 'ḿ', 'ń', 'ň', 'ǹ'
        if pinyin and pinyin[0] not in [
            '\u1e3f', '\u0144', '\u0148', '\u01f9'
        ]:
            py = final(py)
    # 声调在拼音之后、注音
    elif style in [BOPOMOFO, BOPOMOFO_FIRST]:
        # 查表替换成注音
        for f, r in BOPOMOFO_REPLACE:
            py = f.sub(r, py)
        py = ''.join(BOPOMOFO_TABLE.get(x, x) for x in py)
        if style == BOPOMOFO_FIRST:
            py = py[0]
    elif style in [CYRILLIC, CYRILLIC_FIRST]:
        # 汉语拼音与俄语字母对照表
        for f, r in CYRILLIC_REPLACE:
            py = f.sub(r, py)
        py = ''.join(CYRILLIC_TABLE.get(x, x) for x in py)
        if style == CYRILLIC_FIRST:
            py = py[0]
    return py


def toFixed(pinyin, style):
    warnings.warn(
        DeprecationWarning('"toFixed" is deprecated. Use "to_fixed" instead')
    )
    return to_fixed(pinyin, style)


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


def single_pinyin(han, style, heteronym, errors='default'):
    """单字拼音转换.

    :param han: 单个汉字
    :param errors: 指定如何处理没有拼音的字符，详情请参考
                   :py:func:`~pypinyin.pinyin`
    :return: 返回拼音列表，多音字会有多个拼音项
    :rtype: list
    """
    num = ord(han)
    # 处理没有拼音的字符
    if num not in PINYIN_DICT:
        return handle_nopinyin(han, errors=errors)

    pys = PINYIN_DICT[num].split(',')  # 字的拼音列表
    if not heteronym:
        return [to_fixed(pys[0], style)]

    # 输出多音字的多个读音
    # 临时存储已存在的拼音，避免多音字拼音转换为非音标风格出现重复。
    py_cached = {}
    pinyins = []
    for i in pys:
        py = to_fixed(i, style)
        if py in py_cached:
            continue
        py_cached[py] = py
        pinyins.append(py)
    return pinyins


def phrase_pinyin(phrase, style, heteronym, errors='default'):
    """词语拼音转换.

    :param phrase: 词语
    :param errors: 指定如何处理没有拼音的字符
    :return: 拼音列表
    :rtype: list
    """
    py = []
    if phrase in PHRASES_DICT:
        py = deepcopy(PHRASES_DICT[phrase])
        for idx, item in enumerate(py):
            py[idx] = [to_fixed(item[0], style=style)]
    else:
        for i in phrase:
            single = single_pinyin(i, style=style, heteronym=heteronym,
                                   errors=errors)
            if single:
                py.append(single)
    return py


def phrases_pinyin(phrases, style, heteronym, errors='default'):
    """词语拼音转换.

    :param phrases: 词语
    :param errors: 指定如何处理没有拼音的字符
    :return: 拼音列表
    :rtype: list
    """
    warnings.warn(
        DeprecationWarning(
            '"phrases_pinyin" is deprecated. Use "phrase_pinyin" instead'
        )
    )
    return phrase_pinyin(phrases, style, heteronym, errors=errors)


def _pinyin(words, style, heteronym, errors):
    pys = []
    # 初步过滤没有拼音的字符
    if RE_HANS.match(words):
        pys = phrases_pinyin(words, style=style, heteronym=heteronym,
                             errors=errors)
        return pys

    for word in simple_seg(words):
        if not (RE_HANS.match(word)):
            py = handle_nopinyin(word, errors=errors)
            pys.append(py) if py else None
        else:
            pys.extend(_pinyin(word, style, heteronym, errors))
    return pys


def pinyin(hans, style=TONE, heteronym=False, errors='default'):
    """将汉字转换为拼音.

    :param hans: 汉字字符串( ``'你好吗'`` )或列表( ``['你好', '吗']`` ).

                 如果用户安装了 ``jieba`` , 将使用 ``jieba`` 对字符串进行
                 分词处理。可以通过传入列表的方式禁用这种行为。

                 也可以使用自己喜爱的分词模块对字符串进行分词处理,
                 只需将经过分词处理的字符串列表传进来就可以了。
    :type hans: unicode 字符串或字符串列表
    :param style: 指定拼音风格
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
        pys.extend(_pinyin(words, style, heteronym, errors))
    return pys


def slug(hans, style=NORMAL, heteronym=False, separator='-', errors='default'):
    """生成 slug 字符串.

    :param hans: 汉字
    :type hans: unicode or list
    :param style: 指定拼音风格
    :param heteronym: 是否启用多音字
    :param separstor: 两个拼音间的分隔符/连接符
    :param errors: 指定如何处理没有拼音的字符，详情请参考
                   :py:func:`~pypinyin.pinyin`
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
                                        errors=errors)
                                ))


def lazy_pinyin(hans, style=NORMAL, errors='default'):
    """不包含多音字的拼音列表.

    与 :py:func:`~pypinyin.pinyin` 的区别是返回的拼音是个字符串，
    并且每个字只包含一个读音.

    :param hans: 汉字
    :type hans: unicode or list
    :param style: 指定拼音风格
    :param errors: 指定如何处理没有拼音的字符，详情请参考
                   :py:func:`~pypinyin.pinyin`
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
                              errors=errors)))
