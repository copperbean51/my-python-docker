IMAGE_NAME=pyimage
CONTAINER=pyshell
TAG_NAME=$(shell date -u "+%Y%m%d")

DOCKER_IMAGE ?= $(IMAGE_NAME):$(TAG_NAME)

# DOCKER TASKS
# Build the container
build: ## Build the container
	docker build -t $(DOCKER_IMAGE) .
