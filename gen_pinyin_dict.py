# -*- coding: utf-8 -*-
import sys
import json
import pathlib2
import gen_export_helper


def main(in_file: str, out_file: str):
    items = {}
    with open(in_file, "r", encoding="utf-8") as in_file:
        for line in in_file.readlines():
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            # line is U+4E2D: zhōng,zhòng  # 中
            # raw_line U+4E2D: zhōng,zhòng
            raw_line = line.split("#")[0].strip()
            # 0x4E2D: zhōng,zhòng
            new_line = raw_line.replace("U+", "0x")
            # '0x4E2D',' zhōng,zhòng'
            new_line = new_line.split(":")
            items[int(new_line[0].strip(), 16)] = new_line[1].strip()

    gen_export_helper.export_runner(items, out_file, "pinyin_dict")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("python gen_pinyin_dict.py INPUT OUTPUT")
        sys.exit(1)
    in_f = sys.argv[1]
    out_f = sys.argv[2]

    main(in_f, out_f)
