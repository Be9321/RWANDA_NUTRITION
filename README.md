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
- MySQL 8.4+ for shared/local database use
- SQLite fallback for local development
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

The project uses `DATABASE_URL` when it is configured and falls back to the local `db.sqlite3` SQLite database when it is not. Never commit `.env` or database credentials.

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

The .env file is local configuration and is intentionally not committed. Each team member must create their own .env from .env.example and add a restricted Google Maps API key.

If .env is missing, copy the example:

~~~powershell
Copy-Item .env.example .env
~~~

The .env file should contain:

~~~env
DJANGO_SECRET_KEY=replace-with-a-secure-development-key
GOOGLE_MAPS_API_KEY=your-google-maps-javascript-api-key
DATABASE_URL=mysql://rwanda_user:your_password@127.0.0.1:3306/rwanda_nutrition
~~~

For MySQL, create the database and user before running migrations:

~~~sql
CREATE DATABASE rwanda_nutrition CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'rwanda_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON rwanda_nutrition.* TO 'rwanda_user'@'localhost';
FLUSH PRIVILEGES;
~~~

If the password contains URL-reserved characters, encode them in `DATABASE_URL` (for example, `@` becomes `%40`). Each developer should use a private `.env` file. A `127.0.0.1` database is local to that developer's computer; use a secured hosted MySQL instance if the team needs shared data.
The Google key must be configured in Google Cloud Console with:

- Maps JavaScript API enabled
- HTTP referrer restrictions for local development
- API restrictions limited to the required Google Maps APIs
- Billing enabled if required by the Google Maps account

Never commit the real API key. Restrict it in Google Cloud to the approved development origins and rotate it if it is exposed.

### 5. Apply migrations

~~~powershell
python manage.py migrate
~~~

Migrations create the database schema but do not copy records from another database. To load synthetic data, run the seed commands below. To move an existing SQLite database to MySQL, export it while Django is using SQLite, restore the MySQL `DATABASE_URL`, run migrations, and then load the UTF-8 fixture with `python manage.py loaddata <fixture>.json`.
### 6. Create an administrator

~~~powershell
python manage.py createsuperuser
~~~

### 7. Load synthetic demo data

~~~powershell
python manage.py seed_demo
python manage.py seed_districts
python manage.py train_stunting_model
~~~

These commands can be rerun safely. The data is synthetic and does not represent real people.

### Quick start

After cloning and activating the virtual environment, run:

~~~powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py seed_districts
python manage.py train_stunting_model
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

## Free deployment with Render

The repository includes `render.yaml`, `build.sh`, and production settings for deployment on Render.

1. Create a free Render account and connect the GitHub repository.
2. Create a free PostgreSQL database with a provider such as Neon.
3. Create a Render Web Service from this repository, or use the Blueprint option so Render reads `render.yaml`.
4. Add these environment variables in the Render service:

~~~text
DATABASE_URL=your-postgresql-connection-string
GOOGLE_MAPS_API_KEY=your-restricted-google-maps-javascript-key
~~~

Render generates `DJANGO_SECRET_KEY` automatically from `render.yaml`. The service uses Gunicorn and the build script runs static-file collection, migrations, and synthetic demo-data commands.

Set the final Render hostname in `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`, for example:

~~~text
ALLOWED_HOSTS=nutritrack-rwanda.onrender.com
CSRF_TRUSTED_ORIGINS=https://nutritrack-rwanda.onrender.com
~~~

After deployment, create an administrator from the Render Shell:

~~~bash
python manage.py createsuperuser
~~~

Free services may sleep when idle. The hosted database should be PostgreSQL; SQLite is intended only for local development.
## Project documentation

- Editable ERD source: erd/rwanda_nutrition_erd.dbml
- Rendered ERD diagram: erd/rwanda_nutrition_erd.svg
- Project report: docs/Rwanda Nutrition Project report.pdf
- API contract: docs/openapi.yaml

The ERD source can be pasted into dbdiagram.io for interactive editing.

## Validation and useful commands

~~~powershell
python manage.py check
python manage.py showmigrations
python manage.py test
python manage.py train_stunting_model
~~~

After model changes:

~~~powershell
python manage.py makemigrations
python manage.py migrate
~~~

## Data protection and security

This prototype uses synthetic data only. Real child and household information is sensitive and must be handled according to ethical approval requirements and applicable Rwanda data-protection obligations.

The model is decision-support only and is not a clinical diagnosis. Its training label is derived from the recorded height-for-age z-score, so production use requires independent clinical validation and monitoring for bias.

Before deployment:

- Replace the development secret key
- Set DEBUG=False
- Configure production ALLOWED_HOSTS
- Use a production database
- Restrict and rotate the Google Maps API key
- Configure HTTPS
- Back up the database securely
- Do not commit .env or production secrets
- Rotate any API key that has been exposed

## Team members

| No. | Student ID | Name |
| ---: | --- | --- |
| 1 | 20251MBI021 | Urwidukunda Belyse |
| 2 | 20251MBI006 | Gasarabwe Medard |
| 3 | 20251MBI048 | Turashimye Patience |

## Project status

The project is a functional academic prototype with database migrations, synthetic demo data, authentication, administration, nutrition monitoring, referrals, a Rwanda map, an ERD, and supporting project documentation.
## Prediction API and model training

The project exposes authenticated JSON endpoints backed by the Django database:

- `GET /api/measurements/` returns recent measurements and model risk scores.
- `POST /api/measurements/create/` validates and stores an incoming measurement, then returns its predicted stunting risk.

Train or retrain the model from labelled measurements with:

~~~powershell
python manage.py train_stunting_model
~~~

The classifier uses child age, sex, weight, height, MUAC, and household risk indicators. The training label is whether the recorded height-for-age z-score is below -2. The generated model artifact is stored locally under `model_artifacts/` and is ignored by Git. On deployment, `build.sh` seeds demo data when needed and trains the model automatically.
