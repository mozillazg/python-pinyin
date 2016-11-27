FAQ
-----


* | Q: 如何禁用“自动调用结巴分词模块”功能：
  | A: 设置环境变量 ``PYPINYIN_NO_JIEBA=true``

* | Q: 如何禁用内置的“词组拼音库”：
  | A: 设置环境变量 ``PYPINYIN_NO_PHRASES=true``

* | Q: ``INITIALS`` 声母风格下，以 ``y``, ``w``, ``yu`` 开头的汉字返回空字符串，例如：

  .. code:: python

      pinyin('火影忍者', style=pypinyin.INITIALS)
      [['h'], [''], ['r'], ['zh']]

  | A: 因为 ``y``, ``w``, ``yu`` 都不是声母。参考: `hotoo/pinyin#57 <https://github.com/hotoo/pinyin/issues/57>`__, `#22 <https://github.com/mozillazg/python-pinyin/pull/22>`__, `#27 <https://github.com/mozillazg/python-pinyin/issues/27>`__,
    `#44 <https://github.com/mozillazg/python-pinyin/issues/44>`__

      声母风格（INITIALS）下，“雨”、“我”、“圆”等汉字返回空字符串，因为根据 `《汉语拼音方案》 <http://www.edu.cn/20011114/3009777.shtml>`__ ， y，w，ü (yu) 都不是声母，在某些特定韵母无声母时，才加上 y 或 w，而 ü 也有其特定规则。
      如果你觉得这个给你带来了麻烦，那么也请小心一些无声母的汉字（如“啊”、“饿”、“按”、“昂”等）。 这时候你也许需要的是首字母风格（FIRST_LETTER）。    —— @hotoo
