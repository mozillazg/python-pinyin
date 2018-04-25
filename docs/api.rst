API
====

.. _style:

拼音风格
-----------

.. autoclass:: pypinyin.Style
   :members:
   :undoc-members:
   :member-order: bysource


.. _core_api:

核心 API
-------------

.. autofunction:: pypinyin.pinyin

.. autofunction:: pypinyin.lazy_pinyin

.. autofunction:: pypinyin.load_single_dict

.. autofunction:: pypinyin.load_phrases_dict

.. autofunction:: pypinyin.slug


.. _convert_style:

风格转换
-----------

.. autofunction:: pypinyin.style.register

.. autofunction:: pypinyin.style.convert


.. _seg:

分词
-------

.. autodata:: pypinyin.contrib.mmseg.seg

.. autodata:: pypinyin.contrib.mmseg.retrain

.. autoclass:: pypinyin.contrib.mmseg.Seg
   :members:
   :member-order: bysource


.. _#27: https://github.com/mozillazg/python-pinyin/issues/27
