from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)  # Use set_password to hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)  # Primary Key
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


# Music model
class Music(models.Model):
    music_id = models.AutoField(primary_key=True)  # Primary Key
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    def __str__(self): 
        return f'{self.title} by {self.author}' #e edit ni depende sa imo ganahan na format sa data achilles ig recieve.


# BeatPack model
class BeatPack(models.Model):
    beatpack_id = models.AutoField(primary_key=True)  # Primary Key
    title = models.CharField(max_length=255)
    music = models.ForeignKey(Music, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title #e edit ni depende sa imo ganahan na format sa data achilles ig recieve.


# Beatmap model
class Beatmap(models.Model):
    beatmap_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    beatpack = models.ForeignKey(BeatPack, on_delete=models.CASCADE)  

    def __str__(self):
        return f'{self.title} - {self.difficulty}' #e edit ni depende sa imo ganahan na format sa data achilles ig recieve.


# Highscore model needs fixing higher score does not override current
class Highscore(models.Model):
    beatmap = models.ForeignKey(Beatmap, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    score = models.IntegerField()
    date_finished = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['beatmap', 'user'], name='unique_user_beatmap')
        ]

    def __str__(self): 
        return f'{self.user.username} - {self.score} on {self.beatmap.title}'  #e edit ni depende sa imo ganahan na format sa data achilles ig recieve.
