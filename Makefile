VENV=venv/bin/activate

demo-iati:
	. $(VENV) && python fetch-iati-data.py | head -100

demo-3w:
	. $(VENV) && python fetch-3w-data.py | head -100

generate: generate-iati generate-3w

generate-iati:
	. $(VENV) && mkdir -p output && time python fetch-iati-data.py > output/iati-data.json

generate-3w:
	. $(VENV) && mkdir -p output && time python fetch-3w-data.py > output/3w-data.json

venv: requirements.txt
	rm -rf venv
	python3 -m venv venv
	. $(VENV) && pip install -r requirements.txt


