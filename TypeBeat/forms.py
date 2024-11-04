# forms.py
from django import forms
from .models import User, Music, BeatPack, Beatmap, Highscore

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio']

class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['title', 'author', 'genre', 'release_date']

class BeatPackForm(forms.ModelForm):
    class Meta:
        model = BeatPack
        fields = ['title', 'description', 'music']

class BeatmapForm(forms.ModelForm):
    class Meta:
        model = Beatmap
        fields = ['title', 'difficulty', 'max_score', 'user', 'beatpack']

class HighscoreForm(forms.ModelForm):
    class Meta:
        model = Highscore
        fields = ['beatmap', 'user', 'score', 'accuracy', 'date_finished']
        widgets = {
            'date_finished': forms.DateInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }),
        }
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)