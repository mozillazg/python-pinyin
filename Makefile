help:
	@echo "register         register to PyPI"
	@echo "register_test    register to TestPyPI"
	@echo "publish          publish to PyPI"
	@echo "publish_test     publish to TestPyPI"

publish:
	@echo "publish to pypi"
	python setup.py publish

register:
	@echo "register to pypi"
	python setup.py register

register_test:
	python setup.py register -r test

publish_test:
	python setup.py sdist upload -r test
	python setup.py bdist_wheel upload -r test
