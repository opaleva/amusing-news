SHELL := /bin/bash

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

run:
	python3.9 manage.py runserver

shell:
	python3.9 manage.py shell

migration:
	python3.9 manage.py makemigrations

migrate:
	python3.9 manage.py migrate

super:
	python3.9 manage.py createsuperuser

heroku:
	git push heroku master

deploy:
	docker-compose build
	docker-compose up -d

down:
	docker-compose down