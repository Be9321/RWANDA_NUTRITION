# NutriTrack Rwanda

NutriTrack Rwanda is a Django web application for community child nutrition surveillance. It helps community health workers, district officers, and administrators record households, monitor children under five, track growth measurements, manage nutrition programmes, and follow up referrals.

This project was developed for the **Web Technologies and API Services** course in the **Master's in Big Data Analytics** programme.

## Main capabilities

- Secure user authentication and Django administration
- Community health worker profiles and role classification
- Rwanda province, district, sector, and health-facility management
- Household registration and socio-economic indicators
- Child registration and under-five age validation
- Growth measurements including weight, height, MUAC, and height-for-age z-score
- Stunting-rate dashboard and Rwanda district map
- Nutrition programme enrolment
- Referrals to health facilities
- Synthetic demo data for testing and presentations
- Professional entity relationship diagram and project report

## Technology stack

- Python 3.15
- Django 6.1.2
- SQLite for local development
- HTML, CSS, and JavaScript
- Bootstrap 4 and AdminLTE 3.2
- Google Maps JavaScript API
- Pillow, Chart.js, and DataTables

## Application structure

| App | Responsibility |
| --- | --- |
| accounts | Authentication, user roles, and community health worker profiles |
| geography | Provinces, districts, sectors, and health facilities |
| households | Household and child records |
| nutrition | Growth measurements, programmes, enrolments, and referrals |
| config | Django project settings and URL configuration |

## Database relationships

The main relationship chain is:

Province -> District -> Sector -> Household -> Child

Nutrition services connect to children through growth measurements, programme enrolment through the Enrollment join table, and referrals to health facilities. Community health worker profiles are assigned to sectors.

The local SQLite database is created as db.sqlite3 after migrations are applied.

## Installation

### 1. Clone the project

~~~powershell
git clone https://github.com/Be9321/RWANDA_NUTRITION.git
cd RWANDA_NUTRITION
~~~

### 2. Create and activate the virtual environment

~~~powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
~~~

If PowerShell blocks activation, run the project interpreter directly:

~~~powershell
.\\.venv\\Scripts\\python.exe manage.py migrate
~~~

### 3. Install dependencies

~~~powershell
pip install -r requirements.txt
~~~

### 4. Configure the Google Maps API

This is a private academic repository. The shared development .env file is included so team members can run the map after cloning.

If .env is missing, copy the example:

~~~powershell
Copy-Item .env.example .env
~~~

The .env file should contain:

~~~env
DJANGO_SECRET_KEY=replace-with-a-secure-development-key
GOOGLE_MAPS_API_KEY=your-google-maps-javascript-api-key
~~~

The Google key must be configured in Google Cloud Console with:

- Maps JavaScript API enabled
- HTTP referrer restrictions for local development
- API restrictions limited to the required Google Maps APIs
- Billing enabled if required by the Google Maps account

Because the shared key is for a private academic repository, restrict it carefully and rotate it before any public or production deployment.

### 5. Apply migrations

~~~powershell
python manage.py migrate
~~~

### 6. Create an administrator

~~~powershell
python manage.py createsuperuser
~~~

### 7. Load synthetic demo data

~~~powershell
python manage.py seed_demo
python manage.py seed_districts
~~~

These commands can be rerun safely. The data is synthetic and does not represent real people.

### Quick start

After cloning and activating the virtual environment, run:

~~~powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py seed_districts
python manage.py runserver
~~~
### 8. Start the development server

~~~powershell
python manage.py runserver
~~~

Open the application at:

- Main application: http://127.0.0.1:8000/
- Login: http://127.0.0.1:8000/accounts/login/
- Django admin: http://127.0.0.1:8000/admin/
- Stunting map: http://127.0.0.1:8000/geography/map/

## Project documentation

- Editable ERD source: erd/rwanda_nutrition_erd.dbml
- Rendered ERD diagram: erd/rwanda_nutrition_erd.svg
- Project report: docs/Rwanda Nutrition Project report.pdf

The ERD source can be pasted into dbdiagram.io for interactive editing.

## Validation and useful commands

~~~powershell
python manage.py check
python manage.py showmigrations
python manage.py test
~~~

After model changes:

~~~powershell
python manage.py makemigrations
python manage.py migrate
~~~

## Data protection and security

This prototype uses synthetic data only. Real child and household information is sensitive and must be handled according to ethical approval requirements and applicable Rwanda data-protection obligations.

Before deployment:

- Replace the development secret key
- Set DEBUG=False
- Configure production ALLOWED_HOSTS
- Use a production database
- Restrict and rotate the Google Maps API key
- Configure HTTPS
- Back up the database securely
- Do not use the shared development key in production

## Team members

| No. | Student ID | Name |
| ---: | --- | --- |
| 1 | 20251MBI021 | Urwidukunda Belyse |
| 2 | 20251MBI006 | Gasarabwe Medard |
| 3 | 20251MBI048 | Turashimye Patience |

## Project status

The project is a functional academic prototype with database migrations, synthetic demo data, authentication, administration, nutrition monitoring, referrals, a Rwanda map, an ERD, and supporting project documentation.


