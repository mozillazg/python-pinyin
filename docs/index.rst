.. pypinyin documentation master file, created by
   sphinx-quickstart on Fri Sep 06 22:22:13 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

汉字拼音转换工具（Python 版）
=============================

|Build| |Coverage| |Pypi version|


将汉字转为拼音。可以用于汉字注音、排序、检索(`Russian translation`_) 。

基于 `hotoo/pinyin <https://github.com/hotoo/pinyin>`__ 开发。

* Documentation: http://pypinyin.rtfd.io
* GitHub: https://github.com/mozillazg/python-pinyin
* License: MIT license
* PyPI: https://pypi.python.org/pypi/pypinyin
* Python version: 2.6, 2.7, pypy, 3.3, 3.4, 3.5


特性
----

* 根据词组智能匹配最正确的拼音。
* 支持多音字。
* 简单的繁体支持, 注音支持。
* 支持多种不同拼音风格。


.. |Build| image:: https://img.shields.io/travis/mozillazg/python-pinyin/master.svg
   :target: https://travis-ci.org/mozillazg/python-pinyin
.. |Coverage| image:: https://img.shields.io/coveralls/mozillazg/python-pinyin/master.svg
   :target: https://coveralls.io/r/mozillazg/python-pinyin
.. |PyPI version| image:: https://img.shields.io/pypi/v/pypinyin.svg
   :target: https://pypi.python.org/pypi/pypinyin
.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/pypinyin.svg
   :target: https://pypi.python.org/pypi/pypinyin
.. _Russian translation: https://github.com/mozillazg/python-pinyin/blob/master/README_ru.rst


Contents
--------

.. toctree::
    :maxdepth: 4

    installation
    usage
    api
    faq
    related
    CHANGELOG


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

