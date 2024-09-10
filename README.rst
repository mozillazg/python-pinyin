汉字拼音转换工具（Python 版）
=============================

|Build| |GitHubAction| |Coverage| |Pypi version| |PyPI downloads| |DOI|


将汉字转为拼音。可以用于汉字注音、排序、检索(`Russian translation`_) 。

最初版本的代码参考了 `hotoo/pinyin <https://github.com/hotoo/pinyin>`__ 的实现。

* Documentation: https://pypinyin.readthedocs.io/
* GitHub: https://github.com/mozillazg/python-pinyin
* License: MIT license
* PyPI: https://pypi.org/project/pypinyin
* Python version: 2.7, pypy, pypy3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12

.. contents::


特性
----

* 根据词组智能匹配最正确的拼音。
* 支持多音字。
* 简单的繁体支持，注音支持，威妥玛拼音支持。
* 支持多种不同拼音/注音风格。


安装
----

.. code-block:: bash

    pip install pypinyin


使用示例
--------

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
* ``嗯`` 的拼音并不是大部分人以为的 ``en`` 以及存在既没有声母也没有韵母的拼音，详见下方 FAQ 中的说明。

命令行工具：

.. code-block:: console

    $ pypinyin 音乐
    yīn yuè

    $ python -m pypinyin.tools.toneconvert to-tone 'zhong4 xin1'
    zhòng xīn


文档
--------

详细文档请访问：https://pypinyin.readthedocs.io/。

项目代码开发方面的问题可以看看 `开发文档`_ 。


FAQ
---------

拼音有误？
+++++++++++++++++++++++++++++

可以通过下面的方法提高拼音准确性：

* 可以通过自定义词组拼音库或者单字拼音库的方式修正拼音结果，
  详见 `文档 <https://pypinyin.readthedocs.io/zh_CN/master/usage.html#custom-dict>`__ 。

.. code-block:: python

    >> from pypinyin import load_phrases_dict, load_single_dict

    >> load_phrases_dict({'桔子': [['jú'], ['zǐ']]})  # 增加 "桔子" 词组

    >> load_single_dict({ord('还'): 'hái,huán'})  # 调整 "还" 字的拼音顺序或覆盖默认拼音

* 也可以使用 `pypinyin-dict <https://github.com/mozillazg/pypinyin-dict>`__ 项目提供的自定义拼音库来纠正结果。

.. code-block:: python

    # 使用 phrase-pinyin-data 项目中 cc_cedict.txt 文件中的拼音数据优化结果
    >>> from pypinyin_dict.phrase_pinyin_data import cc_cedict
    >>> cc_cedict.load()

    # 使用 pinyin-data 项目中 kXHC1983.txt 文件中的拼音数据优化结果
    >>> from pypinyin_dict.pinyin_data import kxhc1983
    >>> kxhc1983.load()

* 如果是分词导致的拼音有误的话，可以先使用其他的分词模块对数据进行分词处理，
  然后将分词后的词组结果列表作为函数的参数即可:

.. code-block:: python

    >>> # 使用其他分词模块分词，比如 jieba 之类，
    >>> #或者基于 phrases_dict.py 里的词语数据使用其他分词算法分词
    >>> words = list(jieba.cut('每股24.67美元的确定性协议'))
    >>> pinyin(words)

* 如果你希望能通过训练模型的方式提高拼音准确性的话，可以看一下 `pypinyin-g2pW <https://github.com/mozillazg/pypinyin-g2pW>`__ 这个项目。


为什么没有 y, w, yu 几个声母？
++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: python

    >>> from pypinyin import Style, pinyin
    >>> pinyin('下雨天', style=Style.INITIALS)
    [['x'], [''], ['t']]

因为根据 `《汉语拼音方案》 <http://www.moe.gov.cn/jyb_sjzl/ziliao/A19/195802/t19580201_186000.html>`__ ，
y，w，ü (yu) 都不是声母。

    声母风格（INITIALS）下，“雨”、“我”、“圆”等汉字返回空字符串，因为根据
    `《汉语拼音方案》 <http://www.moe.gov.cn/jyb_sjzl/ziliao/A19/195802/t19580201_186000.html>`__ ，
    y，w，ü (yu) 都不是声母，在某些特定韵母无声母时，才加上 y 或 w，而 ü 也有其特定规则。    —— @hotoo

    **如果你觉得这个给你带来了麻烦，那么也请小心一些无声母的汉字（如“啊”、“饿”、“按”、“昂”等）。
    这时候你也许需要的是首字母风格（FIRST_LETTER）**。    —— @hotoo

    参考: `hotoo/pinyin#57 <https://github.com/hotoo/pinyin/issues/57>`__,
    `#22 <https://github.com/mozillazg/python-pinyin/pull/22>`__,
    `#27 <https://github.com/mozillazg/python-pinyin/issues/27>`__,
    `#44 <https://github.com/mozillazg/python-pinyin/issues/44>`__

如果觉得这个行为不是你想要的，就是想把 y 当成声母的话，可以指定 ``strict=False`` ，
这个可能会符合你的预期：

.. code-block:: python

    >>> from pypinyin import Style, pinyin
    >>> pinyin('下雨天', style=Style.INITIALS)
    [['x'], [''], ['t']]
    >>> pinyin('下雨天', style=Style.INITIALS, strict=False)
    [['x'], ['y'], ['t']]

详见 `strict 参数的影响`_ 。

存在既没有声母也没有韵母的拼音？
+++++++++++++++++++++++++++++++++

是的，``strict=True`` 模式下存在极少数既没有声母也没有韵母的拼音。
比如下面这些拼音（来自汉字 ``嗯``、``呒``、``呣``、``唔``）::

    ń ńg ňg ǹg ň ǹ m̄ ḿ m̀

尤其需要注意的是 ``嗯`` 的所有拼音都既没有声母也没有韵母，``呣`` 的默认拼音既没有声母也没有韵母。
详见 `#109`_ `#259`_ `#284`_ 。


如何将某一风格的拼音转换为其他风格的拼音？
++++++++++++++++++++++++++++++++++++++++++++

可以通过 ``pypinyin.contrib.tone_convert`` 模块提供的辅助函数对标准拼音进行转换，得到不同风格的拼音。
比如将 ``zhōng`` 转换为 ``zhong``，或者获取拼音中的声母或韵母数据：

.. code-block:: python

    >>> from pypinyin.contrib.tone_convert import to_normal, to_tone, to_initials, to_finals
    >>> to_normal('zhōng')
    'zhong'
    >>> to_tone('zhong1')
    'zhōng'
    >>> to_initials('zhōng')
    'zh'
    >>> to_finals('zhōng')
    'ong'

更多拼音转换的辅助函数，详见 ``pypinyin.contrib.tone_convert`` 模块的
`文档 <https://pypinyin.readthedocs.io/zh_CN/master/contrib.html#tone-convert>`__ 。


如何减少内存占用？
++++++++++++++++++++

如果对拼音的准确性不是特别在意的话，可以通过设置环境变量 ``PYPINYIN_NO_PHRASES``
和 ``PYPINYIN_NO_DICT_COPY`` 来节省内存。
详见 `文档 <https://pypinyin.readthedocs.io/zh_CN/master/faq.html#no-phrases>`__


更多 FAQ 详见文档中的
`FAQ <https://pypinyin.readthedocs.io/zh_CN/master/faq.html>`__ 部分。


.. _#13 : https://github.com/mozillazg/python-pinyin/issues/113
.. _strict 参数的影响: https://pypinyin.readthedocs.io/zh_CN/master/usage.html#strict


拼音数据
---------

* 单个汉字的拼音使用 `pinyin-data`_ 的数据
* 词组的拼音使用 `phrase-pinyin-data`_ 的数据
* 声母和韵母使用 `《汉语拼音方案》 <http://www.moe.gov.cn/jyb_sjzl/ziliao/A19/195802/t19580201_186000.html>`__ 的数据


Related Projects
-----------------

* `hotoo/pinyin`__: 汉字拼音转换工具 Node.js/JavaScript 版。
* `mozillazg/go-pinyin`__: 汉字拼音转换工具 Go 版。
* `mozillazg/rust-pinyin`__: 汉字拼音转换工具 Rust 版。
* `wolfgitpr/cpp-pinyin`__: 汉字拼音转换工具 c++ 版。
* `wolfgitpr/csharp-pinyin`__: 汉字拼音转换工具 c# 版。


__ https://github.com/hotoo/pinyin
__ https://github.com/mozillazg/go-pinyin
__ https://github.com/mozillazg/rust-pinyin
__ https://github.com/wolfgitpr/cpp-pinyin
__ https://github.com/wolfgitpr/csharp-pinyin


.. |Build| image:: https://img.shields.io/circleci/project/github/mozillazg/python-pinyin/master.svg
   :target: https://circleci.com/gh/mozillazg/python-pinyin
.. |GitHubAction| image:: https://github.com/mozillazg/python-pinyin/workflows/CI/badge.svg
   :target: https://github.com/mozillazg/python-pinyin/actions
.. |Coverage| image:: https://img.shields.io/coveralls/github/mozillazg/python-pinyin/master.svg
   :target: https://coveralls.io/github/mozillazg/python-pinyin
.. |PyPI version| image:: https://img.shields.io/pypi/v/pypinyin.svg
   :target: https://pypi.org/project/pypinyin/
.. |DOI| image:: https://zenodo.org/badge/12830126.svg
   :target: https://zenodo.org/badge/latestdoi/12830126
.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/pypinyin.svg
   :target: https://pypi.org/project/pypinyin/



.. _Russian translation: https://github.com/mozillazg/python-pinyin/blob/master/README_ru.rst
.. _pinyin-data: https://github.com/mozillazg/pinyin-data
.. _phrase-pinyin-data: https://github.com/mozillazg/phrase-pinyin-data
.. _开发文档: https://pypinyin.readthedocs.io/zh_CN/develop/develop.html
.. _#109: https://github.com/mozillazg/python-pinyin/issues/109
.. _#259: https://github.com/mozillazg/python-pinyin/issues/259
.. _#284: https://github.com/mozillazg/python-pinyin/issues/284
