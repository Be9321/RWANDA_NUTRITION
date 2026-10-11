import random
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from geography.models import Province, District, Sector, HealthFacility
from households.models import Household, Child
from nutrition.models import GrowthMeasurement, Program, Enrollment, Referral

# province -> district -> (average z-score, sectors)
PLACES = {
    'Northern': {'Gicumbi': (-1.9, ['Byumba', 'Rukomo']), 'Burera': (-1.8, ['Cyanika', 'Butaro'])},
    'Western': {'Karongi': (-1.6, ['Bwishyura', 'Rubengera']), 'Rubavu': (-1.5, ['Gisenyi', 'Nyamyumba'])},
    'Kigali City': {'Gasabo': (-0.6, ['Kimironko', 'Remera']), 'Nyarugenge': (-0.5, ['Nyamirambo', 'Muhima'])},
    'Eastern': {'Rwamagana': (-1.0, ['Muhazi', 'Kigabiro'])},
}
NAMES = ['Uwase', 'Mugisha', 'Ineza', 'Iradukunda', 'Niyonsenga', 'Umutoni', 'Habimana',
         'Ishimwe', 'Keza', 'Manzi', 'Gasana', 'Uwera', 'Nshuti', 'Mutesi', 'Kamanzi', 'Irakoze']


class Command(BaseCommand):
    help = 'Create synthetic demo data (no real people).'

    def handle(self, *args, **options):
        if Child.objects.exists():
            self.stdout.write('Data already exists. Nothing done.')
            return

        random.seed(42)
        today = timezone.localdate()
        programs = [
            Program.objects.create(name='Community Nutrition Program', start_date=today - timedelta(days=400)),
            Program.objects.create(name='Early Childhood Development (ECD)', start_date=today - timedelta(days=300)),
            Program.objects.create(name='Kitchen Garden Support', start_date=today - timedelta(days=200)),
        ]

        hh_no = 0
        child_no = 0
        for prov_name, districts in PLACES.items():
            province = Province.objects.create(name=prov_name)
            for dist_name, (mean_z, sectors) in districts.items():
                district = District.objects.create(province=province, name=dist_name)
                for sec_name in sectors:
                    sector = Sector.objects.create(district=district, name=sec_name)
                    facility = HealthFacility.objects.create(
                        name=f'{sec_name} Health Center', facility_type='HC', sector=sector)
                    for _ in range(6):
                        hh_no += 1
                        hh = Household.objects.create(
                            household_code=f'HH-{hh_no:04d}',
                            head_name=f'{random.choice(NAMES)} {random.choice(NAMES)}',
                            sector=sector,
                            mother_education=random.choice(['none', 'primary', 'primary', 'secondary', 'higher']),
                            food_security=random.choice(['secure', 'mild', 'severe']),
                            sanitation=random.choice(['improved', 'basic', 'none']),
                            water_source=random.choice(['piped', 'unprotected']),
                            income_category=random.choice(['low', 'low', 'lower_mid', 'middle']),
                        )
                        for _ in range(random.randint(1, 2)):
                            child_no += 1
                            age = random.randint(6, 58)
                            child = Child.objects.create(
                                household=hh,
                                full_name=f'{random.choice(NAMES)} {random.choice(NAMES)}',
                                sex=random.choice(['F', 'M']),
                                date_of_birth=today - timedelta(days=age * 30 + random.randint(0, 29)),
                            )
                            z = random.gauss(mean_z, 1.0)
                            for days_ago in (70, 35, 5):
                                zz = z + random.uniform(-0.3, 0.3)
                                m_age = age - days_ago // 30
                                height = 50 + 1.2 * m_age + zz * 2.5
                                weight = 3.3 + 0.22 * m_age
                                GrowthMeasurement.objects.create(
                                    child=child,
                                    measurement_date=today - timedelta(days=days_ago),
                                    weight_kg=Decimal(str(round(max(weight, 2), 1))),
                                    height_cm=Decimal(str(round(min(max(height, 35), 125), 1))),
                                    height_for_age_z=Decimal(str(round(zz, 2))),
                                )
                            if random.random() < 0.5:
                                Enrollment.objects.create(
                                    child=child, program=random.choice(programs),
                                    enrolled_on=today - timedelta(days=90))
                            if z < -2.5:
                                Referral.objects.create(
                                    child=child, facility=facility,
                                    referral_date=today - timedelta(days=3),
                                    reason='Severe stunting, nutrition assessment',
                                    status='open')
        self.stdout.write(self.style.SUCCESS(f'Created {hh_no} households and {child_no} children.'))