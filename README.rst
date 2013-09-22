汉语拼音转换工具(Python 版)
===========================

|Build| |Pypi version| |Pypi downloads|


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

    >>> from pypinyin import pinyin
    >>> import pypinyin
    >>> pinyin(u'中心')
    [[u'zh\u014dng'], [u'x\u012bn']]
    >>> pinyin(u'中心', heteronym=True)  # 启用多音字模式
    [[u'zh\u014dng', u'zh\xf2ng'], [u'x\u012bn']]
    >>> pinyin(u'中心', pypinyin.STYLE_INITIALS)  # 设置拼音风格
    [['zh'], ['x']]


.. |Build| image:: https://api.travis-ci.org/mozillazg/python-pinyin.png?branch=master
   :target: http://travis-ci.org/mozillazg/python-pinyin
.. |Pypi version| image:: https://pypip.in/v/pypinyin/badge.png
   :target: https://crate.io/packages/pypinyin
.. |Pypi downloads| image:: https://pypip.in/d/pypinyin/badge.png
   :target: https://crate.io/packages/pypinyin
