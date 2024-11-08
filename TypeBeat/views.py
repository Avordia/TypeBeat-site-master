from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from datetime import datetime
from .forms import BeatPackForm, SignupForm, LoginForm
from django.contrib import messages
from .models import User, Beatpack, Beatmap, Highscore
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def home(request):
    return HttpResponse("Hello, Django!")

def homepage(request, name):
    print(request.build_absolute_uri())
    return render(
        request,
        'Homepage/homepage.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            # Check if the username already exists
            if User.objects.filter(username=user.username).exists():
                form.add_error('username', 'Username already exists. Please choose a different one.')
            else:
                try:
                    user.save()
                    messages.success(request, 'Signup successful! You can now log in.')
                    return redirect('login')
                except IntegrityError:
                    form.add_error(None, 'An error occurred while saving. Please try again.')
    else:
        form = SignupForm()

    return render(request, 'SignUp/SignUp.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"Username: {username}, Password: {password}")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage', name=user.username)  # Redirects to homepage with the username
            else:
                print("Authentication failed")
                messages.error(request, 'Invalid username or password.')
        else:
            print("Form is invalid")
    else:
        form = LoginForm()
    return render(request, 'Login/Login.html', {'form': form})

from django.shortcuts import render, redirect
from django.db import IntegrityError
from .forms import UserForm, BeatPackForm, BeatmapForm, HighscoreForm
from .models import User, Beatpack, Beatmap, Highscore

def AdminPage(request):
    # Initialize forms
    user_form = UserForm()
    beatpack_form = BeatPackForm()
    beatmap_form = BeatmapForm()
    highscore_form = HighscoreForm()

    if request.method == 'POST':
        if 'user_submit' in request.POST:
            # Handle user form submission with file handling
            user_form = UserForm(request.POST, request.FILES)
            if user_form.is_valid():
                try:
                    user_form.save()
                except IntegrityError:
                    user_form.add_error(None, 'A user with this username or email already exists.')

        elif 'beatpack_submit' in request.POST:
            # Handle beatpack form submission with file handling
            beatpack_form = BeatPackForm(request.POST, request.FILES)
            if beatpack_form.is_valid():
                try:
                    beatpack_form.save()
                except IntegrityError:
                    beatpack_form.add_error(None, 'A beatpack with this title already exists.')

        elif 'beatmap_submit' in request.POST:
            # Handle beatmap form submission
            beatmap_form = BeatmapForm(request.POST)
            if beatmap_form.is_valid():
                try:
                    beatmap_form.save()
                except IntegrityError:
                    beatmap_form.add_error(None, 'A beatmap with this title already exists.')

        elif 'highscore_submit' in request.POST:
            # Handle highscore form submission
            highscore_form = HighscoreForm(request.POST)
            if highscore_form.is_valid():
                try:
                    highscore_form.save()
                except IntegrityError:
                    highscore_form.add_error(None, 'A highscore for this user and beatmap already exists.')

    # Query all entries to display in the template
    users = User.objects.all()
    beatpacks = Beatpack.objects.all()
    beatmaps = Beatmap.objects.all()
    highscores = Highscore.objects.all()

    # Prepare context
    context = {
        'user_form': user_form,
        'beatpack_form': beatpack_form,
        'beatmap_form': beatmap_form,
        'highscore_form': highscore_form,
        'users': users,
        'beatpacks': beatpacks,
        'beatmaps': beatmaps,
        'highscores': highscores,
    }

    return render(request, 'AdminPage/AdminPage.html', context)
def update_field(request, model_name, obj_id):
    if request.method == 'POST':
        field_name = request.POST.get('field_name')
        value = request.POST.get('value')

        model_mapping = {
            'user': User,
            'beatpack': Beatpack,
            'beatmap': Beatmap,
            'highscore': Highscore,
        }

        Model = model_mapping.get(model_name.lower())
        if Model:
            obj = get_object_or_404(Model, pk=obj_id)
            setattr(obj, field_name, value)  # Update the field dynamically
            obj.save()
            return JsonResponse({'status': 'success', 'value': value})
    return JsonResponse({'status': 'error'})


# View to delete an item
def delete_item(request, model_name, obj_id):
    model_mapping = {
        'user': User,
        'beatpack': Beatpack,
        'beatmap': Beatmap,
        'highscore': Highscore,
    }

    Model = model_mapping.get(model_name.lower())
    if Model:
        obj = get_object_or_404(Model, pk=obj_id)
        obj.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})