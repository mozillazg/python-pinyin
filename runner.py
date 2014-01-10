#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from argparse import ArgumentParser
import sys

from pypinyin import (__title__, __version__, pinyin, slug, lazy_pinyin,
                      load_single_dict, load_phrases_dict, NORMAL, TONE,
                      TONE2, INITIALS, FIRST_LETTER, FINALS, FINALS_TONE,
                      FINALS_TONE2)

# 支持命令行选项和参数
parser = ArgumentParser(description='convert chinese to pinyin.')
parser.add_argument('-V', '--version', action='version',
                    version='{0} {1}'.format(__title__, __version__))
# 要执行的函数名称
parser.add_argument('--func', help='function name (default: "pinyin")',
                    choices=['pinyin', 'slug'],
                    default='pinyin')
# 拼音风格
parser.add_argument('--style', help='pinyin style (default: "TONE")',
                    choices=['NORMAL', 'TONE', 'TONE2', 'INITIALS',
                             'FIRST_LETTER', 'FINALS', 'FINALS_TONE',
                             'FINALS_TONE2'], default='TONE')
parser.add_argument('--separator', help='slug separator (default: "-")',
                    default='-')
# 输出多音字
parser.add_argument('--heteronym', help='enable heteronym',
                    action='store_true')
# 要查询的汉字
parser.add_argument('hans', help='chinese string')

# python 3
try:
    unicode = unicode
except NameError:
    unicode = str


def main():
    # 获取命令行选项和参数
    options = parser.parse_args()
    hans = options.hans.decode(sys.stdin.encoding)
    func = globals()[options.func]
    style = globals()[options.style]
    heteronym = options.heteronym
    separator = options.separator

    kwargs = {
        'pinyin': {'heteronym': heteronym},
        'slug': {'heteronym': heteronym, 'separator': separator},
    }
    import logging
    # 禁用除 CRITICAL 外的日志消息
    logging.disable(logging.CRITICAL)
    result = func(hans, style=style, **kwargs[func.func_name])

    if result and isinstance(result, (list, tuple)):
        if isinstance(result[0], (list, tuple)):
            print(' '.join([','.join(s) for s in result]))
        else:
            print(result)
    else:
        print(result)

if __name__ == '__main__':
    main()
