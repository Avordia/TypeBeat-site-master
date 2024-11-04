# views.py
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from datetime import datetime
from .forms import UserForm, MusicForm, BeatPackForm, BeatmapForm, HighscoreForm, SignupForm, LoginForm
from django.contrib import messages
from .models import User

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Signup successful! You can now log in.')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'SignUp/SignUp.html', {'form': form})

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

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"Username: {username}, Password: {password}")  # Debugging
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage', name=username)  # Redirect to homepage with username
            else:
                print("Authentication failed")  # Debugging
                messages.error(request, 'Invalid username or password.')
        else:
            print("Form is invalid")  # Debugging
    else:
        form = LoginForm()
    return render(request, 'Login/Login.html', {'form': form})

def test(request):
    user_form = UserForm()
    music_form = MusicForm()
    beatpack_form = BeatPackForm()
    beatmap_form = BeatmapForm()
    highscore_form = HighscoreForm()

    if request.method == 'POST':
        if 'user_submit' in request.POST:
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                user_form.save()
                return redirect('test')  

        elif 'music_submit' in request.POST:
            music_form = MusicForm(request.POST)
            if music_form.is_valid():
                music_form.save()
                return redirect('test')  

        elif 'beatpack_submit' in request.POST:
            beatpack_form = BeatPackForm(request.POST)
            if beatpack_form.is_valid():
                beatpack_form.save()
                return redirect('test') 

        elif 'beatmap_submit' in request.POST:
            beatmap_form = BeatmapForm(request.POST)
            if beatmap_form.is_valid():
                beatmap_form.save()
                return redirect('test')  

        elif 'highscore_submit' in request.POST:
            highscore_form = HighscoreForm(request.POST)
            if highscore_form.is_valid():
                highscore_form.save()
                return redirect('test')  

    context = {
        'user_form': user_form,
        'music_form': music_form,
        'beatpack_form': beatpack_form,
        'beatmap_form': beatmap_form,
        'highscore_form': highscore_form,
    }

    return render(request, 'test/test.html', context)
