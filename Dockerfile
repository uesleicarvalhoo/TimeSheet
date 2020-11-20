# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1


# Install pip requirements
ADD Pipfile .
RUN pip3 install --upgrade pip && pip3 install pipenv
RUN pipenv install

WORKDIR /srv
ADD srv/ ./timesheet
ADD settings.toml .
ADD .secrets.toml .

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /timesheet
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "srv.app:create_app()"]
