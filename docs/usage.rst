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



命令行工具
------------

程序内置了一个命令行工具 ``pypinyin`` :

.. code-block:: console

    $ pypinyin 音乐
    yīn yuè
    $ pypinyin -h


命令行工具支持如下参数：

.. code-block:: console

    $ pypinyin -h
    usage: pypinyin [-h] [-V] [-f {pinyin,slug}]
                    [-s {NORMAL,zhao,TONE,zh4ao,TONE2,zha4o,TONE3,zhao4,INITIALS,zh,FIRST_LETTER,z,FINALS,ao,FINALS_TONE,4ao,FINALS_TONE2,a4o,FINALS_TONE3,ao4,BOPOMOFO,BOPOMOFO_FIRST,CYRILLIC,CYRILLIC_FIRST}]
                    [-p SEPARATOR] [-e {default,ignore,replace}] [-m]
                    hans

    convert chinese to pinyin.

    positional arguments:
      hans                  chinese string

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -f {pinyin,slug}, --func {pinyin,slug}
                            function name (default: "pinyin")
      -s {NORMAL,zhao,TONE,zh4ao,TONE2,zha4o,TONE3,zhao4,INITIALS,zh,FIRST_LETTER,z,FINALS,ao,FINALS_TONE,4ao,FINALS_TONE2,a4o,FINALS_TONE3,ao4,BOPOMOFO,BOPOMOFO_FIRST,CYRILLIC,CYRILLIC_FIRST}, --style {NORMAL,zhao,TONE,zh4ao,TONE2,zha4o,TONE3,zhao4,INITIALS,zh,FIRST_LETTER,z,FINALS,ao,FINALS_TONE,4ao,FINALS_TONE2,a4o,FINALS_TONE3,ao4,BOPOMOFO,BOPOMOFO_FIRST,CYRILLIC,CYRILLIC_FIRST}
                            pinyin style (default: "zh4ao")
      -p SEPARATOR, --separator SEPARATOR
                            slug separator (default: "-")
      -e {default,ignore,replace}, --errors {default,ignore,replace}
                            how to handle none-pinyin string (default: "default")
      -m, --heteronym       enable heteronym


``-s``, ``--style`` 参数可以选值的含义如下：

================== =========================================
-s 或 --style 的值 对应的拼音风格
================== =========================================
zhao               :py:attr:`~pypinyin.Style.NORMAL`
zh4ao              :py:attr:`~pypinyin.Style.TONE`
zha4o              :py:attr:`~pypinyin.Style.TONE2`
zhao4              :py:attr:`~pypinyin.Style.TONE3`
zh                 :py:attr:`~pypinyin.Style.INITIALS`
z                  :py:attr:`~pypinyin.Style.FIRST_LETTER`
ao                 :py:attr:`~pypinyin.Style.FINALS`
4ao                :py:attr:`~pypinyin.Style.FINALS_TONE`
a4o                :py:attr:`~pypinyin.Style.FINALS_TONE2`
ao4                :py:attr:`~pypinyin.Style.FINALS_TONE3`
NORMAL             :py:attr:`~pypinyin.Style.NORMAL`
TONE               :py:attr:`~pypinyin.Style.TONE`
TONE2              :py:attr:`~pypinyin.Style.TONE2`
TONE3              :py:attr:`~pypinyin.Style.TONE3`
INITIALS           :py:attr:`~pypinyin.Style.INITIALS`
FIRST_LETTER       :py:attr:`~pypinyin.Style.FIRST_LETTER`
FINALS             :py:attr:`~pypinyin.Style.FINALS`
FINALS_TONE        :py:attr:`~pypinyin.Style.FINALS_TONE`
FINALS_TONE2       :py:attr:`~pypinyin.Style.FINALS_TONE2`
FINALS_TONE3       :py:attr:`~pypinyin.Style.FINALS_TONE3`
BOPOMOFO           :py:attr:`~pypinyin.Style.BOPOMOFO`
BOPOMOFO_FIRST     :py:attr:`~pypinyin.Style.BOPOMOFO_FIRST`
CYRILLIC           :py:attr:`~pypinyin.Style.CYRILLIC`
CYRILLIC_FIRST     :py:attr:`~pypinyin.Style.CYRILLIC_FIRST`
================== =========================================
