.PHONY: build clean flake8 run

build:
	virtualenv --python=python3 venv
	venv/bin/pip install -e .

flake:
	flake8 .

clean:
	find . -name "*.pyc" -delete
	rm -rf build dist wheels venv *.egg-info

run:
	venv/bin/gunicorn --access-logfile - -w 1 -b 127.0.0.1:5001 stow.server:app --reload
