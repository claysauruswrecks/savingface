.PHONY: test
test:
	python3 -m pytest --showlocals --durations=0 --color=yes --tb=long -v -m "not integration"

.PHONY: lint
lint:
	python3 -m isort ./
	python3 -m black ./

.PHONY: lint-check
lint-check:
	python3 -m isort --check --diff ./
	python3 -m black --check --diff ./
