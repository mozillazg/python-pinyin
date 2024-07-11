# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pathlib2
import json

# Warning: Auto-generated file, don't edit.
db_path = pathlib2.Path(__file__).parent / 'phrases_dict.py.json'
with open(db_path, "r", encoding="utf-8") as f:
    tmp_phrases_dict = json.loads(f.read())
phrases_dict = {}
for x in tmp_phrases_dict:
    phrases_dict[int(x)] = tmp_phrases_dict[x]

