from django.db import models
from django.db import transaction
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
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=60, unique=True)
    password = models.CharField(max_length=30)  
    profile_picture = models.ImageField(
    upload_to='Profile/',
    default='Profile/DefaultProfile.png',  
    null=True,
    blank=True
)

    is_staff = models.BooleanField(default=False)  

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Beatpack(models.Model):
    beatpack_id = models.AutoField(primary_key=True)
    beatpack_title = models.CharField(max_length=30)
    music_author = models.CharField(max_length=30)
    no_of_beatmaps = models.IntegerField()
    no_of_downloads = models.IntegerField()
    beatpack_picture = models.ImageField(upload_to='beatpack_pictures/', null=True, blank=True)

    def __str__(self):
        return self.beatpack_title


class Beatmap(models.Model):
    beatmap_id = models.AutoField(primary_key=True)
    mapmaker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_beatmaps")
    beatpack = models.ForeignKey(Beatpack, on_delete=models.CASCADE)
    beatmap_title = models.CharField(max_length=30)
    difficulty = models.PositiveSmallIntegerField()
    total_note_count = models.IntegerField()
    no_of_letters = models.IntegerField(null=True, blank=True)
    no_of_spaces = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.beatmap_title} - {self.difficulty}'


class Highscore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="highscores")
    beatmap = models.ForeignKey(Beatmap, on_delete=models.CASCADE)
    mapmaker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mapmaker_highscores")
    beatpack = models.ForeignKey(Beatpack, on_delete=models.CASCADE)
    total_score = models.IntegerField()
    highest_combo = models.IntegerField()
    accuracy = models.FloatField()
    perfect = models.IntegerField(null=True, blank=True)
    great = models.IntegerField(null=True, blank=True)
    good = models.IntegerField(null=True, blank=True)
    miss = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['beatmap', 'user'], name='unique_user_beatmap')
        ]

    def __str__(self):
        return f'{self.user.username} - {self.total_score} on {self.beatmap.beatmap_title}'
