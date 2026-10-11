from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class GrowthMeasurement(models.Model):
    child = models.ForeignKey('households.Child', on_delete=models.CASCADE, related_name='measurements')
    measured_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name='measurements')
    measurement_date = models.DateField()
    weight_kg = models.DecimalField(max_digits=4, decimal_places=1,
                                    validators=[MinValueValidator(1), MaxValueValidator(30)])
    height_cm = models.DecimalField(max_digits=4, decimal_places=1,
                                    validators=[MinValueValidator(30), MaxValueValidator(130)])
    muac_cm = models.DecimalField('MUAC (cm)', max_digits=3, decimal_places=1, null=True, blank=True)
    height_for_age_z = models.DecimalField('Height-for-age z-score', max_digits=4, decimal_places=2,
                                           null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-measurement_date']

    def clean(self):
        if self.measurement_date and self.measurement_date > date.today():
            raise ValidationError({'measurement_date': 'Measurement date cannot be in the future.'})

    @property
    def status(self):
        z = self.height_for_age_z
        if z is None:
            return 'Not assessed'
        if z < -3:
            return 'Severely stunted'
        if z < -2:
            return 'Stunted'
        return 'Normal'

    def __str__(self):
        return f"{self.child} on {self.measurement_date}"


class Program(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    children = models.ManyToManyField('households.Child', through='Enrollment', related_name='programs')

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    child = models.ForeignKey('households.Child', on_delete=models.CASCADE, related_name='enrollments')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_on = models.DateField()

    class Meta:
        unique_together = ('child', 'program')

    def __str__(self):
        return f"{self.child} in {self.program}"


class Referral(models.Model):
    STATUS = [('open', 'Open'), ('attended', 'Attended'), ('closed', 'Closed')]

    child = models.ForeignKey('households.Child', on_delete=models.CASCADE, related_name='referrals')
    facility = models.ForeignKey('geography.HealthFacility', on_delete=models.PROTECT, related_name='referrals')
    referred_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name='referrals')
    referral_date = models.DateField()
    reason = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS, default='open')

    class Meta:
        ordering = ['-referral_date']

    def __str__(self):
        return f"{self.child} to {self.facility.name}"