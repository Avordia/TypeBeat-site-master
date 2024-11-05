# TypeBeat/forms.py
from django import forms
from .models import User, Beatpack, Beatmap, Highscore

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
        
class BeatpackForm(forms.ModelForm):
    class Meta:
        model = Beatpack
        fields = ['beatpack_title', 'music_author', 'no_of_beatmaps', 'no_of_downloads', 'beatpack_picture']

class BeatmapForm(forms.ModelForm):
    class Meta:
        model = Beatmap
        fields = ['beatmap_title', 'difficulty', 'mapmaker', 'beatpack', 'total_note_count', 'no_of_letters', 'no_of_spaces']

class HighscoreForm(forms.ModelForm):
    class Meta:
        model = Highscore
        fields = ['beatmap', 'user', 'mapmaker', 'beatpack', 'total_score', 'highest_combo', 'accuracy', 'perfect', 'great', 'good', 'miss']
        widgets = {
            'date_finished': forms.DateInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }),
        }
