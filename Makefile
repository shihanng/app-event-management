.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: migrate
migrate: ## Run migration
	poetry run ./manage.py migrate 

.PHONY: add_events
add_events: migrate ## Run populate development server with events
	poetry run ./manage.py loaddata events.json

.PHONY: dev
dev: add_events ## Run development server
	poetry run ./manage.py runserver 5000

.PHONY: test
test: ## Run unit-tests
	poetry run pytest
