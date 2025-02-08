demo:
	echo TODO 

tests:
	python3 -m pytest tests/

tests_verbose:
	python3 -m pytest tests/ -v

.PHONY: demo tests tests_verbose
