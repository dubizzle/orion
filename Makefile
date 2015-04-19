SHELL = /bin/bash
IMAGE_NAME ?= dubizzledotcom/nazgul
IMAGE_VERSION ?= $(shell git describe --tags HEAD)
GIT_BRANCH = $(shell git rev-parse HEAD)

.PHONY: docker

docker:
	docker build -t $(IMAGE_NAME):$(IMAGE_VERSION) docker

