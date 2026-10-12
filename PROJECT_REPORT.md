# Rwanda Nutrition Project Report

## Project summary
Rwanda Nutrition is a Django-based child nutrition surveillance system for Rwanda. The application helps community health workers and district officers monitor household and child nutrition data, track growth measurements, follow up with referrals, and analyze stunting risk across districts and sectors.

## Problem solved
The system provides a practical way to record households, children, nutritional measurements, program enrollments, and referrals. It supports monitoring of children under five and identifies high-risk cases based on the latest height-for-age z-score.

## Application modules
### 1. Geography
The geography app stores the administrative structure:
- Province
- District
- Sector
- HealthFacility

This creates a clean, hierarchical dataset that supports household registration by location.

### 2. Households
The households app records:
- household information
- household head
- village and sector
- socioeconomic risk indicators
- children attached to each household

This allows the system to link nutrition risk with local household conditions.

### 3. Nutrition
The nutrition app tracks:
- growth measurements with weight, height, MUAC and z-score
- nutrition programs and child enrollment
- referrals to health facilities

This is the operational core of the surveillance system.

## Relationships and database design
The project uses meaningful Django model relationships:
- Province -> District (one-to-many)
- District -> Sector (one-to-many)
- Sector -> HealthFacility (one-to-many)
- Sector -> Household (one-to-many)
- Household -> Child (one-to-many)
- Child -> GrowthMeasurement (one-to-many)
- Child -> Enrollment -> Program (many-to-many through model)
- Child -> Referral (one-to-many)

This relationship structure supports accurate demographic, clinical and geographic monitoring.

## Main features implemented
- Django project with multiple apps
- URL routing and view-based logic
- AdminLTE-based dashboard and shared layout
- Dashboard summary cards and district stunting chart
- CRUD pages for households, children, measurements, programs and referrals
- Form validation and error handling
- Django admin registration for the key models
- Demo data generation for Rwanda-style synthetic records
- Authentication flow with login/logout support

## CRUD and validation
The app includes create, read, update and delete operations for the main project entities. Validation logic was implemented for fields such as:
- child names
- household codes and names
- referral reasons
- nutrition measurement dates and values

This ensures the application behaves like a real, maintainable data system.

## AdminLTE dashboard integration
The project uses AdminLTE styling and components, including:
- sidebar navigation
- top navigation bar
- dashboard cards
- tables for records
- consistent layout using a shared base template

## Challenges encountered
The main challenges were:
- structuring the project into multiple Django apps cleanly
- creating consistent CRUD templates and routes
- ensuring data relationships worked as intended
- integrating the dashboard with real database records
- keeping the app aligned with the assignment requirements while maintaining a usable project flow

## Conclusion
The Rwanda Nutrition system presents a functional and realistic prototype for a child nutrition monitoring application. It demonstrates the practical use of Django models, routing, templates, forms, admin integration and dashboard analytics relevant to the midterm project requirement.

## Access and demo credentials
The development server can be started with:

```bash
python manage.py runserver
```

Admin credentials used for testing:
- username: admin
- password: admin123

Main pages to review:
- Dashboard: http://127.0.0.1:8000/
- Children: http://127.0.0.1:8000/households/children/
- Households: http://127.0.0.1:8000/households/
- Measurements: http://127.0.0.1:8000/measurements/
- Programs: http://127.0.0.1:8000/programs/
- Referrals: http://127.0.0.1:8000/referrals/
- Admin: http://127.0.0.1:8000/admin/
