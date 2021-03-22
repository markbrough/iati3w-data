VENV=venv/bin/activate

run-3w: venv
	. $(VENV) && python fetch-3w-data.py

run-iati: venv
	. $(VENV) && python fetch-iati-data.py

venv: requirements.txt
	rm -rf venv
	python3 -m venv venv
	. $(VENV) && pip install -r requirements.txt


