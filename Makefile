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
	PDF_COMPLETED_HOOK="./test-data/test_complete_hook.sh" \
	python scantool/scantool.py

docker:
	docker build -t scantool:development .

runtime-config:
	mkdir -p runtime/intake runtime/completed
	cp -R test-data/scan* runtime/intake

docker-run: docker runtime-config
	docker run -it \
		-v $(shell pwd)/runtime/intake:/scantool/intake \
		-v $(shell pwd)/runtime/completed:/scantool/completed \
		scantool:development

docker-shell: docker runtime-config
	docker run -it \
		-v $(shell pwd)/runtime/intake:/scantool/intake \
		-v $(shell pwd)/runtime/completed:/scantool/completed \
		-v $(shell pwd)/test-data/test_complete_hook.sh:/scantool/post_pdf_script.sh \
		-e PDF_COMPLETED_HOOK=/scantool/post_pdf_script.sh \
		scantool:development bash

test:
	PYTHONPATH=.:./scantool python -m pytest -s ./tests/

env:
	pipenv install
	pipenv shell

clean:
	rm -rf runtime
	rm -rf .pytest_cache

clean-env: clean
	@echo "Exit the pipenv shell and run 'pipenv --rm'"
