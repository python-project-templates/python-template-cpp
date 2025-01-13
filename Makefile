#########
# BUILD #
#########
.PHONY: develop
develop:  ## setup project for development
	python -m pip install -e .[develop]

.PHONY: build-py build-cpp build
build-py:
	python -m build -w -n

build-cpp:
	python -m hatchling build --hooks-only

build: build-cpp build-py  ## build the project

.PHONY: install
install:  ## install python library
	python -m pip install .

#########
# LINTS #
#########
.PHONY: lint-py lint-cpp lint lints
lint-py:  ## run python linter with ruff
	python -m ruff check python_template_cpp
	python -m ruff format --check python_template_cpp

lint-cpp:  ## run cpp linter
	clang-format --dry-run -Werror -i -style=file `find ./cpp -name "*.*pp"`

lint: lint-cpp lint-py  ## run project linters

# alias
lints: lint

.PHONY: fix-py fix-cpp fix format
fix-py:  ## fix python formatting with ruff
	python -m ruff check --fix python_template_cpp
	python -m ruff format python_template_cpp

fix-cpp:  ## fix cpp formatting
	clang-format -i -style=file `find ./cpp -name "*.*pp"`

fix: fix-cpp fix-py  ## run project autoformatters

# alias
format: fix

################
# Other Checks #
################
.PHONY: check-manifest checks check

check-manifest:  ## check python sdist manifest with check-manifest
	check-manifest -v

checks: check-manifest

# alias
check: checks

#########
# TESTS #
#########
.PHONY: test-py tests-py coverage-py
test-py:  ## run python tests
	python -m pytest -v python_template_cpp/tests

# alias
tests-py: test-py

coverage-py:  ## run python tests and collect test coverage
	python -m pytest -v python_template_cpp/tests --cov=python_template_cpp --cov-report term-missing --cov-report xml

.PHONY: test coverage tests
test: test-py  ## run all tests
coverage: coverage-py  ## run all tests and collect test coverage

# alias
tests: test

###########
# VERSION #
###########
.PHONY: show-version patch minor major

show-version:  ## show current library version
	@bump-my-version show current_version

patch:  ## bump a patch version
	@bump-my-version bump patch

minor:  ## bump a minor version
	@bump-my-version bump minor

major:  ## bump a major version
	@bump-my-version bump major

########
# DIST #
########
.PHONY: dist dist-py dist-check publish

dist-py:  # build python dists
	python -m build -w -s

dist-check:  ## run python dist checker with twine
	python -m twine check dist/*

dist: clean build dist-js dist-py dist-check  ## build all dists

publish: dist  # publish python assets

#########
# CLEAN #
#########
.PHONY: deep-clean clean

deep-clean: ## clean everything from the repository
	git clean -fdx

clean: ## clean the repository
	rm -rf .coverage coverage cover htmlcov logs build dist *.egg-info

############################################################################################

.PHONY: help

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'
