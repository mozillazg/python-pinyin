使用
======


示例
-------

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
    >>> lazy_pinyin('中心')  # 不考虑多音字的情况
    ['zhong', 'xin']


命令行工具
------------

.. code-block:: console

    $ pypinyin 音乐
    yīn yuè
    $ pypinyin -h


处理不包含拼音的字符
---------------------

当程序遇到不包含拼音的字符(串)时，会根据 ``errors`` 参数的值做相应的处理:

* ``default`` (默认行为): 不做任何处理，原样返回::

      lazy_pinyin('你好☆☆')
      ['ni', 'hao', '☆☆']
* ``ignore`` : 忽略该字符 ::

      lazy_pinyin('你好☆☆', errors='ignore')
      ['ni', 'hao']
* ``replace`` : 替换为去掉 ``\u`` 的 unicode 编码::

      lazy_pinyin('你好☆☆', errors='replace')
      ['ni', 'hao', '26062606']

* callable 对象 : 提供一个回调函数，接受无拼音字符(串)作为参数,
  支持的返回值类型: ``unicode`` 或 ``list`` ([unicode, ...]) 或 ``None`` 。

  可参考 `单元测试代码`_  ::

      lazy_pinyin('你好☆☆', errors=lambda x: 'star')
      ['ni', 'hao', 'star']

.. _单元测试代码: https://github.com/mozillazg/python-pinyin/blob/3d52fe821b7f55aecf5af9bad78380762484f4d9/tests/test_pinyin.py#L161-L166


分词处理(用于处理多音字和非中文字符)
-----------------------------------------

* 内置了简单的分词功能，对字符串按是否是中文字符进行分词。

  .. code-block:: python

        >> from pypinyin import lazy_pinyin
        >> lazy_pinyin('你好abcこんにちは')
        ['ni', 'hao', 'abcこんにちは']

  如果需要处理多音字问题，推荐同时安装其他分词模块。

* | 如果安装了 `jieba <https://github.com/fxsjy/jieba>`__ 分词模块，程序会自动调用，
  | 也可以使用经过 ``jieba`` 分词处理的 **字符串列表** 作参数。

* 使用其他分词模块：

    1. 安装分词模块，比如 ``pip install snownlp`` ；
    2. 使用经过分词处理的 **字符串列表** 作参数：

       .. code-block:: python

           >> from pypinyin import lazy_pinyin, TONE2
           >> from snownlp import SnowNLP
           >> hans = '音乐123'
           >> hans_seg = SnowNLP(hans).words  # 分词处理
           >> hans_seg
           ['音乐', '123']
           >> lazy_pinyin(hans_seg, style=TONE2)
           ['yi1n', 'yue4', '123']


自定义拼音库
------------

如果对结果不满意，可以通过
:py:func:`~pypinyin.load_single_dict` 或
:py:func:`~pypinyin.load_phrases_dict`
以自定义拼音库的方式修正结果：


**安装了 jieba 分词模块并且支持分词的词组**

.. code-block:: python

    >> from pypinyin import lazy_pinyin, load_phrases_dict, TONE2
    >> hans = '桔子'
    >> lazy_pinyin(hans, style=TONE2)
    ['jie2', 'zi3']
    >> load_phrases_dict({'桔子': [['jú'], ['zǐ']]})
    >> lazy_pinyin(hans, style=TONE2)
    ['ju2', 'zi3']


**未安装 jieba 分词模块 and/or 不支持分词的词组**

.. code-block:: python

    >> from pypinyin import lazy_pinyin, load_phrases_dict, TONE2, load_single_dict
    >> hans = '还没'
    >> lazy_pinyin(hans, style=TONE2)
    ['hua2n', 'me2i']
    >>>  # 第一种自定义词组的方法
    >> load_phrases_dict({'还没': [['hái'], ['méi']]})
    >>> lazy_pinyin('还没', style=TONE2)})
    ['hua2n', 'me2i']
    >>> lazy_pinyin(['还没'], style=TONE2)  # 手动指定 "还没" 为一个词组
    ['ha2i', 'me2i']
    >>>  # 第二种自定义词组的方法
    >> load_single_dict({ord('还'): 'hái,huán'})  # 调整 "还" 字的拼音顺序
    >>> lazy_pinyin('还没', style=TONE2)
    ['ha2i', 'me2i']
