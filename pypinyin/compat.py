#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

SUPPORT_UCS4 = len('\U00020000') == 1

PY2 = sys.version_info < (3, 0)
if not PY2:
    text_type = str
    bytes_type = bytes
else:
    text_type = unicode           # noqa
    bytes_type = str

try:
    callable_check = callable     # noqa
except NameError:
    def callable_check(obj):
        return hasattr(obj, '__call__')
