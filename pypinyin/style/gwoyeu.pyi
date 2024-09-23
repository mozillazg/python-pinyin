from typing import Any, Text, Tuple

GWOYEU_REPLACE = ... # type: Tuple[Tuple[Any]]

class GwoyeuConverter(object):
    def to_wade_glides(self, pinyin: Text, **kwargs: Any) -> Text: ...

    def _pre_convert(self, pinyin: Text) -> Text: ...

converter = ... # type: GwoyeuConverter
