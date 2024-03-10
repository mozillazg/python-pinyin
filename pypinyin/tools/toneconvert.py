#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from argparse import ArgumentParser
from functools import partial
import re
import sys

from pypinyin.compat import PY2
from pypinyin.style._constants import (
    PHONETIC_SYMBOL_DICT, PHONETIC_SYMBOL_DICT_KEY_LENGTH_NOT_ONE
)
from pypinyin.contrib.tone_convert import (
    to_normal,
    to_tone,
    to_tone2,
    to_tone3,
    # to_initials,
    # to_finals,
    # to_finals_tone,
    # to_finals_tone2,
    # to_finals_tone3,
)

re_pinyin = re.compile(
    r'(?m)(^|\s|,)([1-5a-zêü{0}]+)'.format(
        re.escape(
            ''.join(x for x in PHONETIC_SYMBOL_DICT if len(x) == 1)
        )
    )
)
ACTIONS = {
    'to_normal': to_normal,
    'to_tone': to_tone,
    'to_tone2': to_tone2,
    'to_tone3': to_tone3,
    # 'to_initials': to_initials,
    # 'to_finals': to_finals,
    # 'to_finals_tone': to_finals_tone,
    # 'to_finals_tone2': to_finals_tone2,
    # 'to_finals_tone3': to_finals_tone3,
}


def re_sub(action, match_obj):
    func = ACTIONS[action]
    converted = func(match_obj.group(2))
    return '{0}{1}'.format(match_obj.group(1), converted)


def prepare(input):
    for k, v in PHONETIC_SYMBOL_DICT_KEY_LENGTH_NOT_ONE.items():
        if k in input:
            input = input.replace(k, v)
    return input


def convert(action, args):
    inputs = args.inputs
    for item in inputs:
        item = prepare(item)
        result = re_pinyin.sub(lambda m: re_sub(action, m), item)
        print(result)


def get_parser():
    parser = ArgumentParser()

    if PY2 or sys.version_info < (3, 7):
        subparser = parser.add_subparsers()
    else:
        subparser = parser.add_subparsers(required=True, title='subcommands')

    for key in ACTIONS.keys():
        name = key.replace('_', '-')
        func = partial(convert, key)
        p = subparser.add_parser(
            name,
            help='call pypinyin.contrib.tone_convert.{}() with inputs'.format(key))
        p.set_defaults(func=func)
        p.add_argument('inputs', nargs='+')

    return parser


def main(argv):
    argv = argv[:]

    if not sys.stdin.isatty():
        pipe_data = sys.stdin.read().strip()
    else:
        pipe_data = ''
    if pipe_data:
        argv.append(pipe_data)

    parser = get_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == '__main__':
    main(sys.argv[1:])
