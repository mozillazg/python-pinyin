# -*- coding: utf-8 -*-
import sys


def main(in_fp, out_fp):
    out_fp.write('''# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Warning: Auto-generated file, don't edit.
pinyin_dict = {
''')
    for line in in_fp.readlines():
        if (line.startswith('"') or line.startswith('#') or
                not line.strip()):
            continue
        else:
            # line is U+4E2D: zhōng,zhòng  # 中
            # raw_line U+4E2D: zhōng,zhòng
            raw_line = line.split('#')[0].strip()
            new_line = raw_line.replace('U+', '0x')
            new_line = new_line.replace(': ', ": '") + "',"
            #     0x4E2D: 'zhōng,zhòng'
            out_fp.write(' ' * 4 + new_line + '\n')
    out_fp.write('}\n')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('python gen.py INPUT OUTPUT')
        sys.exit(1)
    in_f = sys.argv[1]
    out_f = sys.argv[2]

    with open(in_f) as in_fp, open(out_f, 'w') as out_fp:
            main(in_fp, out_fp)
