from django.contrib import admin

from .models import Province, District, Sector, HealthFacility


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')
    search_fields = ('name',)
    list_filter = ('province',)


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'district')
    search_fields = ('name',)
    list_filter = ('district',)


@admin.register(HealthFacility)
class HealthFacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility_type', 'sector')
    search_fields = ('name',)
    list_filter = ('facility_type', 'sector')
