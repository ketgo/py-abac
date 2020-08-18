PYTHON = python3
PIP = ${PYTHON} -m pip
PY_TEST = ${PYTHON} -m pytest

MARK ?= ""
COVERAGE_OPTS ?=


.PHONY: default
default: test lint

.PHONY: deps
deps:
	${PIP} install -e .[dev]

.PHONY: test
test:
	${PY_TEST} -m ${MARK}

.PHONY: coverage
coverage:
	${PY_TEST} -m ${MARK} --cov-config .coveragerc --cov=./ --cov-report html:htmlcov ${COVERAGE_OPTS}

.PHONY: lint
lint:
	pylint py_abac

.PHONY: security
security:
	bandit -r py_abac

.PHONY: release
release: test
	${PYTHON} setup.py sdist
	twine upload dist/*
