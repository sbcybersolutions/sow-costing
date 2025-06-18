from django import forms
from quotes.models import Talent, TalentRate, LiveVideo

class TalentForm(forms.ModelForm):
    name = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    live_video = forms.ModelChoiceField(queryset=LiveVideo.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Talent
        fields = ['name', 'live_video']

    def __init__(self, *args, **kwargs):
        quote = kwargs.pop('quote', None)
        super().__init__(*args, **kwargs)

        self.fields['name'].choices = [(tr.name, tr.name) for tr in TalentRate.objects.all()]

        if quote:
            self.fields['live_video'].queryset = quote.live_videos.all() # type: ignore
