#run:
#	python runner.py
#
#test:
#	python -m pytest -p no:warnings tests/
#
#clean:
#	find . -name '*.pyc' -delete
#	find . -name '__pycache__' -type d | xargs rm -fr

local-run:
	INTAKE_DIR=. python3 app/scanman.py

docker: requirements
	docker build -t scanman:development .

docker-run: docker
	docker run -it -p 17022:22 -e KNOWN_PUBLIC_KEY="$(shell cat ~/.ssh/id_rsa.pub)" scanman:development /sbin/my_init -- bash -l

test:
	$(shell cat ~/.ssh/id_rsa.pub)

env:
	pipenv shell

requirements: Pipfile
	mkdir -p .build
	pipenv lock --requirements > .build/requirements.txt
