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

start-dapr:
	dapr run --app-id service-1 --app-port 8001 -- uvicorn core.asgi:application --host 0.0.0.0 --port 8001

stop-dapr:
	dapr stop --app-id service-1
