from django.contrib import admin
from .models import Province, District, Sector, HealthFacility


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'latitude', 'longitude', 'photo')
    list_filter = ('province',)
    search_fields = ('name',)


admin.site.register(Province)
admin.site.register(Sector)
admin.site.register(HealthFacility)