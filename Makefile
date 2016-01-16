help:
	@echo "test             run test"
	@echo "register         register to PyPI"
	@echo "register_test    register to TestPyPI"
	@echo "publish          publish to PyPI"
	@echo "publish_test     publish to TestPyPI"
	@echo "docs_html        make html docs"

.PHONY: test
test:
	@echo "run test"
	py.test --cov pypinyin tests/ && py.test --cov pypinyin tests/_test_env.py

.PHONY: register
register:
	@echo "register to pypi"
	python setup.py register

.PHONY: publish
publish:
	@echo "publish to pypi"
	python setup.py publish


.PHONY: register_test
register_test:
	python setup.py register -r test

.PHONY: publish_test
publish_test:
	python setup.py sdist upload -r test
	python setup.py bdist_wheel upload -r test

.PHONY: docs_html
docs_html:
	cd docs && make html
