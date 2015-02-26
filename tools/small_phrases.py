#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pypinyin.phrases_dict import phrases_dict
from pypinyin import pinyin, TONE

phrases_list = set()
phrases_same = set()

for han, pys in phrases_dict.items():
    if pinyin(han, style=TONE, heteronym=True) != pys:
        phrases_list.add(han)
    else:
        phrases_same.add(han)


if __name__ == '__main__':
    with open('phrases_same.txt', 'w') as f:
        for x in phrases_same:
            f.write(u'%s\n' % x)

    print(len(phrases_dict))
    print(len(phrases_same))
    print(len(phrases_list))
