import json
import pathlib2


def get_template(is_simple: bool = False):
    if not is_simple:
        code = """tmp_{var_name} = json.loads(f.read())
{var_name} = {{}}
for x in tmp_{var_name}:
    {var_name}[int(x)] = tmp_{var_name}[x] # convert string to number directly"""
        return code
    code = """{var_name} = json.loads(f.read())"""
    return code


def export_runner(items: dict, out_file: str, var_name: str, is_simple: bool = False):
    """导出配置文件加载器"""
    db_file = f"{out_file}.json"
    with open(db_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(items, ensure_ascii=False))
    cfg_file_name = pathlib2.Path(db_file).name
    code = """# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pathlib2
import json

# Warning: Auto-generated file, don't edit.
db_path = pathlib2.Path(__file__).parent / '{cfg_file_name}'
with open(db_path, "r", encoding="utf-8") as f:
    {code_template}

""".format(
        cfg_file_name=cfg_file_name,
        code_template=get_template(is_simple),
    ).format(
        var_name=var_name,
    )
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(code)
