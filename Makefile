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
	flask db upgrade && python seed.py;

.PHONY: run
run: ## Start the local web server
	python run.py;

.PHONY: test
test: ## Run tests with pytest
	pytest -vv;

.PHONY: docker-up
docker-up: ## Bring up environment in Docker
	docker-compose up --build;

.PHONY: docker-down
docker-down: ## Bring down environment in Docker
	docker-compose down;

.PHONY: docker-db-upgrade
docker-db-upgrade: ## Perform database upgrade when running in Docker
	docker-compose exec flask_service flask db upgrade;

.PHONY: docker-db-seed
docker-db-seed: ## Perform database seed when running in Docker
	docker-compose exec flask_service python seed.py;

.PHONY: docker-up-detached
docker-up-detached: ## Bring up environment in Docker detached mode
	docker-compose up --build -d;

.PHONY: docker-run
docker-run: ## Bring up environment in Docker, upgrade and seed database
	$(MAKE) docker-up-detached
	$(MAKE) docker-db-upgrade
	$(MAKE) docker-db-seed
