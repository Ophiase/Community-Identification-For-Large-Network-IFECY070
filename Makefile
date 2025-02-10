demo:
	echo TODO 

#########################################

demo_distribution:
	python3 -m logic.degree_distribution test

demo_generation:
	python3 -m logic.graph_generation

demo_community_identification:
	python3 -m logic.community_identification

###################################################################################

tests:
	python3 -m pytest tests/

tests_verbose:
	python3 -m pytest tests/ -v

###################################################################################

.PHONY: demo tests tests_verbose
