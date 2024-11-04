# models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)  # New field for user bio
    join_date = models.DateTimeField(auto_now_add=True)  # New field for join date
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Music(models.Model):
    music_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100, blank=True, null=True)  # New genre field
    release_date = models.DateField(blank=True, null=True)  # New release date field

    def __str__(self):
        return f'{self.title} by {self.author}'

class BeatPack(models.Model):
    beatpack_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # New field for description
    music = models.ForeignKey(Music, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Beatmap(models.Model):
    beatmap_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=100)
    max_score = models.IntegerField(default=100)  # New field for max score
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beatpack = models.ForeignKey(BeatPack, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.difficulty}'

class Highscore(models.Model):
    beatmap = models.ForeignKey(Beatmap, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # New accuracy field
    date_finished = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['beatmap', 'user'], name='unique_user_beatmap')
        ]

    def __str__(self):
        return f'{self.user.username} - {self.score} on {self.beatmap.title}'
