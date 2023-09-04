.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST)  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

##

.PHONY: install
install: ## Install requirements in virtual environment
	pip install -r requirements-dev.txt && pre-commit install;

.PHONY: db-migrate
db-migrate: ## Create migrations file for database
	flask db migrate;

.PHONY: db-upgrade
db-upgrade: ## Perform upgrade to database
	flask db upgrade;

.PHONY: run
run: ## Start the local web server
	python run.py;

.PHONY: test
test: ## Run tests with pytest
	pytest -vv;

.PHONY: docker-up
docker-up: ## Bring up environment in Docker
	docker-compose up --build;

.PHONY: docker-db-upgrade
docker-db-upgrade: ## Perform database upgrade when running in Docker
	docker-compose exec flask_service flask db upgrade;
