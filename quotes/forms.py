from django import forms
from .models import Course, LiveVideo, AnimatedVideo, Studio, Talent, TechnicalStaff

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
    class Meta:
        model = Talent
        fields = ['name', 'live_video']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'live_video': forms.Select(attrs={'class': 'form-control'}),
        }

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
