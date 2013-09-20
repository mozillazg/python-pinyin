#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

__version__ = '0.1.0'
__author__ = 'mozillazg, 闲耘'
__license__ = 'MIT'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

requirements = [
    'jieba>=0.31',
]
packages = [
    'pypinyin',
]


def long_description():
    return open('README.rst').read() + '\n\n' + open('CHANGELOG.rst').read()

setup(
    name='pypinyin',
    version=__version__,
    description='汉语拼音转换工具',
    long_description=long_description(),
    url='https://github.com/mozillazg/python-pinyin',
    download_url='https://github.com/mozillazg/python-pinyin',
    author=__author__,
    author_email='mozillazg101@gmail.com',
    license=__license__,
    packages=packages,
    package_data={'': ['LICENSE.txt']},
    package_dir={'pypinyin': 'pypinyin'},
    include_package_data=True,
    install_requires=requirements,
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
        'Topic :: Utilities',
    ],
    keywords='pinyin, 拼音',
)
