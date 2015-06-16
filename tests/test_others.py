#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def test_import_all():
    from pypinyin import *   # noqa
    pinyin('啦啦啦')
    pinyin('啦啦啦', TONE2)
    lazy_pinyin('啦啦啦')
    slug('啦啦啦')
