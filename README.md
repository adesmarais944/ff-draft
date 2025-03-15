# FF-Draft
Football drafting application built with Django.

## Setup Options

1. ### Local Development (Windows)
```bash
# Create and activate virtual environment
python -m venv env
env\Scripts\activate

# Install dependencies and run
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

2. ### Docker
```bash

# Build and start containers (Django + PostgreSQL)
docker-compose up

# Rebuild after Dockerfile/requirements changes
docker-compose build
docker-compose up
```