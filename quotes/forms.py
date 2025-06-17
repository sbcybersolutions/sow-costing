from django import forms
from quotes.models import (
    Course, LiveVideo, AnimatedVideo, Studio,
    Talent, TechnicalStaff, TalentRate
)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['complexity', 'description', 'num_languages']
        widgets = {
            'complexity': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'num_languages': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class LiveVideoForm(forms.ModelForm):
    class Meta:
        model = LiveVideo
        fields = ['video_type', 'num_seconds', 'description']
        widgets = {
            'video_type': forms.Select(attrs={'class': 'form-control'}),
            'num_seconds': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TalentForm(forms.ModelForm):
    name = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    live_video = forms.ModelChoiceField(
        queryset=LiveVideo.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Talent
        fields = ['name', 'live_video']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ Populate dropdown choices from TalentRate in DB
        self.fields['name'].choices = [
            (tr.name, tr.name) for tr in TalentRate.objects.all()
        ]

class AnimatedVideoForm(forms.ModelForm):
    class Meta:
        model = AnimatedVideo
        fields = ['video_type', 'num_seconds', 'description']
        widgets = {
            'video_type': forms.Select(attrs={'class': 'form-control'}),
            'num_seconds': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

class StudioForm(forms.ModelForm):
    class Meta:
        model = Studio
        fields = ['studio_name', 'filming_days']
        widgets = {
            'studio_name': forms.Select(attrs={'class': 'form-control'}),
            'filming_days': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TechnicalStaffForm(forms.ModelForm):
    class Meta:
        model = TechnicalStaff
        fields = ['filming_days', 'editing_days']
        widgets = {
            'filming_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'editing_days': forms.NumberInput(attrs={'class': 'form-control'}),
        }
