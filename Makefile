IMAGE_NAME=musync-web-app
CONTAINER_NAME=musync-web-app-container
PROJECT_DIR=$(shell pwd)

.DEFAULT_GOAL := help

.PHONY: help build run stop rm restart logs shell

help: ## Display this help message
	@echo "Usage:"
	@echo "  make <target>"
	@echo
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'


build: ## Build the Docker image
	docker build -t $(IMAGE_NAME) .

run: ## Run the Docker container with the project directory mounted
	docker run -d -p 8000:8000 --name $(CONTAINER_NAME) -v $(PROJECT_DIR):/app $(IMAGE_NAME)

stop: ## Stop the Docker container
	docker stop $(CONTAINER_NAME)

rm: ## Remove the Docker container
	docker rm $(CONTAINER_NAME)

restart: ## Rebuild and restart the Docker container
	stop rm build run

logs: ## Show logs from the Docker container
	docker logs -f $(CONTAINER_NAME)

shell: ## Access the Docker container interactively
	docker exec -it $(CONTAINER_NAME) /bin/bash
