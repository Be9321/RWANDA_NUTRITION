from django.contrib import admin

from .models import GrowthMeasurement, Program, Enrollment, Referral


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date')
    search_fields = ('name',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('child', 'program', 'enrolled_on')
    list_filter = ('program',)


@admin.register(GrowthMeasurement)
class GrowthMeasurementAdmin(admin.ModelAdmin):
    list_display = ('child', 'measurement_date', 'weight_kg', 'height_cm', 'status')
    list_filter = ('measurement_date',)
    search_fields = ('child__full_name',)


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('child', 'facility', 'referral_date', 'status')
    list_filter = ('status', 'facility')
    search_fields = ('child__full_name', 'reason')
