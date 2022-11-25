.DEFAULT_GOAL := help
SHELL = bash


.PHONY: help
help: ## show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## install dependencies
	poetry install --with local
	poetry run pre-commit install

.PHONY: lint
lint: ## lint code
	poetry run isort src tests
	poetry run black src tests
	poetry run flake8 src tests

.PHONY: test-unit
test-unit: ## run unit tests
	poetry run pytest tests --rununit

.PHONY: test
test: ## run all tests
	poetry run pytest tests -vv --cov-report term-missing --cov=src

.PHONY: dev
dev:
	poetry run uvicorn \
		--env-file .env.example --no-access-log --host 0.0.0.0 --port 8080 \
		"src.main:asgi_app"
