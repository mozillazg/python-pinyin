# -*- coding: utf-8 -*-
"""最大正向匹配分词"""


class Seg(object):
    def __init__(self, prefix_set):
        self.prefix_set = prefix_set

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
                if word in self.prefix_set:
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


class PrefixSet(object):
    def __init__(self):
        self._prefix_set = set()

    def train(self, word_s):
        """更新 prefix set

        :param word_s: 词语库列表
        :type word_s: iterable
        :return: None
        """
        for word in word_s:
            # 把词语的每个前缀更新到 prefix_set 中
            for index in range(len(word)):
                self._prefix_set.add(word[:index + 1])

    def __contains__(self, key):
        return key in self._prefix_set
