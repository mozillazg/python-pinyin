#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pypinyin import *   # noqa


def test_import_all():
    pinyin('啦啦啦')
    pinyin('啦啦啦', TONE2)
    lazy_pinyin('啦啦啦')
    slug('啦啦啦')
