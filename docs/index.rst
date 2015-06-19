.. pypinyin documentation master file, created by
   sphinx-quickstart on Fri Sep 06 22:22:13 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. include:: ../README.rst


API
---

拼音风格:

=======================  ====   =====================================================================================
风格                     值     含义
=======================  ====   =====================================================================================
pypinyin.NORMAL          0      普通风格，不带声调。如： ``pin yin``
pypinyin.TONE            1      声调风格1，拼音声调在韵母第一个字母上（默认风格）。如： ``pīn yīn``
pypinyin.TONE2           2      声调风格2，即拼音声调在各个拼音之后，用数字 [0-4] 进行表示。如： ``pi1n yi1n``
pypinyin.INITIALS        3      声母风格，只返回各个拼音的声母部分。如： ``中国`` 的拼音 ``zh g``
pypinyin.FIRST_LETTER    4      首字母风格，只返回拼音的首字母部分。如： ``p y``
pypinyin.FINALS          5      韵母风格1，只返回各个拼音的韵母部分，不带声调。如： ``ong uo``
pypinyin.FINALS_TONE     6      韵母风格2，带声调，声调在韵母第一个字母上。如： ``ōng uó``
pypinyin.FINALS_TONE2    7      韵母风格2，带声调，声调在各个拼音之后，用数字 [0-4] 进行表示。如： ``o1ng uo2``
=======================  ====   =====================================================================================


.. autofunction:: pypinyin.pinyin

.. autofunction:: pypinyin.slug

.. autofunction:: pypinyin.lazy_pinyin

.. autofunction:: pypinyin.load_single_dict

.. autofunction:: pypinyin.load_phrases_dict


TIPS
-----

* | 禁用“自动调用结巴分词模块”功能：
  | 设置环境变量 ``PYPINYIN_NO_JIEBA=true``

* | 禁用内置的“词组拼音库”：
  | 设置环境变量 ``PYPINYIN_NO_PHRASES=true``


.. include:: ../CHANGELOG.rst


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

