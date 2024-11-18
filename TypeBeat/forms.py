# TypeBeat/forms.py
from django import forms
from .models import User, Beatpack, Beatmap, Highscore


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile_picture']  # Removed 'bio'

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile_picture']  # Removed 'bio'

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user



class BeatPackForm(forms.ModelForm):
    class Meta:
        model = Beatpack
        fields = [
            'beatpack_title',
            'music_author',
            'no_of_beatmaps',
            'no_of_downloads',
            'beatpack_picture'
        ]
class UploadForm(forms.ModelForm):
    class Meta:
        model = Beatpack
        fields = [
            'beatpack_title',
            'music_author',
            'no_of_beatmaps',
            'beatpack_picture'
        ]


class BeatmapForm(forms.ModelForm):
    class Meta:
        model = Beatmap
        fields = [
            'beatmap_title',
            'difficulty',
            'total_note_count',
            'no_of_letters',
            'no_of_spaces',
            'mapmaker',
            'beatpack'
        ]  # Updated fields


class HighscoreForm(forms.ModelForm):
    class Meta:
        model = Highscore
        fields = [
            'user',
            'beatmap',
            'mapmaker',
            'beatpack',
            'total_score',
            'highest_combo',
            'accuracy',
            'perfect',
            'great',
            'good',
            'miss'
        ]