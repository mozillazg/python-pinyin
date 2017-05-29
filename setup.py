#!/usr/bin/env python
# -*- coding: utf-8 -*-
from codecs import open
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

current_dir = os.path.dirname(os.path.realpath(__file__))

packages = [
    'pypinyin',
    'pypinyin.style',
]

requirements = []
if sys.version_info[:2] < (2, 7):
    requirements.append('argparse')
if sys.version_info[:2] < (3, 4):
    requirements.append('enum34')
extras_require = {
    ':python_version<"2.7"': ['argparse'],
    ':python_version<"3.4"': ['enum34'],
}


def get_meta():
    meta_re = re.compile(r"(?P<name>__\w+__) = '(?P<value>[^']+)'")
    meta_d = {}
    with open(os.path.join(current_dir, 'pypinyin/__init__.py'),
              encoding='utf8') as fp:
        for match in meta_re.finditer(fp.read()):
            meta_d[match.group('name')] = match.group('value')
    return meta_d


def long_description():
    with open(os.path.join(current_dir, 'README.rst'),
              encoding='utf8') as fp:
        return fp.read()


meta_d = get_meta()
setup(
    name=meta_d['__title__'],
    version=meta_d['__version__'],
    description='汉字拼音转换工具.',
    long_description=long_description(),
    url='https://github.com/mozillazg/python-pinyin',
    author=meta_d['__author__'],
    author_email='mozillazg101@gmail.com',
    license=meta_d['__license__'],
    packages=packages,
    package_dir={'pypinyin': 'pypinyin'},
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'pypinyin = pypinyin.__main__:main',
        ],
    },
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    keywords='pinyin, 拼音',
)
