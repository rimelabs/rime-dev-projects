PYTHON ?= python3
PROJECT ?=

.PHONY: add render check test

add:
	@test -n "$(PROJECT)" || (echo "Usage: make add PROJECT=/path/to/project.json" && exit 2)
	$(PYTHON) scripts/add_project.py --file "$(PROJECT)"

render:
	$(PYTHON) scripts/render_catalog.py

test:
	$(PYTHON) -m unittest discover -s tests

check:
	$(PYTHON) scripts/check_catalog.py
	$(PYTHON) scripts/render_catalog.py --check
	$(PYTHON) -m compileall -q scripts
	$(PYTHON) -m unittest discover -s tests
