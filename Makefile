# Variables
LINE_LENGTH := 120

run:
	FLASK_APP=timesheet/app.py FLASK_ENV=development flask run

run_docker:
	docker-compose build
	docker-compose up

format:
	black timesheet/* --line-length=$(LINE_LENGTH) --skip-string-normalization
	isort timesheet/* --line-length=$(LINE_LENGTH) --multi-line=0
	flake8 timesheet/* --max-line-length=$(LINE_LENGTH)
