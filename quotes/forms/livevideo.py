from django import forms
from quotes.models import LiveVideo

class LiveVideoForm(forms.ModelForm):
    class Meta:
        model = LiveVideo
        fields = ['video_type', 'num_seconds', 'description']
        widgets = {
            'video_type': forms.Select(attrs={'class': 'form-control'}),
            'num_seconds': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
