from typing import Union, Text, ByteString


class PinyinNotFoundException(Exception):
    message: Union[Text, ByteString]
    chars: Union[Text, ByteString]

    def __init__(self, chars: Union[Text, ByteString]) -> None: ...
