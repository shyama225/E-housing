#!/bin/bash

# E-Housing Management Setup Script

echo "Setting up E-Housing Management Application..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate  # For Linux/Mac
# venv\Scripts\activate  # For Windows

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create directories
echo "Creating necessary directories..."
mkdir -p media/profiles
mkdir -p media/properties
mkdir -p static

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations accounts
python manage.py makemigrations properties
python manage.py makemigrations communications
python manage.py migrate

# Create superuser
echo "Creating admin superuser..."
echo "Please create an admin user:"
python manage.py createsuperuser

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setup complete!"
echo "To run the server: python manage.py runserver"
echo "Access the application at: http://127.0.0.1:8000/"
echo "Admin panel: http://127.0.0.1:8000/admin/"
