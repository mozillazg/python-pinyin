from argparse import ArgumentParser, Namespace
import re
from typing import Union, Text, ByteString, Dict, Any, List

re_pinyin = ...  # type: Any
ACTIONS = ...  # type: Dict[Text, Any]

def re_sub(action: Text, match_obj: re.Match[Text]) -> Text: ...

def prepare(input: Text) -> Text: ...

def convert(action: Text, args: Namespace) -> None: ...

def get_parser() -> ArgumentParser: ...

def main(argv: List[Text]) -> None: ...
