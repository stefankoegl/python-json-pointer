
help:
	@echo "jsonpointer"
	@echo "Makefile targets"
	@echo " - test: run tests"
	@echo " - coverage: run tests with coverage"
	@echo
	@echo "To install jsonpointer, type"
	@echo "  python setup.py install"
	@echo

test:
	python tests.py

coverage:
	coverage run --source=jsonpointer tests.py
	coverage report -m
