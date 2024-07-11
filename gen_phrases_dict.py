# -*- coding: utf-8 -*-
import sys
import gen_export_helper


def remove_dup_items(lst):
    new_lst = []
    for item in lst:
        if item not in new_lst:
            new_lst.append(item)
    return new_lst


def parse(in_file: str):
    with open(in_file, "r", encoding="utf-8") as in_fp:
        phrases_dict = {}
        for line in in_fp.readlines():
            line = line.strip()
            if line.startswith("#") or not line:
                continue

            # 中国: zhōng guó
            data = line.split("#")[0]
            hanzi, pinyin = data.strip().split(":")
            hanzi = hanzi.strip()
            # [[zhōng], [guó]]
            pinyin_list = [[s] for s in pinyin.split()]

            if hanzi not in phrases_dict:
                phrases_dict[hanzi] = pinyin_list
            else:
                for index, value in enumerate(phrases_dict[hanzi]):
                    value.extend(pinyin_list[index])
                    phrases_dict[hanzi][index] = remove_dup_items(value)

        return phrases_dict


def main(in_file, out_file):
    hanzi_pairs = sorted(parse(in_file).items(), key=lambda x: x[0])
    items = {}
    for hanzi, pinyin_list in hanzi_pairs:
        #     中国: [[zhōng], [guó]]
        items[hanzi.strip()] = pinyin_list

    gen_export_helper.export_runner(items, out_file, "phrases_dict", is_simple=True)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("python gen_phrases_dict.py INPUT OUTPUT")
        sys.exit(1)
    in_f = sys.argv[1]
    out_f = sys.argv[2]

    main(in_f, out_f)
