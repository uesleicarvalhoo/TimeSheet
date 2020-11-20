# Variables
LINE_LENGTH := 120
SRC_DIR := timesheet

run:
	FLASK_APP=$(SRC_DIR)/app.py FLASK_ENV=development flask run

run_docker:
	docker-compose build
	docker-compose up

deploy:
	gunicorn "$(SRC_DIR).app:create_app()" -b 0.0.0.0 -w 4

format:
	black $(SRC_DIR)/* --line-length=$(LINE_LENGTH) --skip-string-normalization
	isort $(SRC_DIR)/* --line-length=$(LINE_LENGTH) --multi-line=0
	flake8 $(SRC_DIR)/* --max-line-length=$(LINE_LENGTH)
