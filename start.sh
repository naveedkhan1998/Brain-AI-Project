#!/bin/sh


# Create new database migration files based on model changes
python manage.py makemigrations

# Apply database migrations to the database
python manage.py migrate --noinput


# Start your Django application
python manage.py runserver 0.0.0.0:8080
