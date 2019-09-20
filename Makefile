PYTHON = python3
PIP = ${PYTHON} -m pip
PY_TEST = ${PYTHON} -m pytest


.PHONY: default
default: test lint

.PHONY: deps
deps:
	${PIP} install -e .[dev]

.PHONY: test
test:
	${PY_TEST}

.PHONY: test-ni
test-ni:
	${PY_TEST} -m "not integration"

.PHONY: test-i
test-i:
	${PY_TEST} -m "integration"

.PHONY: coverage
coverage:
	${PY_TEST} --cov-config .coveragerc --cov=./ --cov-report html:htmlcov

.PHONY: lint
lint:
	pylint vakt

.PHONY: release
release: test
	${PYTHON} setup.py sdist upload -r pypi
