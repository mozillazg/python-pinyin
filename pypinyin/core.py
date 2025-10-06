#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from itertools import chain

from pypinyin.compat import text_type
from pypinyin.constants import (
    PHRASES_DICT, PINYIN_DICT, Style, RE_HANS
)
from pypinyin.converter import DefaultConverter, UltimateConverter
from pypinyin.contrib.tone_sandhi import ToneSandhiMixin
from pypinyin.contrib.tone_convert import tone2_to_tone
from pypinyin.seg import mmseg
from pypinyin.seg.simpleseg import seg


def load_single_dict(pinyin_dict, style='default'):
    """载入用户自定义的单字拼音库

    :param pinyin_dict: 单字拼音库。比如： ``{0x963F: u"ā,ē"}``
    :param style: pinyin_dict 参数值的拼音库风格. 支持 'default', 'tone2'
    :type pinyin_dict: dict
    """
    if style == 'tone2':
        for k, v in pinyin_dict.items():
            v = tone2_to_tone(v)
            PINYIN_DICT[k] = v
    else:
        PINYIN_DICT.update(pinyin_dict)

    mmseg.retrain(mmseg.seg)


def load_phrases_dict(phrases_dict, style='default'):
    """载入用户自定义的词语拼音库

    :param phrases_dict: 词语拼音库。比如： ``{u"阿爸": [[u"ā"], [u"bà"]]}``
    :param style: phrases_dict 参数值的拼音库风格. 支持 'default', 'tone2'
    :type phrases_dict: dict
    """
    if style == 'tone2':
        for k, value in phrases_dict.items():
            v = [
                list(map(tone2_to_tone, pys))
                for pys in value
            ]
            PHRASES_DICT[k] = v
    else:
        PHRASES_DICT.update(phrases_dict)

    mmseg.retrain(mmseg.seg)


class Pinyin(object):

    def __init__(self, converter=None, **kwargs):
        self._converter = converter or DefaultConverter()

    def pinyin(self, hans, style=Style.TONE, heteronym=False,
               errors='default', strict=True, **kwargs):
        """将汉字转换为拼音，返回汉字的拼音列表。

        :param hans: 汉字字符串( ``'你好吗'`` )或列表( ``['你好', '吗']`` ).
                     可以使用自己喜爱的分词模块对字符串进行分词处理,
                     只需将经过分词处理的字符串列表传进来就可以了。
        :type hans: unicode 字符串或字符串列表
        :param style: 指定拼音风格，默认是 :py:attr:`~pypinyin.Style.TONE` 风格。
                      更多拼音风格详见 :class:`~pypinyin.Style`
        :param errors: 指定如何处理没有拼音的字符。详见 :ref:`handle_no_pinyin`

                       * ``'default'``: 保留原始字符
                       * ``'ignore'``: 忽略该字符
                       * ``'exception'``: 抛出异常
                         :class:`~pypinyin.exceptions.PinyinNotFoundException`
                       * ``'replace'``: 替换为去掉 ``\\u`` 的 unicode 编码字符串
                         (``'\\u90aa'`` => ``'90aa'``)
                       * callable 对象: 回调函数之类的可调用对象。

        :param heteronym: 是否启用多音字
        :param strict: 只获取声母或只获取韵母相关拼音风格的返回结果
                       是否严格遵照《汉语拼音方案》来处理声母和韵母，
                       详见 :ref:`strict`
        :return: 拼音列表
        :rtype: list

        """
        # 对字符串进行分词处理
        if isinstance(hans, text_type):
            han_list = self.seg(hans)
        else:
            if isinstance(self._converter, UltimateConverter) or \
                    isinstance(self._converter, ToneSandhiMixin):
                han_list = []
                for h in hans:
                    if not RE_HANS.match(h):
                        han_list.extend(self.seg(h))
                    else:
                        han_list.append(h)
            else:
                han_list = chain(*(self.seg(x) for x in hans))

        pys = []
        for words in han_list:
            pys.extend(
                self._converter.convert(
                    words, style, heteronym, errors, strict=strict))
        return pys

    def lazy_pinyin(self, hans, style=Style.NORMAL,
                    errors='default', strict=True, **kwargs):
        """将汉字转换为拼音，返回不包含多音字结果的拼音列表.

        与 :py:func:`~pypinyin.pinyin` 的区别是每个汉字的拼音是个字符串，
        并且每个字只包含一个读音.

        :param hans: 汉字字符串( ``'你好吗'`` )或列表( ``['你好', '吗']`` ).
                 可以使用自己喜爱的分词模块对字符串进行分词处理,
                 只需将经过分词处理的字符串列表传进来就可以了。
        :type hans: unicode 字符串或字符串列表
        :param style: 指定拼音风格，默认是 :py:attr:`~pypinyin.Style.NORMAL` 风格。
                      更多拼音风格详见 :class:`~pypinyin.Style`。
        :param errors: 指定如何处理没有拼音的字符，详情请参考
                       :py:func:`~pypinyin.pinyin`
        :param strict: 只获取声母或只获取韵母相关拼音风格的返回结果
                       是否严格遵照《汉语拼音方案》来处理声母和韵母，
                       详见 :ref:`strict`
        :return: 拼音列表(e.g. ``['zhong', 'guo', 'ren']``)
        :rtype: list

        """
        return list(
            chain(
                *self.pinyin(
                    hans, style=style, heteronym=False,
                    errors=errors, strict=strict)))

    def pinyin_group(self, hans, style=Style.TONE, heteronym=False,
                     errors='default', strict=True, **kwargs):
        """将汉字转换为拼音，按词组进行分组，返回分组后的结果列表。

        每个分组包含原始汉字和对应的拼音。拼音会根据情况进行处理：
        - 词语中的多个字的拼音会用空格连接
        - 儿化音会合并处理（如：花儿 -> huar）
        - 需要隔音符的拼音会自动添加（如：西安 -> xi'an）

        :param hans: 汉字字符串( ``'你好吗'`` )或列表( ``['你好', '吗']`` ).
                     可以使用自己喜爱的分词模块对字符串进行分词处理,
                     只需将经过分词处理的字符串列表传进来就可以了。
        :type hans: unicode 字符串或字符串列表
        :param style: 指定拼音风格，默认是 :py:attr:`~pypinyin.Style.TONE` 风格。
                      更多拼音风格详见 :class:`~pypinyin.Style`
        :param errors: 指定如何处理没有拼音的字符。详见 :ref:`handle_no_pinyin`

                       * ``'default'``: 保留原始字符
                       * ``'ignore'``: 忽略该字符
                       * ``'replace'``: 替换为去掉 ``\\u`` 的 unicode 编码字符串
                         (``'\\u90aa'`` => ``'90aa'``)
                       * callable 对象: 回调函数之类的可调用对象。

        :param heteronym: 是否启用多音字
        :param strict: 只获取声母或只获取韵母相关拼音风格的返回结果
                       是否严格遵照《汉语拼音方案》来处理声母和韵母，
                       详见 :ref:`strict`
        :return: 分组后的拼音列表，每个元素是一个字典，包含 'hanzi' 和 'pinyin' 两个键
        :rtype: list

        """
        # 对字符串进行分词处理
        if isinstance(hans, text_type):
            han_list = self.seg(hans)
        else:
            # 当输入是列表时，跳过分词操作
            han_list = hans

        result = []
        i = 0
        while i < len(han_list):
            word = han_list[i]

            # 检查是否需要与下一个字符合并（儿化音处理）
            # 如果当前字是汉字且下一个字是"儿"，合并处理
            if (i + 1 < len(han_list) and 
                han_list[i + 1] == '儿' and 
                RE_HANS.match(word)):
                # 合并当前字和"儿"
                word = word + '儿'
                i += 1  # 跳过下一个字符
                is_erhua = True
            else:
                is_erhua = False

            # 获取该词的拼音
            pys = self.pinyin(
                word, style=style, heteronym=heteronym,
                errors=errors, strict=strict
            )

            # 检查是否全是非汉字（如标点符号）
            if not RE_HANS.match(word):
                result.append({'hanzi': word, 'pinyin': []})
                i += 1
                continue

            # 如果没有拼音，返回空列表
            if not pys or all(not p for p in pys):
                result.append({'hanzi': word, 'pinyin': []})
                i += 1
                continue

            # 处理儿化音
            if is_erhua and len(pys) >= 2:
                # 获取倒数第二个拼音（花）和最后一个拼音（儿）
                base_pinyin_list = pys[-2]
                er_pinyin_list = pys[-1]

                if heteronym:
                    # 多音字模式：生成所有组合
                    combined = []
                    for base in base_pinyin_list:
                        for er in er_pinyin_list:
                            # 移除 er 的声母，只保留 r
                            er_suffix = 'r' if er else ''
                            combined.append(base + er_suffix)

                    # 前面的拼音保持不变
                    if len(pys) > 2:
                        # 如果有多个字，前面的用空格连接
                        prev_pinyins = []
                        for j in range(len(pys) - 2):
                            prev_pinyins.append(pys[j])
                        # 为前面的拼音生成所有组合
                        from itertools import product
                        if prev_pinyins:
                            prev_combinations = [' '.join(p) for p in product(*prev_pinyins)]
                            final_pinyins = [prev + ' ' + comb for prev in prev_combinations for comb in combined]
                        else:
                            final_pinyins = combined
                    else:
                        final_pinyins = combined
                else:
                    # 非多音字模式：只取第一个
                    base = base_pinyin_list[0] if base_pinyin_list else ''
                    er = er_pinyin_list[0] if er_pinyin_list else ''
                    er_suffix = 'r' if er else ''
                    combined = base + er_suffix

                    # 前面的拼音用空格连接
                    if len(pys) > 2:
                        prev_pinyins = [p[0] for p in pys[:-2]]
                        final_pinyins = [' '.join(prev_pinyins + [combined])]
                    else:
                        final_pinyins = [combined]

                result.append({'hanzi': word, 'pinyin': final_pinyins})
            else:
                # 非儿化音处理
                if heteronym:
                    # 多音字模式：生成所有组合
                    from itertools import product
                    # 检查是否需要添加隔音符
                    combinations = []
                    for combo in product(*pys):
                        joined = _join_pinyin_with_separator(list(combo))
                        combinations.append(joined)
                    result.append({'hanzi': word, 'pinyin': combinations})
                else:
                    # 非多音字模式：只取第一个
                    pinyin_list = [p[0] if p else '' for p in pys]
                    joined = _join_pinyin_with_separator(pinyin_list)
                    result.append({'hanzi': word, 'pinyin': [joined]})

            i += 1

        return result

    def lazy_pinyin_group(self, hans, style=Style.NORMAL,
                          errors='default', strict=True, **kwargs):
        """将汉字转换为拼音，按词组进行分组，返回分组后的结果列表。

        与 :py:func:`~pypinyin.Pinyin.pinyin_group` 的区别是每个词语的拼音结果是个字符串，
        并且每个词语只包含一个读音。

        每个分组包含原始汉字和对应的拼音字符串。拼音会根据情况进行处理：
        - 词语中的多个字的拼音会用空格连接
        - 儿化音会合并处理（如：花儿 -> huar）
        - 需要隔音符的拼音会自动添加（如：西安 -> xi'an）

        :param hans: 汉字字符串( ``'你好吗'`` )或列表( ``['你好', '吗']`` ).
                     可以使用自己喜爱的分词模块对字符串进行分词处理,
                     只需将经过分词处理的字符串列表传进来就可以了。
        :type hans: unicode 字符串或字符串列表
        :param style: 指定拼音风格，默认是 :py:attr:`~pypinyin.Style.NORMAL` 风格。
                      更多拼音风格详见 :class:`~pypinyin.Style`
        :param errors: 指定如何处理没有拼音的字符。详见 :ref:`handle_no_pinyin`

                       * ``'default'``: 保留原始字符
                       * ``'ignore'``: 忽略该字符
                       * ``'replace'``: 替换为去掉 ``\\u`` 的 unicode 编码字符串
                         (``'\\u90aa'`` => ``'90aa'``)
                       * callable 对象: 回调函数之类的可调用对象。

        :param strict: 只获取声母或只获取韵母相关拼音风格的返回结果
                       是否严格遵照《汉语拼音方案》来处理声母和韵母，
                       详见 :ref:`strict`
        :return: 分组后的拼音列表，每个元素是一个字典，包含 'hanzi' 和 'pinyin' 两个键，
                 其中 'pinyin' 是字符串而不是列表
        :rtype: list

        """
        # 调用 pinyin_group 获取完整结果
        result = self.pinyin_group(
            hans, style=style, heteronym=False,
            errors=errors, strict=strict, **kwargs
        )
        
        # 将每个词语的拼音列表转换为字符串（取第一个元素）
        lazy_result = []
        for item in result:
            lazy_item = {
                'hanzi': item['hanzi'],
                'pinyin': item['pinyin'][0] if item['pinyin'] else ''
            }
            lazy_result.append(lazy_item)
        
        return lazy_result

    def pre_seg(self, hans, **kwargs):
        """对字符串进行分词前将调用 ``pre_seg`` 方法对未分词的字符串做预处理。

        默认原样返回传入的 ``hans``。

        如果这个方法的返回值类型是 ``list``，表示返回的是一个分词后的结果，此时，
        ``seg`` 方法中将不再调用 ``seg_function`` 进行分词。

        :param hans: 分词前的字符串
        :return: ``None`` or ``list``
        """
        pass

    def seg(self, hans, **kwargs):
        """对汉字进行分词。

        分词前会调用 ``pre_seg`` 方法，分词后会调用 ``post_seg`` 方法。

        :param hans:
        :return:
        """
        pre_data = self.pre_seg(hans)
        if isinstance(pre_data, list):
            seg_data = pre_data
        else:
            seg_data = self.get_seg()(hans)

        post_data = self.post_seg(hans, seg_data)
        if isinstance(post_data, list):
            return post_data

        return seg_data

    def get_seg(self, **kwargs):
        """获取分词函数。

        :return: 分词函数
        """
        return seg

    def post_seg(self, hans, seg_data, **kwargs):
        """对字符串进行分词后将调用 ``post_seg`` 方法对分词后的结果做处理。

        默认原样返回传入的 ``seg_data``。

        如果这个方法的返回值类型是 ``list``，表示对分词结果做了二次处理，此时，
        ``seg`` 方法将以这个返回的数据作为返回值。

        :param hans: 分词前的字符串
        :param seg_data: 分词后的结果
        :type seg_data: list
        :return: ``None`` or ``list``
        """
        pass


_default_convert = DefaultConverter()
_default_pinyin = Pinyin(_default_convert)


def to_fixed(pinyin, style, strict=True):
    # 用于向后兼容，TODO: 废弃
    return _default_convert.convert_style(
        '', pinyin, style=style, strict=strict, default=pinyin)


_to_fixed = to_fixed


def handle_nopinyin(chars, errors='default', heteronym=True):
    # 用于向后兼容，TODO: 废弃
    return _default_convert.handle_nopinyin(
        chars, style=None, errors=errors, heteronym=heteronym, strict=True)


def single_pinyin(han, style, heteronym, errors='default', strict=True):
    # 用于向后兼容，TODO: 废弃
    return _default_convert._single_pinyin(
        han, style, heteronym, errors=errors, strict=strict)


def phrase_pinyin(phrase, style, heteronym, errors='default', strict=True):
    # 用于向后兼容，TODO: 废弃
    return _default_convert._phrase_pinyin(
        phrase, style, heteronym, errors=errors, strict=strict)


def pinyin(hans, style=Style.TONE, heteronym=False,
           errors='default', strict=True,
           v_to_u=False, neutral_tone_with_five=False):
    """将汉字转换为拼音，返回汉字的拼音列表。

    :param hans: 汉字字符串( ``'你好吗'`` )或列表( ``['你好', '吗']`` ).
                 可以使用自己喜爱的分词模块对字符串进行分词处理,
                 只需将经过分词处理的字符串列表传进来就可以了。
    :type hans: unicode 字符串或字符串列表
    :param style: 指定拼音风格，默认是 :py:attr:`~pypinyin.Style.TONE` 风格。
                  更多拼音风格详见 :class:`~pypinyin.Style`
    :param errors: 指定如何处理没有拼音的字符。详见 :ref:`handle_no_pinyin`

                   * ``'default'``: 保留原始字符
                   * ``'ignore'``: 忽略该字符
                   * ``'replace'``: 替换为去掉 ``\\u`` 的 unicode 编码字符串
                     (``'\\u90aa'`` => ``'90aa'``)
                   * callable 对象: 回调函数之类的可调用对象。

    :param heteronym: 是否启用多音字
    :param strict: 只获取声母或只获取韵母相关拼音风格的返回结果
                   是否严格遵照《汉语拼音方案》来处理声母和韵母，
                   详见 :ref:`strict`
    :param v_to_u: 无声调相关拼音风格下的结果是否使用 ``ü`` 代替原来的 ``v``
                   当为 False 时结果中将使用 ``v`` 表示 ``ü``
    :type v_to_u: bool
    :param neutral_tone_with_five: 声调使用数字表示的相关拼音风格下的结果是否
                                   使用 5 标识轻声
    :type neutral_tone_with_five: bool
    :return: 拼音列表
    :rtype: list

    :raise AssertionError: 当传入的字符串不是 unicode 字符时会抛出这个异常

    Usage::

      >>> from pypinyin import pinyin, Style
      >>> import pypinyin
      >>> pinyin('中心')
      [['zhōng'], ['xīn']]
      >>> pinyin('中心', heteronym=True)  # 启用多音字模式
      [['zhōng', 'zhòng'], ['xīn']]
      >>> pinyin('中心', style=Style.FIRST_LETTER)  # 设置拼音风格
      [['z'], ['x']]
      >>> pinyin('中心', style=Style.TONE2)
      [['zho1ng'], ['xi1n']]
      >>> pinyin('中心', style=Style.CYRILLIC)
      [['чжун1'], ['синь1']]
      >>> pinyin('战略', v_to_u=True, style=Style.NORMAL)
      [['zhan'], ['lüe']]
      >>> pinyin('衣裳', style=Style.TONE3, neutral_tone_with_five=True)
      [['yi1'], ['shang5']]
    """
    _pinyin = Pinyin(UltimateConverter(
        v_to_u=v_to_u, neutral_tone_with_five=neutral_tone_with_five))
    return _pinyin.pinyin(
        hans, style=style, heteronym=heteronym, errors=errors, strict=strict)


def pinyin_group(hans, style=Style.TONE, heteronym=False,
                 errors='default', strict=True,
                 v_to_u=False, neutral_tone_with_five=False):
    """将汉字转换为拼音，按词组进行分组，返回分组后的结果列表。

    每个分组包含原始汉字和对应的拼音。拼音会根据情况进行处理：
    - 词语中的多个字的拼音会用空格连接
    - 儿化音会合并处理（如：花儿 -> huar）
    - 需要隔音符的拼音会自动添加（如：西安 -> xi'an）

    :param hans: 汉字字符串( ``'你好吗'`` )或列表( ``['你好', '吗']`` ).
                 可以使用自己喜爱的分词模块对字符串进行分词处理,
                 只需将经过分词处理的字符串列表传进来就可以了。
    :type hans: unicode 字符串或字符串列表
    :param style: 指定拼音风格，默认是 :py:attr:`~pypinyin.Style.TONE` 风格。
                  更多拼音风格详见 :class:`~pypinyin.Style`
    :param errors: 指定如何处理没有拼音的字符。详见 :ref:`handle_no_pinyin`

                   * ``'default'``: 保留原始字符
                   * ``'ignore'``: 忽略该字符
                   * ``'replace'``: 替换为去掉 ``\\u`` 的 unicode 编码字符串
                     (``'\\u90aa'`` => ``'90aa'``)
                   * callable 对象: 回调函数之类的可调用对象。

    :param heteronym: 是否启用多音字
    :param strict: 只获取声母或只获取韵母相关拼音风格的返回结果
                   是否严格遵照《汉语拼音方案》来处理声母和韵母，
                   详见 :ref:`strict`
    :param v_to_u: 无声调相关拼音风格下的结果是否使用 ``ü`` 代替原来的 ``v``
                   当为 False 时结果中将使用 ``v`` 表示 ``ü``
    :type v_to_u: bool
    :param neutral_tone_with_five: 声调使用数字表示的相关拼音风格下的结果是否
                                   使用 5 标识轻声
    :type neutral_tone_with_five: bool
    :return: 分组后的拼音列表，每个元素是一个字典，包含 'hanzi' 和 'pinyin' 两个键
    :rtype: list

    Usage::

      >>> from pypinyin import pinyin_group, Style
      >>> pinyin_group('你好吗？')  # doctest: +SKIP
      [{'hanzi': '你好', 'pinyin': ['nǐ hǎo']}, {'hanzi': '吗', 'pinyin': ['ma']}, {'hanzi': '？', 'pinyin': []}]
      >>> # 如果西安在词库中，会输出 [{'hanzi': '西安', 'pinyin': ["xi'an"]}]
      >>> # 如果花儿在词库中，会输出 [{'hanzi': '花儿', 'pinyin': ['huar']}]
      >>> # 演示儿化音处理：如果词语以"儿"结尾，会自动合并
      >>> result = pinyin_group('玩儿', style=Style.NORMAL)
      >>> result[0]['hanzi']
      '玩儿'
      >>> 'r' in result[0]['pinyin'][0]  # 儿化音包含 r
      True
    """
    _pinyin = Pinyin(UltimateConverter(
        v_to_u=v_to_u, neutral_tone_with_five=neutral_tone_with_five))
    return _pinyin.pinyin_group(
        hans, style=style, heteronym=heteronym, errors=errors, strict=strict)


def lazy_pinyin_group(hans, style=Style.NORMAL,
                      errors='default', strict=True,
                      v_to_u=False, neutral_tone_with_five=False):
    """将汉字转换为拼音，按词组进行分组，返回分组后的结果列表。

    与 :py:func:`~pypinyin.pinyin_group` 的区别是每个词语的拼音结果是个字符串，
    并且每个词语只包含一个读音。

    每个分组包含原始汉字和对应的拼音字符串。拼音会根据情况进行处理：
    - 词语中的多个字的拼音会用空格连接
    - 儿化音会合并处理（如：花儿 -> huar）
    - 需要隔音符的拼音会自动添加（如：西安 -> xi'an）

    :param hans: 汉字字符串( ``'你好吗'`` )或列表( ``['你好', '吗']`` ).
                 可以使用自己喜爱的分词模块对字符串进行分词处理,
                 只需将经过分词处理的字符串列表传进来就可以了。
    :type hans: unicode 字符串或字符串列表
    :param style: 指定拼音风格，默认是 :py:attr:`~pypinyin.Style.NORMAL` 风格。
                  更多拼音风格详见 :class:`~pypinyin.Style`
    :param errors: 指定如何处理没有拼音的字符。详见 :ref:`handle_no_pinyin`

                   * ``'default'``: 保留原始字符
                   * ``'ignore'``: 忽略该字符
                   * ``'replace'``: 替换为去掉 ``\\u`` 的 unicode 编码字符串
                     (``'\\u90aa'`` => ``'90aa'``)
                   * callable 对象: 回调函数之类的可调用对象。

    :param strict: 只获取声母或只获取韵母相关拼音风格的返回结果
                   是否严格遵照《汉语拼音方案》来处理声母和韵母，
                   详见 :ref:`strict`
    :param v_to_u: 无声调相关拼音风格下的结果是否使用 ``ü`` 代替原来的 ``v``
                   当为 False 时结果中将使用 ``v`` 表示 ``ü``
    :type v_to_u: bool
    :param neutral_tone_with_five: 声调使用数字表示的相关拼音风格下的结果是否
                                   使用 5 标识轻声
    :type neutral_tone_with_five: bool
    :return: 分组后的拼音列表，每个元素是一个字典，包含 'hanzi' 和 'pinyin' 两个键，
             其中 'pinyin' 是字符串而不是列表
    :rtype: list

    Usage::

      >>> from pypinyin import lazy_pinyin_group, Style
      >>> lazy_pinyin_group('你好吗？')  # doctest: +SKIP
      [{'hanzi': '你好', 'pinyin': 'ni hao'}, {'hanzi': '吗', 'pinyin': 'ma'}, {'hanzi': '？', 'pinyin': ''}]
      >>> # 演示儿化音处理：如果词语以"儿"结尾，会自动合并
      >>> result = lazy_pinyin_group('玩儿', style=Style.NORMAL)
      >>> result[0]['hanzi']
      '玩儿'
      >>> 'r' in result[0]['pinyin']  # 儿化音包含 r
      True
    """
    _pinyin = Pinyin(UltimateConverter(
        v_to_u=v_to_u, neutral_tone_with_five=neutral_tone_with_five))
    return _pinyin.lazy_pinyin_group(
        hans, style=style, errors=errors, strict=strict)


def _join_pinyin_with_separator(pinyin_list):
    """连接拼音列表，在需要的地方添加隔音符。

    根据《汉语拼音方案》的规定，当一个音节的首字母是 a、o、e 时，
    如果前面还有音节，需要在两个音节之间加上隔音符号（'）。

    :param pinyin_list: 拼音列表
    :type pinyin_list: list
    :return: 连接后的拼音字符串
    :rtype: unicode
    """
    if not pinyin_list:
        return ''

    if len(pinyin_list) == 1:
        return pinyin_list[0]

    result = []
    for i, py in enumerate(pinyin_list):
        if not py:
            continue

        if i > 0 and result:
            # 检查当前拼音是否以 a、o、e 开头（忽略声调符号）
            # 需要处理带声调的字符，如 ā, á, ǎ, à, ō, ó, ǒ, ò, ē, é, ě, è
            first_char = py[0].lower()
            # 检查是否为 a, o, e 或带声调的版本
            if first_char in ('a', 'o', 'e', 'ā', 'á', 'ǎ', 'à', 'ō', 'ó', 'ǒ', 'ò', 'ē', 'é', 'ě', 'è'):
                # 需要添加隔音符，不加空格
                result.append("'")
                result.append(py)
            else:
                # 不需要隔音符，用空格分隔
                result.append(' ')
                result.append(py)
        else:
            result.append(py)

    return ''.join(result)


def slug(hans, style=Style.NORMAL, heteronym=False, separator='-',
         errors='default', strict=True):
    """将汉字转换为拼音，然后生成 slug 字符串.

    :param hans: 汉字字符串( ``'你好吗'`` )或列表( ``['你好', '吗']`` ).
                 可以使用自己喜爱的分词模块对字符串进行分词处理,
                 只需将经过分词处理的字符串列表传进来就可以了。
    :type hans: unicode 字符串或字符串列表
    :param style: 指定拼音风格，默认是 :py:attr:`~pypinyin.Style.NORMAL` 风格。
                  更多拼音风格详见 :class:`~pypinyin.Style`
    :param heteronym: 是否启用多音字
    :param separator: 两个拼音间的分隔符/连接符
    :param errors: 指定如何处理没有拼音的字符，详情请参考
                   :py:func:`~pypinyin.pinyin`
    :param strict: 只获取声母或只获取韵母相关拼音风格的返回结果
                   是否严格遵照《汉语拼音方案》来处理声母和韵母，
                   详见 :ref:`strict`
    :return: slug 字符串.

    :raise AssertionError: 当传入的字符串不是 unicode 字符时会抛出这个异常

    ::

      >>> import pypinyin
      >>> from pypinyin import Style
      >>> pypinyin.slug('中国人')
      'zhong-guo-ren'
      >>> pypinyin.slug('中国人', separator=' ')
      'zhong guo ren'
      >>> pypinyin.slug('中国人', style=Style.FIRST_LETTER)
      'z-g-r'
      >>> pypinyin.slug('中国人', style=Style.CYRILLIC)
      'чжун1-го2-жэнь2'
    """
    return separator.join(
        chain(
            *_default_pinyin.pinyin(
                hans, style=style, heteronym=heteronym,
                errors=errors, strict=strict
            )
        )
    )


def lazy_pinyin(hans, style=Style.NORMAL, errors='default', strict=True,
                v_to_u=False, neutral_tone_with_five=False, tone_sandhi=False):
    """将汉字转换为拼音，返回不包含多音字结果的拼音列表.

    与 :py:func:`~pypinyin.pinyin` 的区别是返回的拼音是个字符串，
    并且每个字只包含一个读音.

    :param hans: 汉字字符串( ``'你好吗'`` )或列表( ``['你好', '吗']`` ).
                 可以使用自己喜爱的分词模块对字符串进行分词处理,
                 只需将经过分词处理的字符串列表传进来就可以了。
    :type hans: unicode 字符串或字符串列表
    :param style: 指定拼音风格，默认是 :py:attr:`~pypinyin.Style.NORMAL` 风格。
                  更多拼音风格详见 :class:`~pypinyin.Style`。
    :param errors: 指定如何处理没有拼音的字符，详情请参考
                   :py:func:`~pypinyin.pinyin`
    :param strict: 只获取声母或只获取韵母相关拼音风格的返回结果
                   是否严格遵照《汉语拼音方案》来处理声母和韵母，
                   详见 :ref:`strict`
    :param v_to_u: 无声调相关拼音风格下的结果是否使用 ``ü`` 代替原来的 ``v``
                   当为 False 时结果中将使用 ``v`` 表示 ``ü``
    :type v_to_u: bool
    :param neutral_tone_with_five: 声调使用数字表示的相关拼音风格下的结果是否
                                   使用 5 标识轻声
    :type neutral_tone_with_five: bool
    :param tone_sandhi: 是否按照声调 `变调规则 <https://en.wikipedia.org/wiki/Standard_Chinese_phonology#Tone_sandhi>`__
                        对拼音进行处理
                        （使用预先通过分词库进行过分词后的结果作为 ``hans``
                        参数的值效果会更好，因为变调效果依赖分词效果）
    :type tone_sandhi: bool
    :return: 拼音列表(e.g. ``['zhong', 'guo', 'ren']``)
    :rtype: list

    :raise AssertionError: 当传入的字符串不是 unicode 字符时会抛出这个异常

    Usage::

      >>> from pypinyin import lazy_pinyin, Style
      >>> import pypinyin
      >>> lazy_pinyin('中心')
      ['zhong', 'xin']
      >>> lazy_pinyin('中心', style=Style.TONE)
      ['zhōng', 'xīn']
      >>> lazy_pinyin('中心', style=Style.FIRST_LETTER)
      ['z', 'x']
      >>> lazy_pinyin('中心', style=Style.TONE2)
      ['zho1ng', 'xi1n']
      >>> lazy_pinyin('中心', style=Style.CYRILLIC)
      ['чжун1', 'синь1']
      >>> lazy_pinyin('战略', v_to_u=True)
      ['zhan', 'lüe']
      >>> lazy_pinyin('衣裳', style=Style.TONE3, neutral_tone_with_five=True)
      ['yi1', 'shang5']
      >>> lazy_pinyin('你好', style=Style.TONE2, tone_sandhi=True)
      ['ni2', 'ha3o']
    """  # noqa
    _pinyin = Pinyin(UltimateConverter(
        v_to_u=v_to_u, neutral_tone_with_five=neutral_tone_with_five,
        tone_sandhi=tone_sandhi))
    return _pinyin.lazy_pinyin(
        hans, style=style, errors=errors, strict=strict)
