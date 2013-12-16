.. pypinyin documentation master file, created by
   sphinx-quickstart on Fri Sep 06 22:22:13 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pypinyin's documentation!
====================================

|Build| |Coverage| |Pypi version| |Pypi downloads|


将汉语转为拼音。可以用于汉字注音、排序、检索。基于 `pinyinjs <https://github.com/hotoo/node-pinyin>`__ 开发。

* Documentation: http://pypinyin.rtfd.org
* GitHub: https://github.com/mozillazg/python-pinyin
* Free software: MIT license
* PyPI: https://pypi.python.org/pypi/pypinyin
* Python version: 2.6, 2.7


.. 特性
.. ----
.. 
.. * 根据词组智能匹配最正确的拼音。
.. * 支持多音字。
.. * 简单的繁体支持。
.. * 支持多种不同拼音风格。


Installation
------------

To install pypinyin, simply:

.. code-block:: bash

    $ pip install pypinyin


Basic Usage
-----------

.. code-block:: python

    >>> from pypinyin import pinyin, lazy_pinyin
    >>> import pypinyin
    >>> pinyin(u'中心')
    [[u'zh\u014dng'], [u'x\u012bn']]
    >>> pinyin(u'中心', heteronym=True)  # 启用多音字模式
    [[u'zh\u014dng', u'zh\xf2ng'], [u'x\u012bn']]
    >>> pinyin(u'中心', style=pypinyin.STYLE_INITIALS)  # 设置拼音风格
    [['zh'], ['x']]
    >>> lazy_pinyin(u'中心')
    ['zhong', 'xin']


.. |Build| image:: https://api.travis-ci.org/mozillazg/python-pinyin.png?branch=master
   :target: https://travis-ci.org/mozillazg/python-pinyin
.. |Coverage| image:: https://coveralls.io/repos/mozillazg/python-pinyin/badge.png?branch=master
   :target: https://coveralls.io/r/mozillazg/python-pinyin
.. |Pypi version| image:: https://pypip.in/v/pypinyin/badge.png
   :target: https://crate.io/packages/pypinyin
.. |Pypi downloads| image:: https://pypip.in/d/pypinyin/badge.png
   :target: https://crate.io/packages/pypinyin


API
---

拼音风格:

+-----------------------------+-------------------------------------------------------------------------------+
|pypinyin.STYLE_NORMAL        |普通风格，不带声调。如： ``pin yin``                                           |
+-----------------------------+-------------------------------------------------------------------------------+
|pypinyin.STYLE_TONE          |声调风格，拼音声调在韵母第一个字母上（默认风格）。如： ``pīn yīn``             |
+-----------------------------+-------------------------------------------------------------------------------+
|pypinyin.STYLE_TONE2         |声调风格2，即拼音声调在各个拼音之后，用数字 [0-4] 进行表示。如： ``pi1n yi1n`` |
+-----------------------------+-------------------------------------------------------------------------------+
|pypinyin.STYLE_INITIALS      |声母风格，只返回各个拼音的声母部分。如： ``中国`` 的拼音 ``zh g``              |
+-----------------------------+-------------------------------------------------------------------------------+
|pypinyin.STYLE_FINALS        |韵母风格1，只返回各个拼音的韵母部分，不带声调。如： ``ong uo``                 |
+-----------------------------+-------------------------------------------------------------------------------+
|pypinyin.STYLE_FINALS_TONE   |韵母风格2，带声调，声调在韵母第一个字母上。如： ``ōng uó``                     |
+-----------------------------+-------------------------------------------------------------------------------+
|pypinyin.STYLE_FINALS_TONE2  |韵母风格2，带声调，声调在各个拼音之后，用数字 [0-4] 进行表示。如： ``o1ng uo2``|
+-----------------------------+-------------------------------------------------------------------------------+
|pypinyin.STYLE_FIRST_LETTER  |首字母风格，只返回拼音的首字母部分。如： ``p y``                               |
+-----------------------------+-------------------------------------------------------------------------------+


.. autofunction:: pypinyin.pinyin

.. autofunction:: pypinyin.slug

.. autofunction:: pypinyin.lazy_pinyin


Changelog
---------

0.3.0 (2013-09-26)
``````````````````

* 修复首字母风格无法正确处理只有韵母的汉字
* 新增三个拼音风格:
    * ``pypinyin.STYLE_FINALS`` ：       韵母风格1，只返回各个拼音的韵母部分，不带声调。如： ``ong uo``
    * ``pypinyin.STYLE_FINALS_TONE`` ：   韵母风格2，带声调，声调在韵母第一个字母上。如： ``ōng uó``
    * ``pypinyin.STYLE_FINALS_TONE2`` ：  韵母风格2，带声调，声调在各个拼音之后，用数字 [0-4] 进行表示。如： ``o1ng uo2``

0.2.0 (2013-09-22)
``````````````````

* 完善对中英文混合字符串的支持::

    >> pypinyin.pinyin(u'你好abc')
    [[u'n\u01d0'], [u'h\u01ceo'], [u'abc']]

0.1.0 (2013-09-21)
``````````````````

* Initial Release


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

