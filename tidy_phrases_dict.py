# -*- coding: utf-8 -*-

env = {}
import gen_export_helper


def get_pinyins_via_pinyin_dict(phrases):
    pinyins = []
    for han in phrases:
        pinyin = env["pinyin_dict"][ord(han)].split(",")[0]
        pinyins.append([pinyin])

    return pinyins


def save(new_dict, output_file):
    hanzi_pairs = sorted(new_dict.items(), key=lambda x: x[0])
    items = {}
    for hanzi, pinyin_list in hanzi_pairs:
        #     中国: [[zhōng], [guó]]
        items[hanzi.strip()] = pinyin_list

    gen_export_helper.export_runner(items, output_file, "phrases_dict")


def double_check():
    import pypinyin

    missing_dict = {}
    for phrases, pinyins in env["phrases_dict"].items():
        if pypinyin.pinyin(phrases, heteronym=True) != pinyins:
            missing_dict[phrases] = pinyins

    return missing_dict


def tidy():
    new_dict = {}
    for phrases, pinyins in env["phrases_dict"].items():
        pinyins_via_pinyin_dict = get_pinyins_via_pinyin_dict(phrases)
        if pinyins != pinyins_via_pinyin_dict:
            new_dict[phrases] = pinyins

    return new_dict


def main():
    # with open("./pypinyin/pinyin_dict.py") as fp:
    #     exec(fp.read(), env, env)
    # with open("./pypinyin/phrases_dict_large.py") as fp:
    #     exec(fp.read(), env, env)
    import pypinyin.pinyin_dict

    env["pinyin_dict"] = pypinyin.pinyin_dict.pinyin_dict
    import pypinyin.phrases_dict_large

    env["phrases_dict"] = pypinyin.phrases_dict_large.phrases_dict

    output = "pypinyin/phrases_dict.py"
    new_dict = tidy()
    # save(new_dict, output) # duplicated operation?

    missing_dict = double_check()
    new_dict.update(missing_dict)
    save(new_dict, output)


if __name__ == "__main__":
    main()
