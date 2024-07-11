'''
NOTICE: you should run `pip uninstall pypinyin` before run this script
'''
import gen_phrases_dict
import gen_pinyin_dict
import tidy_phrases_dict

gen_pinyin_dict.main("pinyin-data/pinyin.txt", "pypinyin/pinyin_dict.py")

gen_phrases_dict.main(
    "phrase-pinyin-data/pinyin.txt", "pypinyin/phrases_dict_large.py"
)

tidy_phrases_dict.main()
