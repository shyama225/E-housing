@echo off
REM E-Housing Management Setup Script for Windows

echo Setting up E-Housing Management Application...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create directories
echo Creating necessary directories...
mkdir media\profiles 2>nul
mkdir media\properties 2>nul
mkdir static 2>nul

REM Run migrations
echo Running database migrations...
python manage.py makemigrations accounts
python manage.py makemigrations properties
python manage.py makemigrations communications
python manage.py migrate

REM Create superuser
echo Creating admin superuser...
echo Please create an admin user:
python manage.py createsuperuser

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

echo Setup complete!
echo To run the server: python manage.py runserver
echo Access the application at: http://127.0.0.1:8000/
echo Admin panel: http://127.0.0.1:8000/admin/
pause
