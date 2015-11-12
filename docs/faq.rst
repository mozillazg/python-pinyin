FAQ
-----


* | Q: 如何禁用“自动调用结巴分词模块”功能：
  | A: 设置环境变量 ``PYPINYIN_NO_JIEBA=true``

* | Q: 如何禁用内置的“词组拼音库”：
  | A: 设置环境变量 ``PYPINYIN_NO_PHRASES=true``

* | Q: ``INITIALS`` 声母风格下，以 ``y``, ``w``, ``yu`` 开头的汉字返回空字符串，例如：

  .. code:: python

      pinyin(u'火影忍者', style=pypinyin.INITIALS)
      [[u'h'], [u''], [u'r'], [u'zh']]

  | A: 因为 ``y``, ``w``, ``yu`` 都不是声母。参考: `hotoo/pinyin#57 <https://github.com/hotoo/pinyin/issues/57>`__, `#22 <https://github.com/mozillazg/python-pinyin/pull/22>`__, `#27 <https://github.com/mozillazg/python-pinyin/issues/27>`__
