from django import forms
from quotes.models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['complexity', 'description', 'num_languages']
        widgets = {
            'complexity': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'num_languages': forms.NumberInput(attrs={'class': 'form-control'}),
        }
