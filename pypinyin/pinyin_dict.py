# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pathlib2
import json

# Warning: Auto-generated file, don't edit.
db_path = pathlib2.Path(__file__).parent / 'pinyin_dict.py.json'
with open(db_path, "r", encoding="utf-8") as f:
    pinyin_dict = json.loads(f.read())

