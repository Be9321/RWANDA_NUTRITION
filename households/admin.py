from django.contrib import admin

from .models import Child, Household


class ChildInline(admin.TabularInline):
    model = Child
    extra = 0
    fields = ('full_name', 'sex', 'date_of_birth', 'birth_weight_kg')


@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = (
        'household_code',
        'head_name',
        'sector',
        'village',
        'food_security',
        'registered_on',
    )
    list_filter = ('food_security', 'sanitation', 'water_source', 'income_category')
    search_fields = ('household_code', 'head_name', 'village')
    inlines = (ChildInline,)


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'household', 'sex', 'date_of_birth', 'age_in_months')
    list_filter = ('sex',)
    search_fields = ('full_name', 'household__household_code', 'household__head_name')
    autocomplete_fields = ('household',)

