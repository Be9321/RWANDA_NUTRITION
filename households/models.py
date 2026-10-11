from django.db import models

# Create your models here.
from datetime import date

from django.core.exceptions import ValidationError
from django.db import models

from geography.models import Sector


class Household(models.Model):
    EDUCATION = [
        ('none', 'No formal education'),
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('higher', 'Higher education'),
    ]
    FOOD_SECURITY = [
        ('secure', 'Food secure'),
        ('mild', 'Mildly food insecure'),
        ('severe', 'Severely food insecure'),
    ]
    SANITATION = [
        ('improved', 'Improved latrine'),
        ('basic', 'Basic latrine'),
        ('none', 'No latrine'),
    ]
    WATER = [
        ('piped', 'Piped or protected source'),
        ('unprotected', 'Unprotected source'),
    ]
    INCOME = [
        ('low', 'Low'),
        ('lower_mid', 'Lower-middle'),
        ('middle', 'Middle'),
        ('high', 'High'),
    ]

    household_code = models.CharField(max_length=20, unique=True)
    head_name = models.CharField('Head of household', max_length=120)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, related_name='households')
    village = models.CharField(max_length=100, blank=True)
    mother_education = models.CharField(max_length=10, choices=EDUCATION, default='primary')
    food_security = models.CharField(max_length=10, choices=FOOD_SECURITY, default='secure')
    sanitation = models.CharField(max_length=10, choices=SANITATION, default='basic')
    water_source = models.CharField(max_length=12, choices=WATER, default='piped')
    income_category = models.CharField(max_length=10, choices=INCOME, default='low')
    registered_on = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['household_code']

    def __str__(self):
        return f"{self.household_code} - {self.head_name}"


class Child(models.Model):
    SEX = [('F', 'Female'), ('M', 'Male')]

    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='children')
    full_name = models.CharField(max_length=120)
    sex = models.CharField(max_length=1, choices=SEX)
    date_of_birth = models.DateField()
    birth_weight_kg = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'children'
        ordering = ['full_name']

    def clean(self):
        if self.date_of_birth and self.date_of_birth > date.today():
            raise ValidationError({'date_of_birth': 'Date of birth cannot be in the future.'})
        if self.date_of_birth and self.age_in_months > 59:
            raise ValidationError({'date_of_birth': 'This system tracks children under 5 years only.'})

    @property
    def age_in_months(self):
        today = date.today()
        months = (today.year - self.date_of_birth.year) * 12 + (today.month - self.date_of_birth.month)
        if today.day < self.date_of_birth.day:
            months -= 1
        return max(months, 0)

    def __str__(self):
        return self.full_name