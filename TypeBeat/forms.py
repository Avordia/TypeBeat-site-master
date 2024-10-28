from django import forms
from .models import User, Music, BeatPack, Beatmap, Highscore

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['title', 'author']

class BeatPackForm(forms.ModelForm):
    class Meta:
        model = BeatPack
        fields = ['title', 'music']

class BeatmapForm(forms.ModelForm):
    class Meta:
        model = Beatmap
        fields = ['title', 'difficulty', 'user', 'beatpack']

class HighscoreForm(forms.ModelForm):
    class Meta:
        model = Highscore
        fields = ['beatmap', 'user', 'score', 'date_finished']
        widgets = {
            'date_finished': forms.DateInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',   
            }),
        }