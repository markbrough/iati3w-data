VENV=venv/bin/activate

run: venv
	. $(VENV) && python fetch-iati-data.py

venv: requirements.txt
	rm -rf venv
	python3 -m venv venv
	. $(VENV) && pip install -r requirements.txt


