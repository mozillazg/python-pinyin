使用
======


.. _example:

示例
-------

.. code-block:: python

    >>> from pypinyin import pinyin, lazy_pinyin, Style
    >>> pinyin('中心')  # or pinyin(['中心'])，参数值为列表时表示输入的是已分词后的数据
    [['zhōng'], ['xīn']]
    >>> pinyin('中心', heteronym=True)  # 启用多音字模式
    [['zhōng', 'zhòng'], ['xīn']]
    >>> pinyin('中心', style=Style.FIRST_LETTER)  # 设置拼音风格
    [['z'], ['x']]
    >>> pinyin('中心', style=Style.TONE2, heteronym=True)
    [['zho1ng', 'zho4ng'], ['xi1n']]
    >>> pinyin('中心', style=Style.TONE3, heteronym=True)
    [['zhong1', 'zhong4'], ['xin1']]
    >>> pinyin('中心', style=Style.BOPOMOFO)  # 注音风格
    [['ㄓㄨㄥ'], ['ㄒㄧㄣ']]
    >>> lazy_pinyin('威妥玛拼音', style=Style.WADEGILES)
    ['wei', "t'o", 'ma', "p'in", 'yin']
    >>> lazy_pinyin('上海', style=Style.WADEGILES)
    ['shang', 'hai']
    >>> lazy_pinyin('中心')  # 不考虑多音字的情况
    ['zhong', 'xin']
    >>> lazy_pinyin('战略', v_to_u=True)  # 不使用 v 表示 ü
    ['zhan', 'lüe']
    # 使用 5 标识轻声
    >>> lazy_pinyin('衣裳', style=Style.TONE3, neutral_tone_with_five=True)
    ['yi1', 'shang5']
    # 变调  nǐ hǎo -> ní hǎo
    >>> lazy_pinyin('你好', style=Style.TONE2, tone_sandhi=True)
    ['ni2', 'ha3o']


**注意事项** ：

* 默认情况下拼音结果不会标明哪个韵母是轻声，轻声的韵母没有声调或数字标识（可以通过参数 ``neutral_tone_with_five=True`` 开启使用 ``5`` 标识轻声 ）。
* 默认情况下无声调相关拼音风格下的结果会使用 ``v`` 表示 ``ü`` （可以通过参数 ``v_to_u=True`` 开启使用 ``ü`` 代替 ``v`` ）。
* 默认情况下会原样输出没有拼音的字符（自定义处理没有拼音的字符的方法见 `文档 <https://pypinyin.readthedocs.io/zh_CN/master/usage.html#handle-no-pinyin>`__ ）。


.. _handle_no_pinyin:

处理不包含拼音的字符
---------------------

当程序遇到不包含拼音的字符(串)时，会根据 ``errors`` 参数的值做相应的处理:

* ``default`` (默认行为): 不做任何处理，原样返回::

      pinyin('你好☆☆')
      [['nǐ'], ['hǎo'], ['☆☆']]
* ``ignore`` : 忽略该字符 ::

      pinyin('你好☆☆', errors='ignore')
      [['nǐ'], ['hǎo']]
* ``exception`` : 抛出异常 :class:`~pypinyin.exceptions.PinyinNotFoundException` ::

      pinyin('你好☆☆', errors='ignore')
      [['nǐ'], ['hǎo']]
* ``replace`` : 替换为去掉 ``\u`` 的 unicode 编码::

      pinyin('你好☆☆', errors='replace')
      [['nǐ'], ['hǎo'], ['26062606']]

* callable 对象 : 提供一个回调函数，接受无拼音字符(串)作为参数,
  支持的返回值类型: ``unicode`` 或 ``list`` 或 ``None`` 。::

      pinyin('你好☆☆', errors=lambda x: 'star')
      [['nǐ'], ['hǎo'], ['star']]

      pinyin('你好☆☆', errors=lambda x: None)
      [['nǐ'], ['hǎo']]

  返回值类型为 ``list`` 时，会自动 expend list ::

      pinyin('你好☆☆', errors=lambda x: ['star' for _ in x])
      [['nǐ'], ['hǎo'], ['star'], ['star']]

      # 指定多音字
      pinyin('你好☆☆', heteronym=True, errors=lambda x: [['star', '☆'] for _ in x])
      [['nǐ'], ['hǎo'], ['star', '☆'], ['star', '☆']]


.. _custom_dict:

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

    >> hans = '还没'
    >> lazy_pinyin(hans, style=Style.TONE2)
    ['hua2n', 'me2i']
    >> load_single_dict({ord('还'): 'hái,huán'})  # 调整 "还" 字的拼音顺序或覆盖默认拼音
    >>> lazy_pinyin('还没', style=Style.TONE2)
    ['ha2i', 'me2i']

或者使用 `pypinyin-dict <https://github.com/mozillazg/pypinyin-dict>`__ 项目提供的自定义拼音库来纠正结果:

.. code-block:: python

    >>> from pypinyin import pinyin
    >>> pinyin('枯萎')
    [['kū'], ['wēi']]

    # 使用 phrase-pinyin-data 项目中 cc_cedict.txt 文件中的拼音数据优化结果
    >>> from pypinyin_dict.phrase_pinyin_data import cc_cedict
    >>> cc_cedict.load()

    >>> pinyin('枯萎')
    [['kū'], ['wěi']]


    >>> pinyin('扔', heteronym=True)
    [['rēng', 'rèng']]

    # 使用 pinyin-data 项目中 cc_cedict.txt 文件中的拼音数据优化结果
    >>> from pypinyin_dict.pinyin_data import kxhc1983
    >>> kxhc1983.load()

    >>> pinyin('扔', heteronym=True)
    [['rēng']]

.. _custom_style:

自定义拼音风格
----------------

可以通过 :py:func:`~pypinyin.style.register` 来实现自定义拼音风格的需求：

.. code-block:: python

    In [1]: from pypinyin import lazy_pinyin

    In [2]: from pypinyin.style import register

    In [3]: @register('kiss')
       ...: def kiss(pinyin, **kwargs):     # 必须包含 **kwargs 用于接收未来新增的关键字参数
       ...:     return '😘 {0}'.format(pinyin)
       ...:

    In [4]: lazy_pinyin('么么', style='kiss')
    Out[4]: ['😘 me', '😘 me']


.. _strict:

``strict`` 参数的影响
-------------------------------

``strict`` 参数用于控制处理声母和韵母时是否严格遵循 `《汉语拼音方案》`_ 标准：

.. code-block:: python

    In [1]: from pypinyin import Style, lazy_pinyin

    In [2]: lazy_pinyin('乌', style=Style.TONE)
    Out[2]: ['wū']

    In [3]: lazy_pinyin('乌', style=Style.INITIALS)
    Out[3]: ['']

    In [4]: lazy_pinyin('乌', style=Style.INITIALS, strict=False)
    Out[4]: ['w']

    In [5]: lazy_pinyin('迂', style=Style.TONE)
    Out[5]: ['yū']

    In [6]: lazy_pinyin('迂', style=Style.FINALS_TONE)
    Out[6]: ['ǖ']

    In [7]: lazy_pinyin('迂', style=Style.FINALS_TONE, strict=False)
    Out[7]: ['ū']


当 ``strict=True`` 时根据 `《汉语拼音方案》`_ 的如下规则处理声母、在韵母相关风格下还原正确的韵母
（只对只获取声母或只获取韵母相关拼音风格有效，不影响其他获取完整拼音信息的拼音风格的结果）：

* 21 个声母： ``b p m f d t n l g k h j q x zh ch sh r z c s`` （**y, w 不是声母**）
* i行的韵母，前面没有声母的时候，写成yi(衣)，ya(呀)，ye(耶)，yao(腰)，you(忧)，yan(烟)，
  yin(因)，yang(央)，ying(英)，yong(雍)。（**y 不是声母**）
* u行的韵母，前面没有声母的时候，写成wu(乌)，wa(蛙)，wo(窝)，wai(歪)，wei(威)，wan(弯)，
  wen(温)，wang(汪)，weng(翁)。（**w 不是声母**）
* ü行的韵母，前面没有声母的时候，写成yu(迂)，yue(约)，yuan(冤)，yun(晕)；ü上两点省略。
  （**韵母相关风格下还原正确的韵母 ü**）
* ü行的韵跟声母j，q，x拼的时候，写成ju(居)，qu(区)，xu(虚)，ü上两点也省略；
  但是跟声母n，l拼的时候，仍然写成nü(女)，lü(吕)。（**韵母相关风格下还原正确的韵母 ü**）
* iou，uei，uen前面加声母的时候，写成iu，ui，un。例如niu(牛)，gui(归)，lun(论)。
  （**韵母相关风格下还原正确的韵母 iou，uei，uen**）

当 ``strict=False`` 时就是不遵守上面的规则来处理声母和韵母，
比如：``y``, ``w`` 会被当做声母，yu(迂) 的韵母就是一般认为的 ``u`` 等。

具体差异可以查看 `tests/test_standard.py <https://github.com/mozillazg/python-pinyin/blob/master/tests/test_standard.py>`_ 中的对比结果测试用例


.. _cli:

命令行工具
------------


pypinyin
~~~~~~~~~~~

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


toneconvert
~~~~~~~~~~~~~

通过 ``python -m pypinyin.tools.toneconvert`` 命令可以运行一个辅助转换拼音风格的工具::


    $ python -m pypinyin.tools.toneconvert to-tone 'zhong4 xin1'
    zhòng xīn

**注意**: 当输入包含多个拼音时，必须使用空格或英文逗号分隔，该工具不支持多个拼音连在一起的输入。

该工具支持的命令如下::

    $ python -m pypinyin.tools.toneconvert -h

    usage: toneconvert.py [-h] {to-normal,to-tone,to-tone2,to-tone3} ...

    options:
      -h, --help            show this help message and exit

    subcommands:
      {to-normal,to-tone,to-tone2,to-tone3}
        to-normal           call pypinyin.contrib.tone_convert.to_normal() with inputs
        to-tone             call pypinyin.contrib.tone_convert.to_tone() with inputs
        to-tone2            call pypinyin.contrib.tone_convert.to_tone2() with inputs
        to-tone3            call pypinyin.contrib.tone_convert.to_tone3() with inputs


.. _《汉语拼音方案》: http://www.moe.gov.cn/s78/A19/yxs_left/moe_810/s230/195802/t19580201_186000.html
