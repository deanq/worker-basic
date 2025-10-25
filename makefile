.PHONY: build run push build-local

build:
	docker build -t deanq/worker-basic:latest --platform linux/amd64 .

run:
	docker run -p 8080:8080 deanq/worker-basic:latest

push:
	docker push deanq/worker-basic:latest
