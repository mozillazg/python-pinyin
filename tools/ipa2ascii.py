#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
"""将拼音库中的国际音标字母替换为 ASCII 字母"""

from io import open
import sys


def ipa_map_ascii():
    return {
        'ɑ': 'a',
        'b': 'b',
        'c': 'c',
        'd': 'd',
        'e': 'e',
        'f': 'f',
        'ɡ': 'g',
        'h': 'h',
        'i': 'i',
        'j': 'j',
        'k': 'k',
        'l': 'l',
        'm': 'm',
    }


def main(path):
    with open(path, 'r+', encoding='utf8') as f:
        new_content = f.read()
        for ipa, s in ipa_map_ascii().items():
            new_content = new_content.replace(ipa, s)
        f.seek(0)
        f.write(new_content)
        f.truncate()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usge: python ipa2ascii.py FILE...')
    for path in sys.argv[1:]:
        main(path)
