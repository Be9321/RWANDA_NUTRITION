from django.conf import settings
from django.db import models


class CHWProfile(models.Model):
    ROLES = [
        ('chw', 'Community Health Worker'),
        ('officer', 'District/Sector Officer'),
        ('admin', 'System Administrator'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLES, default='chw')
    sector = models.ForeignKey('geography.Sector', on_delete=models.SET_NULL,
                               null=True, blank=True, related_name='workers')
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"