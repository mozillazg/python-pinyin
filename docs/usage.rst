使用
======


示例
-------

.. code-block:: python

    >>> from pypinyin import pinyin, lazy_pinyin, Style
    >>> pinyin('中心')
    [['zhōng'], ['xīn']]
    >>> pinyin('中心', heteronym=True)  # 启用多音字模式
    [['zhōng', 'zhòng'], ['xīn']]
    >>> pinyin('中心', style=Style.FIRST_LETTER)  # 设置拼音风格
    [['z'], ['x']]
    >>> pinyin('中心', style=Style.TONE2, heteronym=True)
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


自定义拼音库
------------

如果对结果不满意，可以通过
:py:func:`~pypinyin.load_single_dict` 或
:py:func:`~pypinyin.load_phrases_dict`
以自定义拼音库的方式修正结果：

.. code-block:: python

    >> from pypinyin import lazy_pinyin, load_phrases_dict, Style, load_single_dict
    >> hans = '桔子'
    >> lazy_pinyin(hans, style=Style.TONE2)
    ['jie2', 'zi3']
    >> load_phrases_dict({'桔子': [['jú'], ['zǐ']]})  # 增加 "桔子" 词组
    >> lazy_pinyin(hans, style=Style.TONE2)
    ['ju2', 'zi3']
    >>
    >> hans = '还没'
    >> lazy_pinyin(hans, style=Style.TONE2)
    ['hua2n', 'me2i']
    >> load_single_dict({ord('还'): 'hái,huán'})  # 调整 "还" 字的拼音顺序
    >>> lazy_pinyin('还没', style=Style.TONE2)
    ['ha2i', 'me2i']


自定义拼音风格
----------------

可以通过 :py:func:`~pypinyin.style.register` 来实现自定义拼音风格的需求：

.. code-block:: python

    In [1]: from pypinyin import lazy_pinyin

    In [2]: from pypinyin.style import register

    In [3]: @register('kiss')
       ...: def kiss(pinyin, **kwargs):
       ...:     return '😘 {0}'.format(pinyin)
       ...:

    In [4]: lazy_pinyin('么么', style='kiss')
    Out[4]: ['😘 me', '😘 me']
