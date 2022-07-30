A tool for converting Chinese characters to pinyin (Python version)
=====================================================================

|Build| |GitHubAction| |Coverage| |Pypi version| |DOI|


Takes Chinese characters and converts them to pinyin, zhuyin, and Cyrillic.

Based on `hotoo/pinyin <https://github.com/hotoo/pinyin>`__

* Documentation: http://pypinyin.rtfd.io/
* GitHub: https://github.com/mozillazg/python-pinyin
* License: MIT license
* PyPI: https://pypi.org/project/pypinyin
* Python version: 2.7, pypy, pypy3, 3.4, 3.5, 3.6, 3.7, 3.8

.. contents::


Characteristics
----

* Finds the most fitting pinyin based on phrase occurences.
* Has support for characters with two or more readings (heteronyms).
* Has support for simplified, traditional characters, and zhuyin (also known als bopomofo).
* Has support for multiple styles of pinyin and zhuyin (e.g. tone conventions).


Install
----

.. code-block:: bash

    $ pip install pypinyin


Usage cases
--------

Python 3 (For below Python 2, change '中心' to u'中心'):

.. code-block:: python

    >>> from pypinyin import pinyin, lazy_pinyin, Style
    >>> pinyin('中心')
    [['zhōng'], ['xīn']]
    >>> pinyin('中心', heteronym=True)  # make use of heteronym mode
    [['zhōng', 'zhòng'], ['xīn']]
    >>> pinyin('中心', style=Style.FIRST_LETTER)  # set the pinyin style
    [['z'], ['x']]
    >>> pinyin('中心', style=Style.TONE2, heteronym=True)
    [['zho1ng', 'zho4ng'], ['xi1n']]
    >>> pinyin('中心', style=Style.TONE3, heteronym=True)
    [['zhong1', 'zhong4'], ['xin1']]
    >>> pinyin('中心', style=Style.BOPOMOFO)  # zhuyin mode
    [['ㄓㄨㄥ'], ['ㄒㄧㄣ']]
    >>> lazy_pinyin('中心')  # don't include tone information or heteronyms
    ['zhong', 'xin']


**Please take note** ：

* Pinyin results will have no indicators for syllables with a neutral tone,
neither diacritics or numbers. (For the use of '5' for neutral tones, see `article <https://pypinyin.readthedocs.io/zh_CN/master/contrib.html#neutraltonewith5mixin>`__).
* Lazy pinyin results will use 'v' for 'ü'
(for using 'ü', see `article <https://pypinyin.readthedocs.io/zh_CN/master/contrib.html#v2umixin>`__).

Command line tools:

.. code-block:: console

    $ pypinyin 音乐
    yīn yuè
    $ pypinyin -h


Documentation
--------

For more details, see `article <http://pypinyin.rtfd.io/>`__

For project development related question, please refer to `development documents`_.


FAQ
---------

Are there any mistakes in the heteronyms?
+++++++++++++++++++++++++++++

A database of pinyin phrases are used to solve the heteronym problem.
If there turns out to be a mistake, you can use custom pinyin phrases to adapt the database:

.. code-block:: python

    >>> from pypinyin import Style, pinyin, load_phrases_dict
    >>> pinyin('步履蹒跚')
    [['bù'], ['lǚ'], ['mán'], ['shān']]
    >>> load_phrases_dict({'步履蹒跚': [['bù'], ['lǚ'], ['pán'], ['shān']]})
    >>> pinyin('步履蹒跚')
    [['bù'], ['lǚ'], ['pán'], ['shān']]

For more details, see `article <https://pypinyin.readthedocs.io/zh_CN/master/usage.html#custom-dict>`__.

Why are there no y, w, yu as syllable initials?
++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: python

    >>> from pypinyin import Style, pinyin
    >>> pinyin('下雨天', style=Style.INITIALS)
    [['x'], [''], ['t']]

Because according to the standard pinyin rules (`《汉语拼音方案》 <http://www.moe.gov.cn/jyb_sjzl/ziliao/A19/195802/t19580201_186000.html>`__),
'y', 'w', and 'ü' ('yu') are not counted as syllable initials.

    ** If this causes you inconvenience, please also be aware of characters without an initial
    like '啊' ('a'), '饿' ('e'), '按' ('an'), '昂' ('ang'), etc. In this case you might need 'FIRST_LETTER' mode.
	 —— @hotoo

    reference: `hotoo/pinyin#57 <https://github.com/hotoo/pinyin/issues/57>`__,
    `#22 <https://github.com/mozillazg/python-pinyin/pull/22>`__,
    `#27 <https://github.com/mozillazg/python-pinyin/issues/27>`__,
    `#44 <https://github.com/mozillazg/python-pinyin/issues/44>`__

If this is not the desired behaviour, that is if you want 'y' to be counted as an initial,
use 'strict=False'.

.. code-block:: python

    >>> from pypinyin import Style, pinyin
    >>> pinyin('下雨天', style=Style.INITIALS)
    [['x'], [''], ['t']]
    >>> pinyin('下雨天', style=Style.INITIALS, strict=False)
    [['x'], ['y'], ['t']]


How to reduce internal memory load?
++++++++++++++++++++

If you don't care too much about the correctness of pinyin,
you can use the environmental parameters 'PYPINYIN_NO_PHRASES' and 'PYPINYIN_NO_DICT_COPY'
to reduce internal memory load.
For more details, see `article <https://pypinyin.readthedocs.io/zh_CN/master/faq.html#no-phrases>`__


For more FAQ:
`FAQ <https://pypinyin.readthedocs.io/zh_CN/master/faq.html>`__


.. _#13 : https://github.com/mozillazg/python-pinyin/issues/113
.. _strict impact: https://pypinyin.readthedocs.io/zh_CN/master/usage.html#strict


Pinyin data
---------

* Single charachter pinyin usage `pinyin-data`_ data
* Pinyin usage in phrases `phrase-pinyin-data`_ data


Related Projects
-----------------

* `hotoo/pinyin`__: A tool for converting Chinese characters to pinyin, Node.js/JavaScript version.
* `mozillazg/go-pinyin`__: A tool for converting Chinese characters to pinyin, Go version.
* `mozillazg/rust-pinyin`__: A tool for converting Chinese characters to pinyin, Rust version.


__ https://github.com/hotoo/pinyin
__ https://github.com/mozillazg/go-pinyin
__ https://github.com/mozillazg/rust-pinyin


.. |Build| image:: https://img.shields.io/circleci/project/github/mozillazg/python-pinyin/master.svg
   :target: https://circleci.com/gh/mozillazg/python-pinyin
.. |GitHubAction| image:: https://github.com/mozillazg/python-pinyin/workflows/CI/badge.svg
   :target: https://github.com/mozillazg/python-pinyin/actions
.. |Coverage| image:: https://img.shields.io/codecov/c/github/mozillazg/python-pinyin/master.svg
   :target: https://codecov.io/gh/mozillazg/python-pinyin
.. |PyPI version| image:: https://img.shields.io/pypi/v/pypinyin.svg
   :target: https://pypi.org/project/pypinyin/
.. |DOI| image:: https://zenodo.org/badge/12830126.svg
   :target: https://zenodo.org/badge/latestdoi/12830126



.. _Russian translation: https://github.com/mozillazg/python-pinyin/blob/master/README_ru.rst
.. _pinyin-data: https://github.com/mozillazg/pinyin-data
.. _phrase-pinyin-data: https://github.com/mozillazg/phrase-pinyin-data
.. _development documents: https://pypinyin.readthedocs.io/zh_CN/develop/develop.html
