汉语拼音转换工具（Python 版）
=============================

|Build| |Coverage| |Pypi version| |Pypi downloads|


将汉语转为拼音。可以用于汉字注音、排序、检索。

基于 `hotoo/pinyin <https://github.com/hotoo/pinyin>`__ 开发。

* Documentation: http://pypinyin.rtfd.org
* GitHub: https://github.com/mozillazg/python-pinyin
* License: MIT license
* PyPI: https://pypi.python.org/pypi/pypinyin
* Python version: 2.6, 2.7, pypy, 3.3, 3.4


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

详细文档请访问：http://pypinyin.rtfd.org


使用示例
--------

.. code-block:: python

    >>> from pypinyin import pinyin, lazy_pinyin
    >>> import pypinyin
    >>> pinyin(u'中心')
    [[u'zh\u014dng'], [u'x\u012bn']]
    >>> pinyin(u'中心', heteronym=True)  # 启用多音字模式
    [[u'zh\u014dng', u'zh\xf2ng'], [u'x\u012bn']]
    >>> pinyin(u'中心', style=pypinyin.INITIALS)  # 设置拼音风格
    [['zh'], ['x']]
    >>> pinyin('中心', style=pypinyin.TONE2, heteronym=True)
    [['zho1ng', 'zho4ng'], ['xi1n']]
    >>> lazy_pinyin(u'中心')  # 不考虑多音字的情况
    ['zhong', 'xin']

命令行工具：

.. code-block:: console

    $ pypinyin 音乐
    yīn yuè
    $ pypinyin -h


处理不包含拼音的字符
---------------------

当程序遇到不包含拼音的字符(串)时，会根据 ``errors`` 参数的值做相应的处理:

* ``default`` (默认行为): 不做任何处理，原样返回::

      lazy_pinyin(u'你好☆')
      [u'ni', u'hao', u'\u2606']
* ``ignore`` : 忽略该字符 ::

      lazy_pinyin(u'你好☆', errors='ignore')
      [u'ni', u'hao']
* ``replace`` : 替换为去掉 ``\u`` 的 unicode 编码::

      lazy_pinyin(u'你好☆', errors='replace')
      [u'ni', u'hao', u'2606']

* callable 对象 : 提供一个回调函数，接受无拼音字符(串)作为参数,
  支持的返回值类型: ``unicode`` 或 ``list`` ([unicode, ...]) 或 ``None`` 。

  可参考 `单元测试代码`_  ::

      lazy_pinyin(u'你好☆', errors=lambda x: u'star')
      [u'ni', u'hao', u'star']

.. _单元测试代码: https://github.com/mozillazg/python-pinyin/blob/3d52fe821b7f55aecf5af9bad78380762484f4d9/tests/test_pinyin.py#L161-L166


分词处理
--------

* 内置了简单的分词功能，对字符串按是否是中文字符进行分词。

  .. code-block:: python

        >> from pypinyin import lazy_pinyin
        >> lazy_pinyin(u'你好abcこんにちは')
        [u'ni', u'hao', u'abc\u3053\u3093\u306b\u3061\u306f']

  如果需要处理多音字问题，推荐同时安装其他分词模块。

* 如果安装了 `jieba <https://github.com/fxsjy/jieba>`__ 分词模块，程序会自动调用。

* 使用其他分词模块：

    1. 安装分词模块，比如 ``pip install snownlp`` ；
    2. 使用经过分词处理的字符串列表作参数：

       .. code-block:: python

           >> from pypinyin import lazy_pinyin, TONE2
           >> from snownlp import SnowNLP
           >> hans = u'音乐123'
           >> hans_seg = SnowNLP(hans).words  # 分词处理
           >> hans_seg
           [u'\u97f3\u4e50', u'123']
           >> lazy_pinyin(hans_seg, style=TONE2)
           [u'yi1n', u'yue4', u'123']


自定义拼音库
------------

如果对结果不满意，可以通过自定义拼音库的方式修正结果：


**安装了 jieba 分词模块并且支持分词的词组**

.. code-block:: python

    >> from pypinyin import lazy_pinyin, load_phrases_dict, TONE2
    >> hans = u'桔子'
    >> lazy_pinyin(hans, style=TONE2)
    [u'jie2', u'zi3']
    >> load_phrases_dict({u'桔子': [[u'jú'], [u'zǐ']]})
    >> lazy_pinyin(hans, style=TONE2)
    [u'ju2', u'zi3']


**未安装 jieba 分词模块 and/or 不支持分词的词组**

.. code-block:: python

    >> from pypinyin import lazy_pinyin, load_phrases_dict, TONE2, load_single_dict
    >> hans = u'还没'
    >> lazy_pinyin(hans, style=TONE2)
    ['hua2n', 'me2i']
    >>>  # 第一种自定义词组的方法
    >> load_phrases_dict({u'还没': [[u'hái'], [u'méi']]})
    >>> lazy_pinyin(u'还没', style=TONE2)})
    ['hua2n', 'me2i']
    >>> lazy_pinyin([u'还没'], style=TONE2)  # 手动指定 "还没" 为一个词组
    ['ha2i', 'me2i']
    >>>  # 第二种自定义词组的方法
    >> load_single_dict({ord(u'还'): u'hái,huán'})  # 调整 "还" 字的拼音顺序
    >>> lazy_pinyin(u'还没', style=TONE2)
    ['ha2i', 'me2i']


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
