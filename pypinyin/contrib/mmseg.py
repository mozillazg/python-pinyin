# -*- coding: utf-8 -*-
"""最大正向匹配分词"""
from collections import defaultdict


class Seg(object):
    def __init__(self, trie):
        self.trie = trie

    def cut(self, text):
        """分词

        :param text: 待分词的文本
        :yield: 单个词语
        """
        remain = text
        while remain:
            # 按最大词长切分
            text = remain[:self.trie.max_word_legth]
            while len(text) > 1:
                matched_tree = self.trie.match(text)
                # 尾节点是个词语
                if '' in matched_tree:
                    yield text
                    # 从待处理文本中删除匹配的词语
                    remain = remain[len(text):]
                    break
                else:
                    # 不是个词语，删除右边一个字，重新开始匹配
                    text = text[:-1]
            else:
                # 只剩一个字了还没匹配到，这个字算一个词语
                yield text
                # 从待处理文本中删除匹配的词语
                remain = remain[len(text):]


class Trie(object):
    def __init__(self):
        self._data = defaultdict(tree)
        self._max_word_legth = 0

    def train(self, word_s):
        """更新 trie

        :param word_s: 词语库列表
        :type word_s: iterable
        :return: None
        """
        for word in word_s:
            # 更新最大词长
            word_length = len(word)
            if word_length > self._max_word_legth:
                self._max_word_legth = word_length
            # 把词语的每个字更新到 trie 中
            # 父节点
            pre_tree = self._data
            for letter in word:
                # 当前节点
                current_tree = pre_tree[letter]
                # 当前节点是子节点的父节点
                pre_tree = current_tree
            # 标记最后一个字的节点，表示到这里是一个词语
            current_tree[''] = None

    def match(self, text):
        """返回匹配的节点

        :param word: 待匹配的文本
        :rtype: tree

        ``'' in tree`` 表示这个节点是词语的尾节点, 当前 text 是个词语
        """
        # 父节点
        pre_tree = self._data
        for char in text:
            if char in pre_tree:
                # 当前节点
                current_tree = pre_tree[char]
                # 当前节点是子节点的父节点
                pre_tree = current_tree
            else:
                return tree()
        return current_tree

    @property
    def max_word_legth(self):
        """最大词长"""
        return self._max_word_legth


def tree():
    return defaultdict(tree)
