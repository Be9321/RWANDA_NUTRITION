from datetime import date, timedelta
import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from geography.models import District, Province, Sector
from households.models import Child, Household
from .models import GrowthMeasurement
from .ml import measurement_features


class NutritionApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='tester', password='test-password-123')
        province = Province.objects.create(name='Test Province')
        district = District.objects.create(province=province, name='Test District')
        sector = Sector.objects.create(district=district, name='Test Sector')
        household = Household.objects.create(
            household_code='TEST-0001', head_name='Test Household', sector=sector,
        )
        self.child = Child.objects.create(
            household=household,
            full_name='Test Child',
            sex='F',
            date_of_birth=date.today() - timedelta(days=365 * 3),
        )
        self.measurement = GrowthMeasurement.objects.create(
            child=self.child,
            measured_by=self.user,
            measurement_date=date.today(),
            weight_kg=12.0,
            height_cm=85.0,
            height_for_age_z=-2.2,
        )

    def test_measurement_api_requires_login(self):
        response = self.client.get(reverse('measurement_api'))
        self.assertEqual(response.status_code, 302)

    def test_measurement_api_returns_records_and_model_metadata(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('measurement_api'))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['count'], 1)
        self.assertEqual(payload['results'][0]['child'], 'Test Child')
        self.assertIn('model', payload)

    def test_measurement_api_creates_incoming_record(self):
        self.client.force_login(self.user)
        payload = {
            'child': self.child.pk,
            'measurement_date': date.today().isoformat(),
            'weight_kg': '12.5',
            'height_cm': '86.0',
            'muac_cm': '13.0',
            'height_for_age_z': '-1.8',
        }
        response = self.client.post(
            reverse('measurement_api_create'),
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(GrowthMeasurement.objects.count(), 2)
        self.assertIn('prediction', response.json())

    def test_measurement_csv_is_available_to_authenticated_users(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('measurement_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('Test Child', response.content.decode())

    def test_feature_vector_contains_expected_values(self):
        features = measurement_features(self.measurement)
        self.assertEqual(len(features), 9)
        self.assertEqual(features[1], 12.0)
        self.assertEqual(features[4], 1)