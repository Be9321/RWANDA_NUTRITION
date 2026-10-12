from django import forms

from .models import GrowthMeasurement, Program, Referral


class GrowthMeasurementForm(forms.ModelForm):
    class Meta:
        model = GrowthMeasurement
        fields = ['child', 'measured_by', 'measurement_date', 'weight_kg', 'height_cm', 'muac_cm',
                  'height_for_age_z', 'notes']
        widgets = {
            'measurement_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'description', 'start_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 3:
            raise forms.ValidationError('Program name must be at least 3 characters long.')
        return name


class ReferralForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = ['child', 'facility', 'referred_by', 'referral_date', 'reason', 'status']
        widgets = {
            'referral_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean_reason(self):
        reason = self.cleaned_data['reason'].strip()
        if len(reason) < 5:
            raise forms.ValidationError('Referral reason must be at least 5 characters long.')
        return reason
