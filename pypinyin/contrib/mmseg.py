# -*- coding: utf-8 -*-
"""最大正向匹配分词"""
from pypinyin.constants import PHRASES_DICT


class Seg(object):
    """最大正向匹配分词

    :type prefix_set: PrefixSet
    """
    def __init__(self, prefix_set):
        self._prefix_set = prefix_set

    def cut(self, text):
        """分词

        :param text: 待分词的文本
        :yield: 单个词语
        """
        remain = text
        while remain:
            matched = ''
            # 一次加一个字的匹配
            for index in range(len(remain)):
                word = remain[:index + 1]
                if word in self._prefix_set:
                    matched = word
                else:
                    # 前面的字符串是个词语
                    if matched:
                        yield matched
                        matched = ''
                        remain = remain[index:]
                    else:  # 前面为空
                        yield word
                        remain = remain[index + 1:]
                    # 有结果了，剩余的重新开始匹配
                    break
            else:  # 整个文本就是一个词语
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
seg = Seg(p_set)


def retrain(seg_instance):
    """重新使用内置词典训练 seg_instance。

    比如在增加自定义词语信息后需要调用这个模块重新训练分词器

    :type seg_instance: Seg
    """
    seg_instance.train(PHRASES_DICT.keys())
