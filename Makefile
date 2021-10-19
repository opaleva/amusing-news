SHELL := /bin/bash

deps:
	. ../env/bin/activate && ../env/bin/pip install -U -r requirements.txt

freeze:
	. ../env/bin/activate && ../env/bin/pip freeze > requirements.txt

run:
	python3.9 manage.py runserver ${p}

shell:
	python3.9 manage.py shell

migrations:
	python3.9 manage.py makemigrations ${app}

sql:
	python3.9 manage.py sqlmigrate ${file}

migrate:
	python3.9 manage.py migrate

static:
	python3.9 manage.py collectstatic
super:
	python3.9 manage.py createsuperuser

upd-id:
	sudo -u postgres psql ${db} -c 'ALTER SEQUENCE ${seq} RESTART; UPDATE ${tab} SET id = DEFAULT;'

heroku:
	git push heroku master

deploy:
	docker-compose build
	docker-compose up -d

down:
	docker-compose down