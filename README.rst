汉语拼音转换工具（Python 版）
=============================

.. image:: https://badges.gitter.im/mozillazg/python-pinyin.svg
   :alt: Join the chat at https://gitter.im/mozillazg/python-pinyin
   :target: https://gitter.im/mozillazg/python-pinyin?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

|Build| |Coverage| |Pypi version| |Pypi downloads|


将汉语转为拼音。可以用于汉字注音、排序、检索。

基于 `hotoo/pinyin <https://github.com/hotoo/pinyin>`__ 开发。

* Documentation: http://pypinyin.mozillazg.com
* GitHub: https://github.com/mozillazg/python-pinyin
* License: MIT license
* PyPI: https://pypi.python.org/pypi/pypinyin
* Python version: 2.6, 2.7, pypy, 3.3, 3.4, 3.5


特性
----

* 根据词组智能匹配最正确的拼音。
* 支持多音字。
* 简单的繁体支持。
* 支持多种不同拼音风格。


安装
----

.. code-block:: bash

    $ pip install pypinyin


文档
--------

详细文档请访问：http://pypinyin.mozillazg.com


使用示例
--------

.. code-block:: python

    >>> from pypinyin import pinyin, lazy_pinyin
    >>> import pypinyin
    >>> pinyin(u'中心')
    [[u'zh\u014dng'], [u'x\u012bn']]
    >>> pinyin(u'中心', heteronym=True)  # 启用多音字模式
    [[u'zh\u014dng', u'zh\xf2ng'], [u'x\u012bn']]
    >>> pinyin(u'中心', style=pypinyin.FIRST_LETTER)  # 设置拼音风格
    [['z'], ['x']]
    >>> pinyin('中心', style=pypinyin.TONE2, heteronym=True)
    [['zho1ng', 'zho4ng'], ['xi1n']]
    >>> lazy_pinyin(u'中心')  # 不考虑多音字的情况
    ['zhong', 'xin']

命令行工具：

.. code-block:: console

    $ pypinyin 音乐
    yīn yuè
    $ pypinyin -h


Related Projects
-----------------

* `hotoo/pinyin`__: 汉语拼音转换工具 Node.js/JavaScript 版。
* `mozillazg/go-pinyin`__: 汉语拼音转换工具 Go 版。
* `mozillazg/rust-pinyin`__: 汉语拼音转换工具 Rust 版。

__ https://github.com/hotoo/pinyin
__ https://github.com/mozillazg/go-pinyin
__ https://github.com/mozillazg/rust-pinyin


.. |Build| image:: https://img.shields.io/travis/mozillazg/python-pinyin/master.svg
   :target: https://travis-ci.org/mozillazg/python-pinyin
.. |Coverage| image:: https://img.shields.io/coveralls/mozillazg/python-pinyin/master.svg
   :target: https://coveralls.io/r/mozillazg/python-pinyin
.. |PyPI version| image:: https://img.shields.io/pypi/v/pypinyin.svg
   :target: https://pypi.python.org/pypi/pypinyin
.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/pypinyin.svg
   :target: https://pypi.python.org/pypi/pypinyin
