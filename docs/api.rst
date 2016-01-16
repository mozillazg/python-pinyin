API
====


拼音风格:

=======================  ====   =========================================================================================
风格                     值     含义
=======================  ====   =========================================================================================
pypinyin.NORMAL          0      普通风格，不带声调。如： 中国 -> ``zhong guo``
pypinyin.TONE            1      声调风格1，拼音声调在韵母第一个字母上（默认风格）。如： 中国 -> ``zhōng guó``
pypinyin.TONE2           2      声调风格2，即拼音声调在各个拼音之后，用数字 [0-4] 进行表示。如： 中国 -> ``zho1ng guo2``
pypinyin.INITIALS        3      声母风格，只返回各个拼音的声母部分。如： 中国 -> ``zh g``
pypinyin.FIRST_LETTER    4      首字母风格，只返回拼音的首字母部分。如： 中国 -> ``z g``
pypinyin.FINALS          5      韵母风格1，只返回各个拼音的韵母部分，不带声调。如： 中国 -> ``ong uo``
pypinyin.FINALS_TONE     6      韵母风格2，带声调，声调在韵母第一个字母上。如：中国 -> ``ōng uó``
pypinyin.FINALS_TONE2    7      韵母风格2，带声调，声调在各个拼音之后，用数字 [0-4] 进行表示。如： 中国 -> ``o1ng uo2``
=======================  ====   =========================================================================================


.. autofunction:: pypinyin.pinyin

.. autofunction:: pypinyin.lazy_pinyin

.. autofunction:: pypinyin.load_single_dict

.. autofunction:: pypinyin.load_phrases_dict

.. autofunction:: pypinyin.slug
