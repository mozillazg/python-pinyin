# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from codecs import open
import json
import os

_current_dir = os.path.dirname(os.path.realpath(__file__))
_json_path = os.path.join(_current_dir, 'pinyin_dict.json')
pinyin_dict = {}


def _load_pinyin_dict():
    global pinyin_dict
    with open(_json_path, encoding='utf8') as fp:
        pinyin_dict = json.loads(fp.read())
    for k, v in pinyin_dict.copy().items():
        del pinyin_dict[k]
        pinyin_dict[int(k)] = v


_load_pinyin_dict()
