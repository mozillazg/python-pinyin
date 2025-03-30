# -*- coding: utf-8 -*-


class PinyinNotFoundException(Exception):
    #: 异常信息
    message = ''
    #: 不包含拼音的字符串
    chars = ''

    def __init__(self, chars):
        self.message = 'No pinyin found for character "{}"'.format(chars)
        self.chars = chars
        super().__init__(self.message)
