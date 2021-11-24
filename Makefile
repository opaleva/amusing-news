SHELL := /bin/bash

deps:
	. ../env/bin/activate && ../env/bin/pip install -U -r requirements.txt

freeze:
	. ../env/bin/activate && ../env/bin/pip freeze > requirements.txt

run:
	#python3.9 manage.py runserver ${p}
	gunicorn news_portal.asgi:application -b 192.168.0.101:8000 -t 1800 -k uvicorn.workers.UvicornWorker

prod:
	python3.9 manage.py runserver --insecure

shell:
	python3.9 manage.py shell

migrations:
	python3.9 manage.py makemigrations ${app}

sql:
	python3.9 manage.py sqlmigrate ${file}

migrate:
	python3.9 manage.py migrate

super:
	python3.9 manage.py createsuperuser

test:
	python3.9 manage.py test

upd-id:
	sudo -u postgres psql ${db} -c 'ALTER SEQUENCE ${seq} RESTART; UPDATE ${tab} SET id = DEFAULT;'

deploy:
	docker-compose build
	docker-compose up -d

down:
	docker-compose down

redis:
	docker-compose up redis