help:
	@echo "test             run test"
	@echo "publish          publish to PyPI"
	@echo "publish_test     publish to TestPyPI"
	@echo "docs_html        make html docs"
	@echo "gen_pinyin_dict  gen pinyin dict"

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

.PHONY: gen_pinyin_dict
gen_pinyin_dict:
	python gen_pinyin_dict.py pinyin-data/pinyin.txt pypinyin/pinyin_dict.py
