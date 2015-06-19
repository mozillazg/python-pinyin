#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


def has_module(module):
    try:
        __import__(module)
        return True
    except ImportError:
        pass
