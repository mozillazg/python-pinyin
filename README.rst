汉字拼音转换工具（Python 版）
=============================

|Build| |Coverage| |Pypi version|


将汉字转为拼音。可以用于汉字注音、排序、检索(`Russian translation`_) 。

基于 `hotoo/pinyin <https://github.com/hotoo/pinyin>`__ 开发。

* Documentation: http://pypinyin.rtfd.io/
* GitHub: https://github.com/mozillazg/python-pinyin
* License: MIT license
* PyPI: https://pypi.python.org/pypi/pypinyin
* Python version: 2.6, 2.7, pypy, 3.3, 3.4, 3.5


特性
----

* 根据词组智能匹配最正确的拼音。
* 支持多音字。
* 简单的繁体支持, 注音支持。
* 支持多种不同拼音/注音风格。


安装
----

.. code-block:: bash

    $ pip install pypinyin


文档
--------

详细文档请访问：http://pypinyin.rtfd.io/


使用示例
--------

Python 3(Python 2 下把 ``'中心'`` 替换为 ``u'中心'`` 即可):

.. code-block:: python

    >>> from pypinyin import pinyin, lazy_pinyin
    >>> import pypinyin
    >>> pinyin('中心')
    [['zhōng'], ['xīn']]
    >>> pinyin('中心', heteronym=True)  # 启用多音字模式
    [['zhōng', 'zhòng'], ['xīn']]
    >>> pinyin('中心', style=pypinyin.FIRST_LETTER)  # 设置拼音风格
    [['z'], ['x']]
    >>> pinyin('中心', style=pypinyin.TONE2, heteronym=True)
    [['zho1ng', 'zho4ng'], ['xi1n']]
    >>> pinyin('中心', style=pypinyin.BOPOMOFO)  # 注音风格
    [['ㄓㄨㄥ'], ['ㄒㄧㄣ']]
    >>> pinyin('中心', style=pypinyin.CYRILLIC)  # 俄语字母风格
    [['чжун1'], ['синь1']]
    >>> lazy_pinyin('中心')  # 不考虑多音字的情况
    ['zhong', 'xin']

命令行工具：

.. code-block:: console

    $ pypinyin 音乐
    yīn yuè
    $ pypinyin -h


FAQ
---------

为什么没有 y, w, yu 几个声母？
++++++++++++++++++++++++++++++++++++++++++++

    声母风格（INITIALS）下，“雨”、“我”、“圆”等汉字返回空字符串，因为根据 `《汉字拼音方案》 <http://www.edu.cn/20011114/3009777.shtml>`__ ， y，w，ü (yu) 都不是声母，在某些特定韵母无声母时，才加上 y 或 w，而 ü 也有其特定规则。    —— @hotoo

    如果你觉得这个给你带来了麻烦，那么也请小心一些无声母的汉字（如“啊”、“饿”、“按”、“昂”等）。 这时候你也许需要的是首字母风格（FIRST_LETTER）。    —— @hotoo

    参考: `hotoo/pinyin#57 <https://github.com/hotoo/pinyin/issues/57>`__, `#22 <https://github.com/mozillazg/python-pinyin/pull/22>`__, `#27 <https://github.com/mozillazg/python-pinyin/issues/27>`__,
    `#44 <https://github.com/mozillazg/python-pinyin/issues/44>`__


Related Projects
-----------------

* `hotoo/pinyin`__: 汉字拼音转换工具 Node.js/JavaScript 版。
* `mozillazg/go-pinyin`__: 汉字拼音转换工具 Go 版。
* `mozillazg/rust-pinyin`__: 汉字拼音转换工具 Rust 版。

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
.. _Russian translation: https://github.com/mozillazg/python-pinyin/blob/master/README_ru.rst
