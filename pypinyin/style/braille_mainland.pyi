# -*- coding: utf-8 -*-
"""中国内地盲文相关的几个拼音风格实现:

Style.BRAILLE_MAINLAND
Style.BRAILLE_MAINLAND_TONE
"""
from typing import Any, Dict, Tuple, Text

BRAILLE_MAINLAND_REPLACE = ...  # type: Tuple[Tuple[Any]]

BRAILLE_MAINLAND_TABLE = ...  # type: Dict[Text, Text]

class BrailleMainlandConverter(object):
    def to_braille_mainland_tone(self, pinyin: Text, **kwargs: Any) -> Text: ...

    def to_braille_mainland(self, pinyin: Text, **kwargs: Any) -> Text: ...

converter = ...  # type: BrailleMainlandConverter
