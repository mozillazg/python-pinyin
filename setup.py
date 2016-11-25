#!/usr/bin/env python
# -*- coding: utf-8 -*-

from codecs import open
import sys
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pypinyin

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

packages = [
    'pypinyin',
]

requirements = []
if sys.version_info[:2] < (2, 7):
    requirements.append('argparse')


def long_description():
    readme = open('README.rst', encoding='utf8').read()
    return readme


setup(
    name=pypinyin.__title__,
    version=pypinyin.__version__,
    description=pypinyin.__doc__,
    long_description=long_description(),
    url='https://github.com/mozillazg/python-pinyin',
    author=pypinyin.__author__,
    author_email='mozillazg101@gmail.com',
    license=pypinyin.__license__,
    packages=packages,
    package_data={'': ['LICENSE.txt']},
    package_dir={'pypinyin': 'pypinyin'},
    include_package_data=True,
    install_requires=requirements,
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
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    keywords='pinyin, 拼音',
)
