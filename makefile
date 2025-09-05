.PHONY: build run push build-local

build:
	docker build -t audryhsu/worker-basic:latest --platform linux/amd64 .

run:
	docker run -p 8080:8080 audryhsu/worker-basic:latest

push:
	docker push audryhsu/worker-basic:latest
