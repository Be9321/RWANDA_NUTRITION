# Rwanda Nutrition

Community child nutrition surveillance system for Rwanda, built with Django and AdminLTE.

## Overview

Rwanda Nutrition is a Django web application designed to support child nutrition surveillance in Rwanda. It helps health workers track households, record child growth data, monitor program enrollment, and manage referrals for at-risk children.

The system is built to support a practical, data-driven nutrition monitoring workflow for community and district-level decision-making.

## Problem addressed

Malnutrition monitoring requires structured data collection across multiple levels:
- households and household members
- child records and age information
- growth measurements
- referral pathways
- geographic coverage

This project provides a simple and organized solution for managing those relationships in one application.

## Features

- Household registration and record management
- Child registration with validation
- Growth measurement tracking
- Height-for-age z-score monitoring and risk analysis
- Nutrition program enrollment tracking
- Referral management for high-risk children
- AdminLTE dashboard with summary cards and district-level analytics
- Django admin integration for managing application data
- Authentication flow for login/logout

## Tech stack

- Python
- Django
- SQLite
- HTML, CSS, JavaScript
- Bootstrap and AdminLTE
- Chart.js

## Project structure

- `accounts/` — authentication and user-related logic
- `geography/` — provinces, districts, sectors, health facilities
- `households/` — households and children
- `nutrition/` — growth measurements, programs, enrollments, referrals
- `templates/` — shared base layout and page templates
- `config/` — Django project settings and URLs

## Main app relationships

- Province -> District -> Sector -> HealthFacility
- Sector -> Household
- Household -> Child
- Child -> GrowthMeasurement
- Child -> Enrollment -> Program
- Child -> Referral

## Setup instructions

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

### 4. Apply migrations

```powershell
python manage.py migrate
```

### 5. Create a superuser

```powershell
python manage.py createsuperuser
```

### 6. Seed demo data (optional)

```powershell
python manage.py seed_demo
```

### 7. Start the development server

```powershell
python manage.py runserver
```

Open the project in the browser:
- Dashboard: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Default admin access

After creating a superuser, log in using the credentials you set during `createsuperuser`.

## Available pages

- Dashboard
- Households
- Children
- Growth measurements
- Programs
- Referrals
- Admin panel

## Data privacy note

This project uses synthetic/demo data for development and learning purposes. Real child data should never be used without proper ethical approval and compliance with privacy and data protection requirements.

## Security note

Do not commit secret keys, local database files, environment files, or virtual environments to version control.

## Project status

This is a functional Django prototype for the midterm project requirement, covering the main project structure, database modeling, CRUD features, AdminLTE dashboard integration, and project documentation.

