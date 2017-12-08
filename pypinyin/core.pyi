from typing import List
from typing import Dict
from typing import Union
from typing import Callable
from typing import Optional
from typing import Text

from pypinyin.constants import Style


TStyle = Style
TErrors = Union[Callable[[Text], Text], Text]
TPinyinResult = List[List[Text]]


def seg(hans: Text) -> List[Text]: ...


def load_single_dict(pinyin_dict: Dict[int, Text],
                     style: str = ...) -> None: ...


def load_phrases_dict(phrases_dict: Dict[Text, List[List[Text]]],
                      style: str = ...
                      ) -> None: ...


def to_fixed(pinyin: Text, style: TStyle,
             strict: bool = ...) -> Text: ...


def _handle_nopinyin_char(chars: Text, errors: TErrors = ...
                          ) -> Optional[Text]: ...


def handle_nopinyin(chars: Text, errors: TErrors = ...
                    ) -> List[Text]: ...


def single_pinyin(han: Text, style: TStyle, heteronym: bool,
                  errors: TErrors = ...,
                  strict: bool = ...
                  ) -> List[Text]: ...


def phrase_pinyin(phrase: Text,
                  style: TStyle,
                  heteronym: bool,
                  errors: TErrors = ...,
                  strict: bool = ...
                  ) -> List[List[Text]]: ...


def _pinyin(words: Text,
            style: TStyle,
            heteronym: bool,
            errors: TErrors,
            strict: bool = ...
            ) -> List[List[Text]]:...


def pinyin(hans: Union[List[Text], Text],
           style: TStyle = ...,
           heteronym: bool = ...,
           errors: TErrors = ...,
           strict: bool = ...
           ) -> List[List[Text]]: ...


def slug(hans: Union[List[Text], Text],
         style: TStyle = ...,
         heteronym: bool = ...,
         separator: Text = ...,
         errors: TErrors = ...,
         strict: bool = ...
         ) -> Text: ...


def lazy_pinyin(hans: Union[List[Text], Text],
                style: TStyle = ...,
                errors: TErrors = ...,
                strict: bool = ...
                ) -> List[Text]: ...
