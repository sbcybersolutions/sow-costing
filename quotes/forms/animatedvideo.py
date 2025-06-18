from django import forms
from quotes.models import AnimatedVideo

class AnimatedVideoForm(forms.ModelForm):
    class Meta:
        model = AnimatedVideo
        fields = ['video_type', 'num_seconds', 'description']
        widgets = {
            'video_type': forms.Select(attrs={'class': 'form-control'}),
            'num_seconds': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
