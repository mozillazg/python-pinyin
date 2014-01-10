#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""更新 index.rst"""

from string import Template

readme_rst = '../README.rst'
changelog_rst = '../CHANGELOG.rst'
template_file = 'index.rst.txt'
index_rst = 'index.rst'

kwargs = {}

with open(readme_rst) as f:
    kwargs['readme'] = f.read()
with open(changelog_rst) as f:
    kwargs['changelog'] = f.read()

with open(index_rst, 'w') as f:
    with open(template_file) as f2:
        f.write(Template(f2.read()).safe_substitute(kwargs))
