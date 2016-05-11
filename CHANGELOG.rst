Changelog
---------


0.12.1 (2016-05-11)
+++++++++++++++++++++

* **[Bugfixed]** 修复一些词语存在拼音粘连在一起的情况. (`#41`_ thanks `@jolly-tao`_ )


0.12.0 (2016-03-12)
+++++++++++++++++++++

* **[Changed]** 单个汉字的拼音数据改为使用来自 `pinyin-data`_ 的拼音数据。
* **[New]** 命令行程序支持从标准输入读取汉字信息::

    $ echo "你好" | pypinyin
    nǐ hǎo
    $ pypinyin < hello.txt
    nǐ hǎo


0.11.1 (2016-02-17)
++++++++++++++++++++

* **[Bugfixed]** 更新 phrases_dict 修复类似 `#36`_ 的问题。thanks `@someus`_


0.11.0 (2016-01-16)
++++++++++++++++++++

* **[Changed]** 分割 ``__init__.py`` 为 ``compat.py``, ``constants.py``， ``core.py`` 和 ``utils.py``。
  影响: ``__init__.py`` 中只保留文档中提到过的 api, 如果使用了不在文档中的 api 则需要调整代码。


0.10.0 (2016-01-02)
++++++++++++++++++++

* **[New]** Python 3.3+ 以上版本默认支持 ``U+20000 ~ U+2FA1F`` 区间内的汉字(详见 `#33`_)


0.9.5 (2015-12-19)
++++++++++++++++++++

* **[Bugfixed]** 修复未正确处理鼻音（详见 `汉语拼音 - 维基百科`_ ）的问题(`#31`_ thanks `@xulin97`_ ):

  * ``ḿ、ń、ň、ǹ`` 对应 “呒”、“呣”、“唔”、“嗯”等字。
    这些字之前在各种风格下都输出原始的汉字而不是拼音。


0.9.4 (2015-11-27)
++++++++++++++++++++

* **[Improved]** 细微调整，主要是更新文档


0.9.3 (2015-11-15)
++++++++++++++++++++

* **[Bugfixed]** Fixed Python 3 compatibility was broken.


0.9.2 (2015-11-15)
++++++++++++++++++++

* **[New]** ``load_single_dict`` 和 ``load_phrases_dict`` 增加 ``style`` 参数支持 TONE2 风格的拼音 ::

      load_single_dict({ord(u'啊'): 'a1'}, style='tone2')
      load_phrases_dict({u"阿爸": [[u"a1"], [u"ba4"]]}, style='tone2'}
* **[Improved]** Improved docs


0.9.1 (2015-10-17)
++++++++++++++++++++

* **[Bugfixed][Changed]** 修复 ``ju``, ``qu``, ``xu``, ``yu``, ``yi`` 和 ``wu`` 的韵母( `#26`_ ). Thanks `@MingStar`_ :

  * ``ju``, ``qu``, ``xu`` 的韵母应该是 ``v``
  * ``yi`` 的韵母是 ``i``
  * ``wu`` 的韵母是 ``u``
  * 从现在开始 ``y`` 既不是声母也不是韵母，详见 `汉语拼音方案`_


0.9.0 (2015-09-20)
++++++++++++++++++++

* **[Changed]** 将拼音词典库里的国际音标字母替换为 ASCII 字母. Thanks `@MingStar`_ :

  * ``ɑ -> a``
  * ``ɡ -> g``


0.8.5 (2015-08-23)
++++++++++++++++++++

* **[Bugfixed]** 修复 zh, ch, sh, z, c, s 顺序问题导致获取声母有误


0.8.4 (2015-08-23)
++++++++++++++++++++

* **[Changed]** ``y``, ``w`` 也不是声母. (`hotoo/pinyin#57 <https://github.com/hotoo/pinyin/issues/57>`__):

  * 以 ``y``, ``w`` 开头的拼音在声母(``INITIALS``)模式下将返回 ``['']``


0.8.3 (2015-08-20)
++++++++++++++++++++

* **[Improved]** 上传到 PyPI 出了点问题，但是又 `没法重新上传 <http://sourceforge.net/p/pypi/support-requests/468/>`__ ，只好新增一个版本


0.8.2 (2015-08-20)
++++++++++++++++++++

* **[Bugfixed][Changed]** 修复误把 yu 放入声母列表里的 BUG(`#22`_). Thanks `@MingStar`_


0.8.1 (2015-07-04)
++++++++++++++++++++

* **[Bugfixed]** 重构内置的分词功能，修复“无法正确处理包含空格的字符串的问题”


0.8.0 (2015-06-27)
+++++++++++++++++++++

* **[New]** 内置简单的分词功能，完善处理没有拼音的字符
  （如果不需要处理多音字问题, 现在可以不用安装 ``jieba`` 或其他分词模块了）::

        # 之前, 安装了结巴分词模块
        lazy_pinyin(u'你好abc☆☆')
        [u'ni', u'hao', 'a', 'b', 'c', u'\u2606', u'\u2606']

        # 现在, 无论是否安装结巴分词模块
        lazy_pinyin(u'你好abc☆☆')
        [u'ni', u'hao', u'abc\u2606\u2606']

* | **[Changed]** 当 ``errors`` 参数是回调函数时，函数的参数由 ``单个字符`` 变更为 ``单个字符或词组`` 。
  | 即: 对于 ``abc`` 字符串, 之前将调用三次 ``errors`` 回调函数: ``func('a') ... func('b') ... func('abc')``
  | 现在只调用一次: ``func('abc')`` 。
* **[Changed]** 将英文字符也纳入 ``errors`` 参数的处理范围::

        # 之前
        lazy_pinyin(u'abc', errors='ignore')
        [u'abc']

        # 现在
        lazy_pinyin(u'abc', errors='ignore')
        []

0.7.0 (2015-06-20)
+++++++++++++++++++++

* **[Bugfixed]** Python 2 下无法使用 ``from pypinyin import *`` 的问题
* **[New]** 支持以下环境变量:

  * ``PYPINYIN_NO_JIEBA=true``: 禁用“自动调用结巴分词模块”
  * ``PYPINYIN_NO_PHRASES=true``: 禁用内置的“词组拼音库”


0.6.0 (2015-06-10)
+++++++++++++++++++++

* **[New]** ``errors`` 参数支持回调函数(`#17`_): ::

    def foobar(char):
        return u'a'
    pinyin(u'あ', errors=foobar)

0.5.7 (2015-05-17)
+++++++++++++++++++

* **[Bugfixed]** 纠正包含 "便宜" 的一些词组的读音


0.5.6 (2015-02-26)
+++++++++++++++++++

* **[Bugfixed]** "苹果" pinyin error. `#11`__
* **[Bugfixed]** 重复 import jieba 的问题
* **[Improved]** 精简 phrases_dict
* **[Improved]** 更新文档

__ https://github.com/mozillazg/python-pinyin/issues/11


0.5.5 (2015-01-27)
+++++++++++++++++++

* **[Bugfixed]** phrases_dict error


0.5.4 (2014-12-26)
+++++++++++++++++++

* **[Bugfixed]** 无法正确处理由分词模块产生的中英文混合词组（比如：B超，维生素C）的问题.  `#8`__

__ https://github.com/mozillazg/python-pinyin/issues/8


0.5.3 (2014-12-07)
+++++++++++++++++++

* **[Improved]** 更新拼音库


0.5.2 (2014-09-21)
++++++++++++++++++

* **[Improved]** 载入拼音库时，改为载入其副本。防止内置的拼音库被破坏
* **[Bugfixed]** ``胜败乃兵家常事`` 的音标问题


0.5.1 (2014-03-09)
++++++++++++++++++

* **[New]** 参数 ``errors`` 用来控制如何处理没有拼音的字符:

  * ``'default'``: 保留原始字符
  * ``'ignore'``: 忽略该字符
  * ``'replace'``: 替换为去掉 ``\u`` 的 unicode 编码字符串(``u'\u90aa'`` => ``u'90aa'``)

  只处理 ``[^a-zA-Z0-9_]`` 字符。


0.5.0 (2014-03-01)
++++++++++++++++++

* **[Changed]** **使用新的单字拼音库内容和格式**

  | 新的格式：``{0x963F: u"ā,ē"}``
  | 旧的格式：``{u'啊': u"ā,ē"}``


0.4.4 (2014-01-16)
++++++++++++++++++

* **[Improved]** 清理命令行命令的输出结果，去除无关信息
* **[Bugfixed]** “ImportError: No module named runner”


0.4.3 (2014-01-10)
++++++++++++++++++

* **[Bugfixed]** 命令行工具在 Python 3 下的兼容性问题


0.4.2 (2014-01-10)
++++++++++++++++++

* **[Changed]** 拼音风格前的 ``STYLE_`` 前缀（兼容包含 ``STYLE_`` 前缀的拼音风格）
* **[New]** 命令行工具，具体用法请见： ``pypinyin -h``


0.4.1 (2014-01-04)
++++++++++++++++++

* **[New]** 支持自定义拼音库，方便用户修正程序结果(``load_single_dict``, ``load_phrases_dict``)


0.4.0 (2014-01-03)
++++++++++++++++++

* **[Changed]** 将 ``jieba`` 模块改为可选安装，用户可以选择使用自己喜爱的分词模块对汉字进行分词处理
* **[New]** 支持 Python 3


0.3.1 (2013-12-24)
++++++++++++++++++

* **[New]** ``lazy_pinyin`` ::

    >>> lazy_pinyin(u'中心')
    ['zhong', 'xin']


0.3.0 (2013-09-26)
++++++++++++++++++

* **[Bugfixed]** 首字母风格无法正确处理只有韵母的汉字

* **[New]** 三个拼音风格:
    * ``pypinyin.STYLE_FINALS`` ：       韵母风格1，只返回各个拼音的韵母部分，不带声调。如： ``ong uo``
    * ``pypinyin.STYLE_FINALS_TONE`` ：   韵母风格2，带声调，声调在韵母第一个字母上。如： ``ōng uó``
    * ``pypinyin.STYLE_FINALS_TONE2`` ：  韵母风格2，带声调，声调在各个拼音之后，用数字 [0-4] 进行表示。如： ``o1ng uo2``


0.2.0 (2013-09-22)
++++++++++++++++++

* **[Improved]** 完善对中英文混合字符串的支持::

    >> pypinyin.pinyin(u'你好abc')
    [[u'n\u01d0'], [u'h\u01ceo'], [u'abc']]


0.1.0 (2013-09-21)
++++++++++++++++++

* **[New]** Initial Release

.. _#17: https://github.com/mozillazg/python-pinyin/pull/17
.. _#22: https://github.com/mozillazg/python-pinyin/pull/22
.. _#26: https://github.com/mozillazg/python-pinyin/pull/26
.. _@MingStar: https://github.com/MingStar
.. _汉语拼音方案: http://www.edu.cn/20011114/3009777.shtml
.. _汉语拼音 - 维基百科: https://zh.wikipedia.org/wiki/%E6%B1%89%E8%AF%AD%E6%8B%BC%E9%9F%B3#cite_ref-10
.. _@xulin97: https://github.com/xulin97
.. _#31: https://github.com/mozillazg/python-pinyin/issues/31
.. _#33: https://github.com/mozillazg/python-pinyin/pull/33
.. _#36: https://github.com/mozillazg/python-pinyin/issues/36
.. _pinyin-data: https://github.com/mozillazg/pinyin-data
.. _@someus: https://github.com/someus
.. _#34: https://github.com/mozillazg/python-pinyin/issues/34
.. _#41: https://github.com/mozillazg/python-pinyin/issues/41
.. _@jolly-tao: https://github.com/jolly-tao
