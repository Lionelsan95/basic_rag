# Makefile for Basic RAG System

# Variables
APP = api.app:app
CELERY_APP = celery_app.celery_app

# Targets
.PHONY: install
install:
	pipenv install

.PHONY: run
run:
	uvicorn $(APP) --reload

.PHONY: worker
worker:
	celery -A $(CELERY_APP) worker --loglevel=info

.PHONY: test
test:
	pipenv run pytest tests/

.PHONY: lint
lint:
	pipenv run flake8 .

.PHONY: format
format:
	pipenv run black .

.PHONY: clean
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
