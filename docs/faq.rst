FAQ
-----


.. _no_phrases:


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

    # 使用 pinyin-data 项目中 cc_cedict.txt 文件中的拼音数据优化结果
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



如何禁用内置的“词组拼音库”
++++++++++++++++++++++++++++++++

设置环境变量 ``PYPINYIN_NO_PHRASES=true`` 即可


.. _no_dict_copy:

如何禁用默认的“拼音库”copy 操作
+++++++++++++++++++++++++++++++++++++++++++

设置环境变量 ``PYPINYIN_NO_DICT_COPY=true`` 即可.

副作用: 用户的自定义拼音库出现问题时, 无法回退到自带的拼音库.


.. _limit_memory:

如何减少内存占用
+++++++++++++++++++++

如果对拼音正确性不在意的话，可以按照上面所说的设置环境变量 ``PYPINYIN_NO_PHRASES``
和 ``PYPINYIN_NO_DICT_COPY`` 详见 `#13`_


.. _initials_problem:

``INITIALS`` 声母风格下，以 ``y``, ``w``, ``yu`` 开头的汉字返回空字符串
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

比如：

  .. code:: python

      pinyin('火影忍者', style=Style.INITIALS)
      [['h'], [''], ['r'], ['zh']]


因为 ``y``, ``w``, ``yu`` 都不是声母。参考:
`hotoo/pinyin#57 <https://github.com/hotoo/pinyin/issues/57>`__,
`#22 <https://github.com/mozillazg/python-pinyin/pull/22>`__,
`#27 <https://github.com/mozillazg/python-pinyin/issues/27>`__,
`#44 <https://github.com/mozillazg/python-pinyin/issues/44>`__

  声母风格（INITIALS）下，“雨”、“我”、“圆”等汉字返回空字符串，因为根据
  `《汉语拼音方案》 <http://www.moe.edu.cn/s78/A19/yxs_left/moe_810/s230/195802/t19580201_186000.html>`__ ，
  y，w，ü (yu) 都不是声母，在某些特定韵母无声母时，才加上 y 或 w，而 ü 也有其特定规则。
  如果你觉得这个给你带来了麻烦，那么也请小心一些无声母的汉字（如“啊”、“饿”、“按”、“昂”等）。
  这时候你也许需要的是首字母风格（FIRST_LETTER）。    —— @hotoo

如果觉得这个行为不是你想要的，就是想把 y 当成声母的话，可以指定 ``strict=False`` ， 这个可能会符合你的预期。详见 `strict 参数的影响`_


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


.. _#13: https://github.com/mozillazg/python-pinyin/issues/113
.. _strict 参数的影响: https://pypinyin.readthedocs.io/zh_CN/master/usage.html#strict
.. _#109: https://github.com/mozillazg/python-pinyin/issues/109
.. _#259: https://github.com/mozillazg/python-pinyin/issues/259
.. _#284: https://github.com/mozillazg/python-pinyin/issues/284
