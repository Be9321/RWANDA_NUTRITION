from django import forms
from .models import Child, Household


class BootstrapFormMixin:
    """Adds the Bootstrap 'form-control' class to every field."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class ChildForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Child
        fields = ['household', 'full_name', 'sex', 'date_of_birth', 'birth_weight_kg']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def clean_full_name(self):
        name = self.cleaned_data['full_name'].strip()
        if len(name) < 3:
            raise forms.ValidationError('Please enter the full name (at least 3 letters).')
        return name


class HouseholdForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Household
        fields = ['household_code', 'head_name', 'sector', 'village', 'mother_education',
                  'food_security', 'sanitation', 'water_source', 'income_category']

    def clean_household_code(self):
        code = self.cleaned_data['household_code'].strip().upper()
        if not code.startswith('HH-'):
            raise forms.ValidationError('The household code must start with HH- (for example HH-0100).')
        return code