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
	INTAKE_DIR=runtime/intake python app/scanman.py

docker:
	docker build -t scanman:development .

runtime-config:
	mkdir -p runtime/intake runtime/completed

docker-run: docker runtime-config
	docker run -it -v $(shell pwd)/runtime/intake:/scanman/intake scanman:development

docker-shell: docker runtime-config
	docker run -it -v $(shell pwd)/runtime/intake:/scanman/intake scanman:development bash

env:
	pipenv shell

clean:
	rm -rf runtime
