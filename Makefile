version := $(shell python3 -c 'from jgtml import version; print(version)')

.PHONY: venv
venv:
	[ -d .venv ] || virtualenv .venv --python=jgtml
	conda activate jgtml

.PHONY: piplocal
piplocal:
	pip install -e '.[dev]'

.PHONY: develop
develop: venv piplocal

.PHONY: lint lint-flake8 lint-isort
lint-flake8:
	flake8 test jgtml
lint-isort:
	isort --check-only -rc jgtml test *.py
lint: lint-flake8 lint-isort

.PHONY: format
format:
	isort -rc jgtml test *.py

.PHONY: test
test:
	coverage run -m py.test
	coverage report

.PHONY: readme_check
readme_check:
	./setup.py check --restructuredtext --strict

.PHONY: rst_check
rst_check:
	make readme_check
	# Doesn't generate any output but prints out errors and warnings.
	make -C docs dummy

.PHONY: clean
clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -f
	rm -Rf dist
	rm -Rf *.egg-info

.PHONY: docs
docs:
	cd docs && make html

.PHONY: authors
authors:
	git log --format='%aN <%aE>' `git describe --abbrev=0 --tags`..@ | sort | uniq >> AUTHORS
	cat AUTHORS | sort --ignore-case | uniq >> AUTHORS_
	mv AUTHORS_ AUTHORS

.PHONY: dist
dist:
	make clean
	python -m build

.PHONY: disto
disto:
	make clean
	python setup.py sdist --format=gztar bdist_wheel

.PHONY: pypi-release
pypi-release:
	twine --version
	twine upload -s dist/*

.PHONY: dev-pypi-release
dev-pypi-release:
	twine --version
	twine upload --repository pypi-dev dist/*

.PHONY: dev-release
dev-release:
	python bump_version.py
	make dist
	make dev-pypi-release

.PHONY: bump_version
bump_version:
	python bump_version.py
	git commit . -m "Bump version"

.PHONY: release
release:
	make bump_version
	make dist
	git tag  $(version)
	git push origin $(version)
	git push
	make pypi-release

