# reference: https://github.com/pyinstaller/hooksample/blob/master/src/pyi_hooksample/__pyinstaller/__init__.py  # noqa

import os


def get_hook_dirs():
    return [os.path.dirname(__file__)]
