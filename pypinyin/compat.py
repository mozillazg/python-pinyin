#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

SUPPORT_UCS4 = len('\U00020000') == 1

PY2 = sys.version_info < (3, 0)
if not PY2:
    unicode = str
    str = bytes
    callable = lambda x: getattr(x, '__call__', None)
else:
    unicode = unicode
    str = str
    callable = callable
