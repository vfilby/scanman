#run:
#	python runner.py
#
#test:
#	python -m pytest -p no:warnings tests/
#
#clean:
#	find . -name '*.pyc' -delete
#	find . -name '__pycache__' -type d | xargs rm -fr

local-run: runtime-config
	INTAKE_DIR=runtime/intake \
	COMPLETED_DIR=runtime/completed \
	python scanman/scanman.py

docker:
	docker build -t scanman:development .

runtime-config:
	mkdir -p runtime/intake runtime/completed

docker-run: docker runtime-config
	docker run -it \
		-v $(shell pwd)/runtime/intake:/scanman/intake \
		-v $(shell pwd)/runtime/completed:/scanman/completed \
		scanman:development

docker-shell: docker runtime-config
	docker run -it \
		-v $(shell pwd)/runtime/intake:/scanman/intake \
		-v $(shell pwd)/runtime/completed:/scanman/completed \
		scanman:development bash

test:
	python -m pytest -s ./tests/

env:
	pipenv install
	pipenv shell

clean:
	rm -rf runtime
	rm -rf .pytest_cache

clean-env: clean
	@echo "Exit the pipenv shell and run 'pipenv --rm'"
