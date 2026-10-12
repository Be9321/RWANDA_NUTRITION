import random
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from geography.models import Province, District, Sector, HealthFacility
from households.models import Household, Child
from nutrition.models import GrowthMeasurement

# province -> (average z-score for the demo, districts)
PROVINCES = {
    'Kigali City': (-0.6, ['Gasabo', 'Kicukiro', 'Nyarugenge']),
    'Northern': (-1.8, ['Burera', 'Gakenke', 'Gicumbi', 'Musanze', 'Rulindo']),
    'Southern': (-1.0, ['Gisagara', 'Huye', 'Kamonyi', 'Muhanga', 'Nyamagabe',
                        'Nyanza', 'Nyaruguru', 'Ruhango']),
    'Eastern': (-1.1, ['Bugesera', 'Gatsibo', 'Kayonza', 'Kirehe', 'Ngoma',
                       'Nyagatare', 'Rwamagana']),
    'Western': (-1.6, ['Karongi', 'Ngororero', 'Nyabihu', 'Nyamasheke',
                       'Rubavu', 'Rusizi', 'Rutsiro']),
}
NAMES = ['Uwase', 'Mugisha', 'Ineza', 'Iradukunda', 'Niyonsenga', 'Umutoni', 'Habimana',
         'Ishimwe', 'Keza', 'Manzi', 'Gasana', 'Uwera', 'Nshuti', 'Mutesi', 'Kamanzi', 'Irakoze']


class Command(BaseCommand):
    help = 'Create all 30 districts, with synthetic demo data for those that have none.'

    def handle(self, *args, **options):
        random.seed(7)
        today = timezone.localdate()
        counter = Household.objects.count()
        filled = 0

        for prov_name, (mean_z, districts) in PROVINCES.items():
            province, _ = Province.objects.get_or_create(name=prov_name)
            for dist_name in districts:
                district, _ = District.objects.get_or_create(province=province, name=dist_name)
                if Household.objects.filter(sector__district=district).exists():
                    continue
                sector, _ = Sector.objects.get_or_create(district=district, name=f'{dist_name} Central')
                facility, _ = HealthFacility.objects.get_or_create(
                    name=f'{dist_name} Health Center', facility_type='HC', sector=sector)
                district_z = mean_z + random.uniform(-0.4, 0.4)

                for _ in range(8):
                    counter += 1
                    code = f'HH-{counter:04d}'
                    while Household.objects.filter(household_code=code).exists():
                        counter += 1
                        code = f'HH-{counter:04d}'
                    hh = Household.objects.create(
                        household_code=code,
                        head_name=f'{random.choice(NAMES)} {random.choice(NAMES)}',
                        sector=sector,
                        mother_education=random.choice(['none', 'primary', 'primary', 'secondary', 'higher']),
                        food_security=random.choice(['secure', 'mild', 'severe']),
                        sanitation=random.choice(['improved', 'basic', 'none']),
                        water_source=random.choice(['piped', 'unprotected']),
                        income_category=random.choice(['low', 'low', 'lower_mid', 'middle']),
                    )
                    for _ in range(random.randint(1, 2)):
                        age = random.randint(6, 58)
                        child = Child.objects.create(
                            household=hh,
                            full_name=f'{random.choice(NAMES)} {random.choice(NAMES)}',
                            sex=random.choice(['F', 'M']),
                            date_of_birth=today - timedelta(days=age * 30 + random.randint(0, 29)),
                        )
                        z = random.gauss(district_z, 1.0)
                        for days_ago in (70, 35, 5):
                            zz = z + random.uniform(-0.3, 0.3)
                            m_age = age - days_ago // 30
                            GrowthMeasurement.objects.create(
                                child=child,
                                measurement_date=today - timedelta(days=days_ago),
                                weight_kg=Decimal(str(round(max(3.3 + 0.22 * m_age, 2), 1))),
                                height_cm=Decimal(str(round(min(max(50 + 1.2 * m_age + zz * 2.5, 35), 125), 1))),
                                height_for_age_z=Decimal(str(round(zz, 2))),
                            )
                filled += 1

        self.stdout.write(self.style.SUCCESS(
            f'Districts in database: {District.objects.count()}. Filled with demo data: {filled}.'))