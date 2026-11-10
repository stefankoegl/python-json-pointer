
help:
	@echo "jsonpointer"
	@echo "Makefile targets"
	@echo " - test: run tests"
	@echo " - coverage: run tests with coverage"
	@echo
	@echo "To install jsonpointer, type"
	@echo "  pip install ."
	@echo

test:
	python3 -munittest

coverage:
	coverage run --source=jsonpointer -m unittest
	coverage report -m
