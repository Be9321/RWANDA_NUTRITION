from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from .models import GrowthMeasurement, Program, Enrollment, Referral


class BootstrapMixin:
    """Adds the Bootstrap 'form-control' class to every field."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class MeasurementForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = GrowthMeasurement
        fields = ['child', 'measurement_date', 'weight_kg', 'height_cm',
                  'muac_cm', 'height_for_age_z', 'notes']
        widgets = {
            'measurement_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_height_for_age_z(self):
        z = self.cleaned_data.get('height_for_age_z')
        if z is not None and not (-6 <= z <= 6):
            raise ValidationError('A height-for-age z-score must be between -6 and 6.')
        return z

    def clean(self):
        cleaned = super().clean()
        child = cleaned.get('child')
        date_measured = cleaned.get('measurement_date')
        if child and date_measured and date_measured < child.date_of_birth:
            raise ValidationError("The measurement date cannot be before the child's birth date.")
        return cleaned


class ProgramForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'description', 'start_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 3:
            raise ValidationError('The program name must have at least 3 letters.')
        return name


class EnrollmentForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['child', 'enrolled_on']
        widgets = {
            'enrolled_on': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, program=None, **kwargs):
        self.program = program
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        child = cleaned.get('child')
        enrolled_on = cleaned.get('enrolled_on')
        if enrolled_on and enrolled_on > date.today():
            raise ValidationError('The enrolment date cannot be in the future.')
        if enrolled_on and self.program and enrolled_on < self.program.start_date:
            raise ValidationError('The enrolment date cannot be before the program start date.')
        if child and self.program and Enrollment.objects.filter(child=child, program=self.program).exists():
            raise ValidationError('This child is already enrolled in this program.')
        return cleaned


class ReferralForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Referral
        fields = ['child', 'facility', 'referral_date', 'reason', 'status']
        widgets = {
            'referral_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def clean_referral_date(self):
        d = self.cleaned_data['referral_date']
        if d > date.today():
            raise ValidationError('The referral date cannot be in the future.')
        return d

    def clean_reason(self):
        reason = self.cleaned_data['reason'].strip()
        if len(reason) < 5:
            raise ValidationError('Please give a short reason (at least 5 characters).')
        return reason