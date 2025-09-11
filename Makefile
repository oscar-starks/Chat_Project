run-local:
	docker-compose -f local.yml up

kill-container:
	sudo docker kill core-web-1 && sudo docker kill core-redis-db-1 && sudo docker kill core-db-1

pre-commit:
	pre-commit run --all-files

build-local:
	docker-compose -f local.yml build --no-cache

make-migrations:
	docker-compose -f local.yml exec web python manage.py makemigrations

migrate:
	docker-compose -f local.yml exec web python manage.py migrate
