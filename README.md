
# Rwanda Nutrition

Community child nutrition surveillance system for Rwanda, built with Django and AdminLTE.

## Project Overview

Rwanda Nutrition is a Django web application for recording households, children, growth measurements, nutrition programs and referrals, so that community health workers and district officers can identify high-risk children and areas early.

Course: Web Technologies and API Services (Master's in Big Data Analytics)

## Technologies

- Python and Django
- SQLite (development database)
- HTML, CSS, JavaScript
- Bootstrap 4, AdminLTE 3.2.0, Chart.js, DataTables

## Project Apps

- `accounts`: user roles and CHW profiles
- `geography`: provinces, districts, sectors and health facilities
- `households`: household and child records
- `nutrition`: growth measurements, programs, enrolments and referrals

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Be9321/RWANDA_NUTRITION.git
cd RWANDA_NUTRITION
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Set `DJANGO_SECRET_KEY` before starting Django, if the settings file asks for it. Configure any other required variables according to your settings.

### 5. Apply database migrations and load demo data

```powershell
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
```

### 6. Start the development server

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Data note

This prototype uses synthetic data only. Real child data is sensitive and needs ethical approval and compliance with Rwanda's data protection law.

## Security

Do not commit secret keys, passwords, environment files, virtual environments, or local database files to GitHub.

## Team

- Member 1: name
- Member 2: name

## Development Status

This project is under development.

- Python
- Django
- SQLite (development database)
- HTML, CSS, and JavaScript

## Project Apps

- `accounts` â€” account-related functionality
- `geography` â€” geographical information
- `households` â€” household and child records
- `nutrition` â€” nutrition-related functionality

## Setup Instructions

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Rwanda_Nutrition
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Set `DJANGO_SECRET_KEY` before starting Django. Configure any other required environment variables according to your settings.

### 5. Apply database migrations

```powershell
python manage.py migrate
```

### 6. Start the development server

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Security

Do not commit secret keys, passwords, environment files, virtual environments, or local database files to GitHub.

## Development Status

This project is under development.

# RWANDA_NUTRITION

Community child nutrition surveillance system for Rwanda, built with Django and AdminLTE.

