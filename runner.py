#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from argparse import ArgumentParser
import sys

import pypinyin
from pypinyin import __title__, __version__

py3 = sys.version_info[0] == 3
if py3:
    unicode = str


def get_parser():
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
    return parser


def main():
    import logging
    # 禁用除 CRITICAL 外的日志消息
    logging.disable(logging.CRITICAL)

    # 获取命令行选项和参数
    parser = get_parser()
    options = parser.parse_args()
    if py3:
        hans = options.hans
    else:
        hans = options.hans.decode(sys.stdin.encoding)
    func = getattr(pypinyin, options.func)
    style = getattr(pypinyin, options.style)
    heteronym = options.heteronym
    separator = options.separator

    func_kwargs = {
        'pinyin': {'heteronym': heteronym},
        'slug': {'heteronym': heteronym, 'separator': separator},
    }
    if py3:
        kwargs = func_kwargs[func.__name__]
    else:
        kwargs = func_kwargs[func.func_name]
    result = func(hans, style=style, **kwargs)

    if result and isinstance(result, (list, tuple)):
        if isinstance(result[0], (list, tuple)):
            print(' '.join([','.join(s) for s in result]))
        else:
            print(result)
    else:
        print(result)

if __name__ == '__main__':
    main()
