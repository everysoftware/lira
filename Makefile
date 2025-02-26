APP_PATH = app
TESTS_PATH = tests

.PHONY: run
run:
	docker-compose up db redis -d --build
	python -m app

.PHONY: up
up:
	docker-compose up -d --build

.PHONY: up-prod
up-prod:
	docker-compose up -d --build

.PHONY: generate
generate:
	docker-compose up db redis -d --build
	alembic revision --m="$(NAME)" --autogenerate

.PHONY: upgrade
upgrade:
	docker-compose up db redis -d --build
	alembic upgrade head

.PHONY: format
format:
	ruff format .

.PHONY: lint
lint:
	ruff check . --fix
	mypy $(APP_PATH) --install-types --enable-incomplete-feature=NewGenericSyntax

.PHONY: freeze
freeze:
	pip freeze > requirements-full.txt
