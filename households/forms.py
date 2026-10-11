from django import forms
from .models import Child


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['household', 'full_name', 'sex', 'date_of_birth', 'birth_weight_kg']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean_full_name(self):
        name = self.cleaned_data['full_name'].strip()
        if len(name) < 3:
            raise forms.ValidationError('Please enter the full name (at least 3 letters).')
        return name