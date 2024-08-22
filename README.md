# Social App

This is a social networking application built with Django and Django Rest Framework.

## Features
- User authentication (signup, login)
- Friend request management (send, accept, reject)
- List of friends
- View pending friend requests

## Prerequisites
- Python 
- PostgreSQL

### Project Setup
1.  python -m venv env (Name of Virtual Environment)
    source env/bin/activate (activate the Virtual Environment)

2.  Install Dependencies
    - pip install -r requirements.txt

3.  Configure the Database
    Ensure your PostgreSQL database is set up and configure in settings.py
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<your-database-name>',
        'USER': '<your-database-user>',
        'PASSWORD': '<your-database-password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
    }

4.  Apply Migrations
    - python manage.py migrate

5.  Run the Development Server
    - python manage.py runserver

6.  Open Postman Collection and import them in Postman
    - Test the API's 

OR using Docker

1.  Start the Containers
    - docker-compose up --build

2.  Run Database Migrations
    - docker-compose exec web python manage.py migrate

3.  Access the application
    - at http://localhost:8000

4.  Test the API's through Postman

5.  Stop the Containers
    docker-compose down
