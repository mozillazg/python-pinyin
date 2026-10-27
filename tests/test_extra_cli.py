# -*- coding: utf-8 -*-
"""runner（命令行入口）缺口：上游 test_cmd.py 只测了 get_parser 的
默认/自定义两例与 toneconvert，本文件补：
- style_map 全部 24 个别名键的解析结果
- runner.main() 经子进程的真实输出（默认/slug/多参数/管道输入/版本/非法参数）
- NullWriter 与 toneconvert 非法子命令的退出码

子进程一律 stdin=DEVNULL（否则 runner.main 会阻塞读 stdin）；
管道输入用例显式传 input。
"""
from __future__ import unicode_literals

import subprocess
import sys

import pytest

from pypinyin import runner
from pypinyin.tools import toneconvert

SRC = None # 由 conftest 把源码目录加进 sys.path；子进程用 sys.path[0] 的父目录推导


def _src_dir():
    import os
    import pypinyin
    return os.path.dirname(os.path.dirname(os.path.abspath(pypinyin.__file__)))


def _run_cli(args, input_data=None):
    env = dict(__import__('os').environ)
    env['PYTHONPATH'] = _src_dir()
    return subprocess.run(
        [sys.executable, '-m', 'pypinyin'] + args,
        input=input_data, capture_output=True, text=True, env=env, timeout=60,
)


@pytest.mark.parametrize('key', [
    'NORMAL', 'zhao', 'TONE', 'zh4ao', 'TONE2', 'zha4o', 'TONE3', 'zhao4',
    'INITIALS', 'zh', 'FIRST_LETTER', 'z', 'FINALS', 'ao', 'FINALS_TONE',
    '4ao', 'FINALS_TONE2', 'a4o', 'FINALS_TONE3', 'ao4', 'BOPOMOFO',
    'BOPOMOFO_FIRST', 'CYRILLIC', 'CYRILLIC_FIRST',
])
def test_runner_parser_accepts_every_style_alias(key):
    options = runner.get_parser().parse_args(['-s', key, '你好'])
    assert options.style == key
    assert options.hans == ['你好']


def test_runner_parser_multi_hans_and_defaults():
    options = runner.get_parser().parse_args(['你好', '世界'])
    assert options.hans == ['你好', '世界']
    assert options.func == 'pinyin'


def test_runner_null_writer_discards_output():
    writer = runner.NullWriter()
    assert writer.write('anything') is None


def test_cli_default_output():
    result = _run_cli(['你好'])
    assert result.returncode == 0
    assert result.stdout == 'nǐ hǎo\n'


def test_cli_multiple_args_print_one_line_each():
    # 每个命令行参数各打印一行，-p 分隔符只作用于单个参数内部。
    result = _run_cli(['-f', 'slug', '-p', ' ', '你好', '世界'])
    assert result.returncode == 0
    assert result.stdout == 'nǐ hǎo\nshì jiè\n'


def test_cli_tone2_and_heteronym_style_alias():
    result = _run_cli(['-s', 'TONE2', '你好', '世界'])
    assert result.returncode == 0
    assert result.stdout == 'ni3 ha3o\nshi4 jie4\n'
    # zhao 是 NORMAL 的别名；-m 开多音字，中心仍是单读音。
    result = _run_cli(['-s', 'zhao', '-m', '中心'])
    assert result.returncode == 0
    assert result.stdout == 'zhong xin\n'


def test_cli_errors_ignore_drops_no_pinyin_char():
    result = _run_cli(['-e', 'ignore', '中心⺁'])
    assert result.returncode == 0
    assert result.stdout == 'zhōng xīn\n'


def test_cli_version_flag():
    result = _run_cli(['-V'])
    assert result.returncode == 0
    assert result.stdout.strip() == 'pypinyin 0.55.0'


def test_cli_invalid_style_exits_2():
    result = _run_cli(['-s', 'bad', '你好'])
    assert result.returncode == 2
    assert 'invalid choice' in result.stderr


def test_cli_missing_hans_exits_2():
    result = _run_cli([])
    assert result.returncode == 2
    assert 'required' in result.stderr


def test_cli_stdin_pipe_is_appended_as_extra_hans():
    # 管道输入不替代命令行参数，而是追加成一个 hans 参数（会多打印一行）。
    result = _run_cli(['你好'], input_data='世界')
    assert result.returncode == 0
    assert result.stdout == 'nǐ hǎo\nshì jiè\n'
    result = _run_cli(['-f', 'slug', '你好'], input_data='你好')
    assert result.returncode == 0
    assert result.stdout == 'nǐ-hǎo\nnǐ-hǎo\n'


def test_toneconvert_invalid_action_exits_2():
    # toneconvert.main() 会先读 stdin，在 pytest 捕获下直接调用会触发
    # DontReadFromInput，故同样走子进程验证退出码。
    import os
    env = dict(os.environ)
    env['PYTHONPATH'] = _src_dir()
    result = subprocess.run(
        [sys.executable, '-m', 'pypinyin.tools.toneconvert', 'bad-action', 'x'],
        input='', capture_output=True, text=True, env=env, timeout=60,
)
    assert result.returncode == 2
    assert 'invalid choice' in result.stderr
