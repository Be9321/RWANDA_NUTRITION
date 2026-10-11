# Rwanda Nutrition

## Project Overview
Rwanda Nutrition is a Django-based web application for managing nutrition-related information, households, children, and geographical data.

## Technologies
- Python
- Django
- SQLite (development database)
- HTML, CSS, and JavaScript

## Project Apps
- `accounts` — account-related functionality
- `geography` — geographical information
- `households` — household and child records
- `nutrition` — nutrition-related functionality

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
