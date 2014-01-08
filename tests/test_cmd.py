#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from subprocess import PIPE, Popen
import sys


def test_cmd():
    command = 'pypinyin 音乐'
    process = Popen(command, shell=True, stdout=PIPE,
                    stderr=PIPE).communicate()
    print(process[0])
    print(process[1])
