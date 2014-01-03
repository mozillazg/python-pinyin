汉语拼音转换工具(Python 版)
===========================

|Build| |Coverage| |Pypi version| |Pypi downloads|


将汉语转为拼音。可以用于汉字注音、排序、检索。基于 `pinyinjs <https://github.com/hotoo/node-pinyin>`__ 开发。

* 文档 http://pypinyin.rtfd.org
* GitHub: https://github.com/mozillazg/python-pinyin
* 开源协议: MIT license
* PyPI: https://pypi.python.org/pypi/pypinyin
* Python 版本: 2.6, 2.7, pypy, 3.3


.. 特性
.. ----
.. 
.. * 根据词组智能匹配最正确的拼音。
.. * 支持多音字。
.. * 简单的繁体支持。
.. * 支持多种不同拼音风格。


安装
----

.. code-block:: bash

    $ pip install pypinyin

为了更好的处理多音字及中英文混合的字符串，
推荐安装 `jieba <https://github.com/fxsjy/jieba>`__ 分词模块。


使用示例
--------

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


分词处理
--------

如果安装了 `jieba <https://github.com/fxsjy/jieba>`__ 分词模块，程序会自动调用。

使用其他分词模块：

1. 安装分词模块，比如 ``pip install snownlp`` ；
2. 使用经过分词处理的字符串列表作参数：

   .. code-block:: python

       >> from pypinyin import lazy_pinyin, STYLE_TONE2
       >> from snownlp import SnowNLP
       >> hans = u'音乐123'
       >>
       >> lazy_pinyin(hans, style=STYLE_TONE2)
       >> [u'yi1n', u'le4', u'1', u'2', u'3']
       >>
       >> hans_seg = SnowNLP(hans).words  # 分词处理
       >> hans_seg
       >> [u'\u97f3\u4e50', u'123']
       >> lazy_pinyin(hans_seg, style=STYLE_TONE2)
       >> [u'yi1n', u'yue4', u'123']


.. |Build| image:: https://api.travis-ci.org/mozillazg/python-pinyin.png?branch=master
   :target: https://travis-ci.org/mozillazg/python-pinyin
.. |Coverage| image:: https://coveralls.io/repos/mozillazg/python-pinyin/badge.png?branch=master
   :target: https://coveralls.io/r/mozillazg/python-pinyin
.. |Pypi version| image:: https://pypip.in/v/pypinyin/badge.png
   :target: https://crate.io/packages/pypinyin
.. |Pypi downloads| image:: https://pypip.in/d/pypinyin/badge.png
   :target: https://crate.io/packages/pypinyin
