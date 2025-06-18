from django import forms
from quotes.models import Studio

class StudioForm(forms.ModelForm):
    class Meta:
        model = Studio
        fields = ['studio_name', 'filming_days']
        widgets = {
            'studio_name': forms.Select(attrs={'class': 'form-control'}),
            'filming_days': forms.NumberInput(attrs={'class': 'form-control'}),
        }
