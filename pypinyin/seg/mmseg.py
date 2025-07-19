# -*- coding: utf-8 -*-
"""最大正向匹配分词"""
from pypinyin.constants import PHRASES_DICT


class Seg(object):
    """正向最大匹配分词

    :type prefix_set: PrefixSet
    :param no_non_phrases: 是否严格按照词语分词，不允许把非词语的词当做词语进行分词
    :type no_non_phrases: bool
    """

    def __init__(self, prefix_set, no_non_phrases=False):
        self._prefix_set = prefix_set
        self._no_non_phrases = no_non_phrases

    def cut(self, text):
        """分词

        :param text: 待分词的文本
        :yield: 单个词语
        """
        remain = text
        while remain:
            matched = ''
            last_valid_word = ''
            last_valid_index = 0

            # 一次加一个字的匹配
            for index in range(len(remain)):
                word = remain[:index + 1]
                if word in self._prefix_set:
                    matched = word
                    # 检查当前匹配的词是否为有效词语
                    if (not self._no_non_phrases) or word in PHRASES_DICT:
                        last_valid_word = word
                        last_valid_index = index + 1
                else:
                    # 前缀匹配失败，需要处理之前的匹配结果
                    if last_valid_word:
                        # 有有效词语，输出最后一个有效词语
                        yield last_valid_word
                        remain = remain[last_valid_index:]
                    else:
                        # 没有有效词语
                        if self._no_non_phrases:
                            # 严格模式：输出第一个字符
                            yield remain[0]
                            remain = remain[1:]
                        else:
                            # 非严格模式：输出匹配到的前缀（如果有）或第一个字符
                            if matched:
                                yield matched
                                remain = remain[len(matched):]
                            else:
                                yield remain[0]
                                remain = remain[1:]
                    break
            else:  # 整个剩余文本都能匹配前缀
                if last_valid_word:
                    # 有有效词语，输出最后一个有效词语
                    yield last_valid_word
                    remain = remain[last_valid_index:]
                else:
                    # 没有有效词语，处理剩余文本
                    if self._no_non_phrases and remain not in PHRASES_DICT:
                        # 严格模式且不在词典中：拆分为单字符
                        for x in remain:
                            yield x
                    else:
                        # 非严格模式或在词典中：输出整个剩余文本
                        yield remain
                    break

    def train(self, words):
        """训练分词器

        :param words: 词语列表
        """
        self._prefix_set.train(words)


class PrefixSet(object):
    def __init__(self):
        self._set = set()

    def train(self, word_s):
        """更新 prefix set

        :param word_s: 词语库列表
        :type word_s: iterable
        :return: None
        """
        for word in word_s:
            # 把词语的每个前缀更新到 prefix_set 中
            for index in range(len(word)):
                self._set.add(word[:index + 1])

    def __contains__(self, key):
        return key in self._set


p_set = PrefixSet()
p_set.train(PHRASES_DICT.keys())

#: 基于内置词库的最大正向匹配分词器。使用:
#:
#: .. code-block:: python
#:
#:     >>> from pypinyin.contrib.mmseg import seg
#:     >>> text = '你好，我是中国人，我爱我的祖国'
#:     >>> seg.cut(text)
#:     <generator object Seg.cut at 0x10b2df2b0>
#:     >>> list(seg.cut(text))
#:     ['你好', '，', '我', '是', '中国人', '，', '我', '爱',
#:      '我的', '祖', '国']
#:     >>> seg.train(['祖国', '我是'])
#:     >>> list(seg.cut(text))
#:     ['你好', '，', '我是', '中国人', '，', '我', '爱',
#:      '我的', '祖国']
#:     >>>
seg = Seg(p_set, no_non_phrases=True)


def retrain(seg_instance):
    """重新使用内置词典训练 seg_instance。

    比如在增加自定义词语信息后需要调用这个模块重新训练分词器

    :type seg_instance: Seg
    """
    seg_instance.train(PHRASES_DICT.keys())
