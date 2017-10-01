FAQ
-----


如何禁用“自动调用结巴分词模块”功能
+++++++++++++++++++++++++++++++++++++


设置环境变量 ``PYPINYIN_NO_JIEBA=true`` 即可


如何禁用内置的“词组拼音库”
++++++++++++++++++++++++++++++++

设置环境变量 ``PYPINYIN_NO_PHRASES=true`` 即可


``INITIALS`` 声母风格下，以 ``y``, ``w``, ``yu`` 开头的汉字返回空字符串
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

比如：

  .. code:: python

      pinyin('火影忍者', style=pypinyin.INITIALS)
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


自定义了词典，但是结果没用使用自定义词典中的拼音信息？
++++++++++++++++++++++++++++++++++++++++++++++++++++++

自定义的词语在你使用的分词模块（比如：jieba）中没有被切分为一个词语，
可以考虑使用内置的最大匹配分词器来分词或者训练使用的分词模块。

.. code-block:: python

    >>> from pypinyin import pinyin, load_phrases_dict
    >>> load_phrases_dict({'了局': [['liǎo'], ['jú']]})
    >>> pinyin('了局啊')   # 使用 jieba 分词
    Building prefix dict from the default dictionary ...
    Dumping model to file cache /var/folders/s6/z9r_07h53pj_d4x7qjszwmbw0000gn/T/jieba.cache
    Loading model cost 1.175 seconds.
    Prefix dict has been built succesfully.
    [['le'], ['jú'], ['a']]

    >>> from pypinyin.contrib.mmseg import seg, retrain
    >>> retrain(seg)     # 没有使用 load_phrases_dict 时可以不调用这个函数
    >>> pinyin(seg.cut('了局啊'))  # 使用内置的最大匹配分词
    [['liǎo'], ['jú'], ['a']]
    >>>
