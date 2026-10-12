from django.contrib import admin

from .models import Child, Household


@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ('household_code', 'head_name', 'sector', 'registered_on')
    search_fields = ('household_code', 'head_name')
    list_filter = ('sector', 'food_security', 'income_category')


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'household', 'sex', 'age_in_months')
    search_fields = ('full_name', 'household__household_code')
    list_filter = ('sex', 'household__sector')
