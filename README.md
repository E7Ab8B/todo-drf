# ToDo - DRF

ToDo is a personal project which is a backend service for a task management application built using the [Django web framework](https://www.djangoproject.com/).

It offers a RESTful API that enables users to create, modify, and delete tasks, as well as create custom labels for tasks, sub-tasks, and recurring tasks. In addition, ToDo includes task time tracking, notifications, and reminders to help users stay organized and on top of their tasks.

The API can be integrated with a frontend application or service to provide users with an interface for managing their tasks.

## Running Locally

### Create env files

Local environment files should be located in ``./.envs/.local/`` directory.

Needed environment files:

- **.django**
- **.postgres**

Examples of these environment files are available in the same directory.

| Environment Variable | Required | Default
|-----|------|------|
| DJANGO_DEBUG | | False
| DJANGO_SECRET_KEY | |
| DATABASE_URL | ✅ |
| POSTGRES_HOST | ✅ |
| POSTGRES_PORT | ✅ |
| POSTGRES_DB | ✅ |
| POSTGRES_USER | ✅ |
| POSTGRES_PASSWORD | ✅ |
| RABBITMQ_URL | ✅ |
| CELERY_BROKER_URL | ✅ |
| CELERY_FLOWER_USER | ✅ |
| CELERY_FLOWER_PASSWORD | ✅ |
| CELERY_FLOWER_PASSWORD | ✅ |

### Build the Stack

Builds the Docker containers for the local development environment.

```sh
docker-compose -f local.yml build
```

### Run the Stack

```sh
docker compose -f local.yml up
```

To run in a detached (background) mode

```sh
docker compose -f local.yml up -d
```

## Basic Commands

### Migrations

Runs the database migrations.

```sh
docker-compose -f local.yml run --rm django python manage.py migrate
```

### Creating superuser

Creates a new superuser account.

```sh
docker-compose -f local.yml run --rm django python manage.py createsuperuser
```

## Technologies

- [Docker](https://www.docker.com/)
- [django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [pre-commit](https://pre-commit.com/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Sphinx](https://www.sphinx-doc.org/en/master/)
- [OpenAPI 3.0](https://spec.openapis.org/oas/v3.0.3/)
- [PostgreSQL](https://www.postgresql.org/)

## Committing changes

### Setting up development environment

```sh
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements/local.txt
pre-commit install
```

### Running tests and generating coverage HTML report

```sh
docker-compose -f local.yml run --rm django bash -c "pytest && coverage html"
```
