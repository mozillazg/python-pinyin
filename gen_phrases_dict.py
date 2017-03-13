# -*- coding: utf-8 -*-
import sys


def main(in_fp, out_fp):
    out_fp.write('''# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Warning: Auto-generated file, don't edit.
phrases_dict = {
''')
    for line in in_fp.readlines():
        line = line.strip()
        if line.startswith('#') or not line:
            continue

        # 中国: zhōng guó
        data = line.split('#')[0]
        hanzi, pinyin = data.strip().split(':')
        # [[zhōng], [guó]]
        pinyin_list = [[s] for s in pinyin.split()]
        #     中国: [[zhōng], [guó]]
        new_line = "    '{hanzi}': {pinyin_list},\n".format(
            hanzi=hanzi.strip(), pinyin_list=pinyin_list
        )
        out_fp.write(new_line)
    out_fp.write('}\n')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('python gen_phrases_dict.py INPUT OUTPUT')
        sys.exit(1)
    in_f = sys.argv[1]
    out_f = sys.argv[2]

    with open(in_f) as in_fp, open(out_f, 'w') as out_fp:
            main(in_fp, out_fp)
