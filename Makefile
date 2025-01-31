run-local:
	docker-compose -f local.yml up

kill-container:
	sudo docker kill learngual-web-1 && sudo docker kill learngual-redis-db-1 && sudo docker kill learngual-db-1

pre-commit:
	pre-commit run --all-files

build-local:
	docker-compose -f local.yml build --no-cache
