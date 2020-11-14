run:
	FLASK_APP=timesheet/app.py FLASK_ENV=development flask run

build:
	docker-compose build
	docker-compose up

format:
	black .
	isort .
