run = poetry run

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: migrate
migrate: ## Run migration
	$(run) ./manage.py migrate 

.PHONY: add_events
add_events: migrate ## Run populate development server with events
	$(run) ./manage.py loaddata events.json

.PHONY: dev
dev: add_events ## Run development server
	$(run) ./manage.py runserver 5000

.PHONY: test
test: ## Run unit-tests
	$(run) pytest

.PHONY: flake8
flake8:
	$(run) flake8 --config=setup.cfg 

.PHONY: isort
isort:
	$(run) isort . -c

.PHONY: pylint
pylint:
	$(run) pylint event_management

.PHONY: format
format:
	$(run) black . --check 

.PHONY: mypy
mypy:
	$(run) mypy ./

.PHONY: lint ## Run all linters
lint: isort format flake8 pylint mypy
