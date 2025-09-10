run-local:
	docker-compose -f local.yml up

kill-container:
	sudo docker kill core-web-1 && sudo docker kill core-redis-db-1 && sudo docker kill core-db-1

pre-commit:
	pre-commit run --all-files

build-local:
	docker-compose -f local.yml build --no-cache
