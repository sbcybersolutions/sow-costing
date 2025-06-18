from django import forms
from quotes.models import TechnicalStaff

class TechnicalStaffForm(forms.ModelForm):
    class Meta:
        model = TechnicalStaff
        fields = ['filming_days', 'editing_days']
        widgets = {
            'filming_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'editing_days': forms.NumberInput(attrs={'class': 'form-control'}),
        }
