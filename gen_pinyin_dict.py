# -*- coding: utf-8 -*-
import sys
import json
import pathlib2


def export_runner(code_file: str, cfg_file_name: str):
    code = """# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pathlib2
import json

# Warning: Auto-generated file, don't edit.
db_path = pathlib2.Path(__file__).parent / '{cfg_file_name}'
with open(db_path, "r", encoding="utf-8") as f:
    pinyin_dict = json.loads(f.read())

""".format(
        cfg_file_name=cfg_file_name,
    )
    with open(code_file, "w", encoding="utf-8") as f:
        f.write(code)


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
            items[new_line[0].strip()] = new_line[1].strip()
    db_file = f"{out_file}.json"
    with open(db_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(items, ensure_ascii=False))
    cfg_file_name = pathlib2.Path(db_file).name
    export_runner(out_file, cfg_file_name)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("python gen_pinyin_dict.py INPUT OUTPUT")
        sys.exit(1)
    in_f = sys.argv[1]
    out_f = sys.argv[2]

    main(in_f, out_f)
