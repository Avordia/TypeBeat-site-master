from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from .forms import SignupForm, LoginForm,UploadForm
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def home(request):
    return HttpResponse("Hello, Django!")

def homepage(request, name):
    beatpacks = Beatpack.objects.all()  # Query all beatpacks
    top_highscores = Highscore.objects.order_by('-total_score')[:10]  # Query top 10 users by highscore

    return render(
        request,
        'Homepage/homepage.html',
        {
            'name': name,
            'date': datetime.now(),
            'beatpacks': beatpacks,
            'top_highscores': top_highscores,
        }
    )

def BeatPack_Upload(request, name):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage', name=request.user.username)
    else:
        form = UploadForm()

    return render(request, 'BeatPack_Upload/BeatPack_Upload.html', {'UploadForm': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def beatpack_detail(request, beatpack_id):
    beatpack = get_object_or_404(Beatpack, pk=beatpack_id)
    beatmaps = Beatmap.objects.filter(beatpack_id=beatpack_id)
    return render(request, 'beatpack_detail/beatpack_detail.html', {'beatpack': beatpack, 'beatmaps': beatmaps})

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
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:  # Check if the user is an admin
                    return redirect('AdminPage')  # Redirect to the custom admin page
                else:
                    return redirect('homepage', name=user.username)  # Redirect to the homepage with the username
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'Login/Login.html', {'form': form})

from django.shortcuts import render, redirect
from django.db import IntegrityError
from .forms import UserForm, BeatPackForm, BeatmapForm, HighscoreForm
from .models import User, Beatpack, Beatmap, Highscore
@staff_member_required
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
            beatpack_form = BeatPackForm(request.POST, request.FILES)
            if beatpack_form.is_valid():
                try:
                    beatpack_form.save()
                except IntegrityError:
                    beatpack_form.add_error(None, 'A beatpack with this title already exists.')

        elif 'beatmap_submit' in request.POST:
            beatmap_form = BeatmapForm(request.POST)
            if beatmap_form.is_valid():
                try:
                    beatmap_form.save()
                except IntegrityError:
                    beatmap_form.add_error(None, 'A beatmap with this title already exists.')

        elif 'highscore_submit' in request.POST:
            user = request.POST.get('user')
            beatmap = request.POST.get('beatmap')

            highscore = Highscore.objects.filter(user_id=user, beatmap_id=beatmap).first()
            if not highscore:
                highscore_form = HighscoreForm(request.POST)
            else:
                highscore_form = HighscoreForm(request.POST, instance=highscore)

            if highscore_form.is_valid():
                try:
                    highscore_form.save()
                except IntegrityError:
                    highscore_form.add_error(None, 'A highscore for this user and beatmap already exists.')

    users = User.objects.all()
    beatpacks = Beatpack.objects.all()
    beatmaps = Beatmap.objects.all()
    highscores = Highscore.objects.all()

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
    if request.method == 'POST':
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