from datetime import datetime
import random
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import SignupForm, LoginForm, BeatpackUploadForm, UserForm, BeatPackForm, BeatmapForm, HighscoreForm
from .models import User, Beatpack, Beatmap, Highscore
from django.db.models import Q
from .utils import parse_beatpack_details
from django.shortcuts import render
from django.core.files.base import ContentFile
from django.db import transaction


color_classes = ['orange', 'red', 'pink', 'blue']

def home(request):
    return HttpResponse("Hello, Django!")

def homepage(request, name):
    beatpacks = Beatpack.objects.all()  # Query all beatpacks
    top_highscores = Highscore.objects.order_by('-total_score')[:10]  # Query top 10 users by highscore

    # Assign a random color class to each beatpack
    for beatpack in beatpacks:
        beatpack.color_class = random.choice(color_classes)

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

def upload_beatpack(request, name):
    user = request.user
    print(f"Current user: {user}")  # Debug message

    user_beatpacks = Beatpack.objects.filter(beatmap__mapmaker=user).distinct()
    print(f"User's existing Beatpacks: {list(user_beatpacks)}")  # Debug message

    if request.method == "POST":
        form = BeatpackUploadForm(request.POST, request.FILES)
        if form.is_valid():
            details_file = form.cleaned_data["details_file"]
            beatpack_image = form.cleaned_data["beatpack_image"]
            print(f"Received details file: {details_file.name}")  # Debug message
            print(f"Received image file: {beatpack_image.name}")  # Debug message

            try:
                # Parse the .txt file using util function
                beatpack_data, beatmaps_data = parse_beatpack_details(details_file)
                print(f"Parsed Beatpack data: {beatpack_data}")  # Debug message
                print(f"Parsed Beatmaps data: {beatmaps_data}")  # Debug message

                # Begin a transaction to handle Beatpack and Beatmap creation
                with transaction.atomic():
                    # Create and save the Beatpack
                    beatpack = Beatpack(
                        beatpack_title=beatpack_data["beatpack_title"],
                        music_author=beatpack_data["music_author"],
                        no_of_beatmaps=len(beatmaps_data),
                        no_of_downloads=0,
                    )
                    beatpack.beatpack_picture.save(beatpack_image.name, ContentFile(beatpack_image.read()))
                    beatpack.save()
                    print(f"Created Beatpack with attributes: {beatpack.__dict__}")  # Debugging attributes

                    # Create and save Beatmaps
                    for beatmap_data in beatmaps_data:
                        contributor_username = beatmap_data.get("contributor", None)
                        if contributor_username:
                            try:
                                # Find contributor by username
                                contributor = User.objects.get(username=contributor_username)
                                mapmaker = contributor
                            except User.DoesNotExist:
                                print(f"Contributor '{contributor_username}' not found. Defaulting to uploader.")
                                mapmaker = user  # Default to uploader if contributor not found
                        else:
                            mapmaker = user  # Default to uploader if no contributor

                        beatmap = Beatmap.objects.create(
                            mapmaker=mapmaker,
                            beatpack=beatpack,
                            beatmap_title=beatmap_data["beatmap_title"],
                            difficulty=int(beatmap_data.get("difficulty", 0)),
                            no_of_letters=int(beatmap_data.get("no_of_letters", 0)),
                            no_of_spaces=int(beatmap_data.get("no of spaces", 0)),
                            total_note_count=int(beatmap_data.get("no_of_letters", 0)) +
                            int(beatmap_data.get("no of spaces", 0)),
                        )
                        print(f"Created Beatmap with attributes: {beatmap.__dict__}")  # Debugging attributes

                # Print success message to the console
                print(f"SUCCESS: Beatpack '{beatpack.beatpack_title}' uploaded by user '{user.username}' with ID {beatpack.beatpack_id}")

                # Add a success message for the user
                messages.success(request, f"Successfully uploaded Beatpack: {beatpack.beatpack_title}")
                return redirect('BeatPack_Upload/BeatPack_Upload.html', name=name)

            except Exception as e:
                print(f"Error during Beatpack processing: {str(e)}")  # Debug message
                messages.error(request, f"Error: {str(e)}")
        else:
            print(f"Form errors: {form.errors}")  # Debug message
            messages.error(request, "Invalid file upload.")

    else:
        form = BeatpackUploadForm()
        print("Rendering the upload form.")  # Debug message

    return render(request, "BeatPack_Upload/BeatPack_Upload.html", {
        "form": form,
        "name": name,
        "user_beatpacks": user_beatpacks,
    })

def my_beatmap(request, name, title):
    beatpack = get_object_or_404(Beatpack, beatpack_title=title)
    beatmaps = Beatmap.objects.filter(beatpack=beatpack)

    if request.method == 'POST':
        beatmap_id = request.POST.get('beatmap_id')
        beatmap = get_object_or_404(Beatmap, pk=beatmap_id)
        if 'delete' in request.POST:
            beatmap.delete()
        else:
            beatmap.beatmap_title = request.POST.get('beatmap_title')
            beatmap.no_of_letters = request.POST.get('no_of_letters')
            beatmap.no_of_spaces = request.POST.get('no_of_spaces')
            beatmap.difficulty = request.POST.get('difficulty')
            beatmap.save()

    return render(request, 'beatpack_beatmaps/beatpack_beatmaps.html', {'beatpack': beatpack, 'beatmaps': beatmaps})


def logout_view(request):
    logout(request)
    return redirect('login')

def beatpack_detail(request, beatpack_id):
    beatpack = get_object_or_404(Beatpack, pk=beatpack_id)
    beatmaps = Beatmap.objects.filter(beatpack_id=beatpack_id)
    return render(request, 'beatpack_detail/beatpack_detail.html', {'beatpack': beatpack, 'beatmaps': beatmaps})

def beatmap_leaderboard(request, beatmap_id):
    beatmap = get_object_or_404(Beatmap, pk=beatmap_id)
    highscores = Highscore.objects.filter(beatmap_id=beatmap_id).order_by('-total_score')
    context = {
        'beatmap': beatmap,
        'beatpack': beatmap.beatpack,
        'mapmaker': beatmap.mapmaker,
        'user': request.user,
        'highscores': highscores,
    }
    return render(request, 'beatmap_leaderboard/beatmap_leaderboard.html', context)

def play(request, beatmap_id):
    if request.method == 'POST':
        user = request.user
        beatmap = get_object_or_404(Beatmap, pk=beatmap_id)
        beatpack = beatmap.beatpack
        mapmaker = beatmap.mapmaker

        highscore = Highscore.objects.filter(user=user, beatmap=beatmap).first()
        if highscore:
            old_total_score = highscore.total_score
            print(f"Old highscore data: {highscore.__dict__}")
            highscore_form = HighscoreForm(request.POST, instance=highscore)
        else:
            old_total_score = None
            highscore_form = HighscoreForm(request.POST)

        if highscore_form.is_valid():
            new_highscore = highscore_form.save(commit=False)
            print(f"New highscore data: {new_highscore.__dict__}")
            print(f"New highscore total score: {new_highscore.total_score}")
            print(f"Old highscore total score: {old_total_score}")

            if old_total_score is None or new_highscore.total_score > old_total_score:
                new_highscore.user = user
                new_highscore.beatmap = beatmap
                new_highscore.beatpack = beatpack
                new_highscore.mapmaker = mapmaker
                try:
                    new_highscore.save()
                    messages.success(request, 'High score submitted successfully!')
                except IntegrityError:
                    highscore_form.add_error(None, 'A highscore for this user and beatmap already exists.')
            else:
                messages.error(request, 'New score is lower than or equal to the current high score.')

    return redirect('beatmap_leaderboard', beatmap_id=beatmap_id)

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

@login_required
def user_page(request):
    return render(request, 'user_page/user_page.html', {'user': request.user})


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')

        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            user.profile_picture = profile_picture

        password = request.POST.get('password')
        if password:
            user.set_password(password)

        user.save()
        messages.success(request, 'User details updated successfully.')
        return redirect('login')
    return render(request, 'edit_user/edit_user.html', {'user': user})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('login')
    return render(request, 'delete_user/delete_user.html', {'user': user})

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