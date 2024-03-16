include .env
RUN_PYTHON=PYTHONPATH=./ poetry run

build:
	docker compose --file ./docker-compose.dev.yaml build web

dev: format lint build
	docker compose --file ./docker-compose.dev.yaml up --remove-orphans

dev-local: format lint migrate
	docker compose --file ./docker-compose.dev.yaml up postgres redis -d
	${RUN_PYTHON} python ./manage.py runserver

lint:
	${RUN_PYTHON} ruff check --fix ./config ./focussy

format:
	${RUN_PYTHON} ruff format ./config ./focussy

start-ngrok:
	ngrok http 8080

makemigrations:
	$(RUN_PYTHON) poetry run python ./manage.py makemigrations

migrate: makemigrations
	${RUN_PYTHON} python ./manage.py migrate

createsuperuser:
	poetry run python ./manage.py createsuperuser
