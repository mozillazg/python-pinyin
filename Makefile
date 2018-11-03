help:
	@echo "test             run test"
	@echo "publish          publish to PyPI"
	@echo "publish_test     publish to TestPyPI"
	@echo "docs_html        make html docs"
	@echo "docs_serve       serve docs"
	@echo "gen_data         gen pinyin data"
	@echo "gen_pinyin_dict  gen single hanzi pinyin dict"
	@echo "gen_phrases_dict gen phrase hanzi pinyin dict"
	@echo "lint             run lint"
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"

.PHONY: test
test:
	@echo "run test"
	py.test --cov pypinyin tests/ && py.test --cov pypinyin tests/_test_env.py

.PHONY: publish
publish: clean
	@echo "publish to pypi"
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload dist/*

.PHONY: publish_test
publish_test: clean
	@echo "publish to test pypi"
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload --repository test dist/*

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

.PHONY: lint
lint:
	pre-commit run --all-files
	mypy pypinyin

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
