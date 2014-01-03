#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pypinyin

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'pypinyin',
]


def long_description():
    return open('README.rst').read() + '\n\n' + open('CHANGELOG.rst').read()

setup(
    name=pypinyin.__title__,
    version=pypinyin.__version__,
    description=pypinyin.__doc__,
    long_description=long_description(),
    url='https://github.com/mozillazg/python-pinyin',
    download_url='https://github.com/mozillazg/python-pinyin/archive/master.zip',
    author=pypinyin.__author__,
    author_email='mozillazg101@gmail.com',
    license=pypinyin.__license__,
    packages=packages,
    package_data={'': ['LICENSE.txt']},
    package_dir={'pypinyin': 'pypinyin'},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities',
    ],
    keywords='pinyin, 拼音',
)
