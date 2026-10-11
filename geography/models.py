from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class District(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        unique_together = ('province', 'name')

    def __str__(self):
        return self.name


class Sector(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='sectors')
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        unique_together = ('district', 'name')

    def __str__(self):
        return f"{self.name} ({self.district.name})"


class HealthFacility(models.Model):
    FACILITY_TYPES = [
        ('HP', 'Health Post'),
        ('HC', 'Health Center'),
        ('DH', 'District Hospital'),
        ('RH', 'Referral Hospital'),
    ]
    name = models.CharField(max_length=150)
    facility_type = models.CharField(max_length=2, choices=FACILITY_TYPES, default='HC')
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='facilities')

    class Meta:
        verbose_name_plural = 'health facilities'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_facility_type_display()})"