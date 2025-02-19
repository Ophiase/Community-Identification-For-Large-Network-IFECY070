demo:
	echo TODO 

#########################################

demo_distribution:
	python3 -m demo.distribution test

demo_generation:
	python3 -m demo.generation

demo_identification:
	python3 -m demo.identification

benchmark:
	python3 -m demo.benchmark

###################################################################################

tests:
	python3 -m pytest tests/

tests_verbose:
	python3 -m pytest tests/ -v

###################################################################################

.PHONY: demo tests tests_verbose
