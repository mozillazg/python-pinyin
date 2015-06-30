#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import sys

PY2 = sys.version_info[0] == 2
if PY2:
    unicode = unicode
    str = str
    callable = callable
    import __builtin__
else:
    unicode = str
    str = bytes
    callable = lambda x: getattr(x, '__call__', None)
    import builtins as __builtin__
