help:
	@echo "test             run test"
	@echo "publish          publish to PyPI"
	@echo "publish_test     publish to TestPyPI"
	@echo "docs_html        make html docs"
	@echo "docs_serve       serve docs"
	@echo "gen_data         gen pinyin data"
	@echo "gen_pinyin_dict  gen single hanzi pinyin dict"
	@echo "gen_phrases_dict gen phrase hanzi pinyin dict"

.PHONY: test
test:
	@echo "run test"
	py.test --cov pypinyin tests/ && py.test --cov pypinyin tests/_test_env.py

.PHONY: publish
publish:
	@echo "publish to pypi"
	python setup.py register
	python setup.py publish

.PHONY: publish_test
publish_test:
	python setup.py register -r test
	python setup.py sdist upload -r test
	python setup.py bdist_wheel upload -r test

.PHONY: docs_html
docs_html:
	cd docs && make html

.PHONY: docs_serve
docs_serve: docs_html
	cd docs/_build/html && python -m http.server

.PHONY: gen_data
gen_data: gen_pinyin_dict gen_phrases_dict

.PHONY: gen_pinyin_dict
gen_pinyin_dict:
	python gen_pinyin_dict.py pinyin-data/pinyin.txt pypinyin/pinyin_dict.py

.PHONY: gen_phrases_dict
gen_phrases_dict:
	python gen_phrases_dict.py phrase-pinyin-data/pinyin.txt pypinyin/phrases_dict.py
