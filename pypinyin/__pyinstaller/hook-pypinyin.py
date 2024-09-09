# reference: https://github.com/pyinstaller/hooksample/blob/master/src/pyi_hooksample/__pyinstaller/hook-pyi_hooksample.py

from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('pypinyin', excludes=['__pyinstaller'])

