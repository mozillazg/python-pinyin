Утилита для фонетической транскрипции китайских иероглифов (Python версия)
============================================================================

|Build| |Coverage| |Pypi version|


Выполняет преобразование китайских иероглифов в пиньин. Можно использовать для фонетики китайских иероглифов, сортировки, просмотра информации.

Основано на `hotoo/pinyin <https://github.com/hotoo/pinyin>`__ проекте.

* Documentation: http://pypinyin.rtfd.io/
* GitHub: https://github.com/mozillazg/python-pinyin
* License: MIT license
* PyPI: https://pypi.python.org/pypi/pypinyin
* Python version: 2.6, 2.7, pypy, 3.3, 3.4, 3.5, 3.6


Особенности
--------------

* Весьма точная транскрипция, основанная на интеллектуальном сопоставлении словосочетаний
* Поддержка иероглифов в несколькими вариантами произношения
* Поддержка простой и полной формы иероглифов, фонетическая поддержка
* Поддержка различных форм пиньина/фонетических стилей


Установка
--------------

.. code-block:: bash

    $ pip install pypinyin


Документация
------------------

Подробную документацию смотрите здесь：http://pypinyin.rtfd.io/


Примеры использования
----------------------------

Python 3(в Python 2 строку ``'中心'`` достаточно заменить на ``u'中心'``):

.. code-block:: python

    >>> from pypinyin import pinyin, lazy_pinyin
    >>> import pypinyin
    >>> pinyin('中心')
    [['zhōng'], ['xīn']]
    >>> pinyin('中心', heteronym=True)  # Задействовать режим выдачи иероглифов с несколькими вариантами произношения (омографы)
    [['zhōng', 'zhòng'], ['xīn']]
    >>> pinyin('中心', style=pypinyin.FIRST_LETTER)  # Настройка фонетического стиля
    [['z'], ['x']]
    >>> pinyin('中心', style=pypinyin.TONE2, heteronym=True)
    [['zho1ng', 'zho4ng'], ['xi1n']]
    >>> pinyin('中心', style=pypinyin.BOPOMOFO)  # Фонетический стиль - чжуи́нь или бопомофо
    [['ㄓㄨㄥ'], ['ㄒㄧㄣ']]
    >>> pinyin('中心', style=pypinyin.CYRILLIC)  # Фонетический стиль - запись кириллицей по системе Палладия
    [['чжун1'], ['синь1']]
    >>> lazy_pinyin('中心')  # Без учета омографов
    ['zhong', 'xin']

Через командную строку:

.. code-block:: console

    $ pypinyin 音乐
    yīn yuè
    $ pypinyin -h


FAQ
---------

Почему y, w, yu не имеют инициалей?
++++++++++++++++++++++++++++++++++++++++++++

    Стиль инициалей （INITIALS） следующих “雨”、“我”、“圆” и других иероглифов возвращает символ пустой строки, так как согласно `"Метод фонетической транскрипции китайских иероглифов" <http://www.moe.gov.cn/jyb_sjzl/ziliao/A19/195802/t19580201_186000.html>`__ , символы y, w, ü (yu) не являются инициалями, при этом к некоторым специальным гласным без согласных букв,добавляется y или w，а также ü согласно специальным правилам    —— @hotoo

    Если вы заметили, что это приносит вам трудности, то пожалуйста повнимательней отнеситесь к некоторым иероглифам без инициалей (например “啊”、“饿”、“按”、“昂” и т.д.). Тогда вам возможно потребуется стиль выдачи инициалей (FIRST_LETTER).    —— @hotoo

    Для справки: `hotoo/pinyin#57 <https://github.com/hotoo/pinyin/issues/57>`__, `#22 <https://github.com/mozillazg/python-pinyin/pull/22>`__, `#27 <https://github.com/mozillazg/python-pinyin/issues/27>`__,
    `#44 <https://github.com/mozillazg/python-pinyin/issues/44>`__


Related Projects
-----------------

* `hotoo/pinyin`__: Утилита для пиньин конвертации китайских иероглифов  Node.js/JavaScript версия.
* `mozillazg/go-pinyin`__: Утилита для пиньин конвертации китайских иероглифов Go версия.
* `mozillazg/rust-pinyin`__: Утилита для пиньин конвертации китайских иероглифов Rust версия.
* `wolfgitpr/cpp-pinyin`__: Утилита для пиньин конвертации китайских иероглифов Cpp версия.


__ https://github.com/hotoo/pinyin
__ https://github.com/mozillazg/go-pinyin
__ https://github.com/mozillazg/rust-pinyin
__ https://github.com/wolfgitpr/cpp-pinyin


.. |Build| image:: https://img.shields.io/travis/mozillazg/python-pinyin/master.svg
   :target: https://travis-ci.org/mozillazg/python-pinyin
.. |Coverage| image:: https://img.shields.io/coveralls/mozillazg/python-pinyin/master.svg
   :target: https://coveralls.io/r/mozillazg/python-pinyin
.. |PyPI version| image:: https://img.shields.io/pypi/v/pypinyin.svg
   :target: https://pypi.python.org/pypi/pypinyin
.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/pypinyin.svg
   :target: https://pypi.python.org/pypi/pypinyin
