from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _
from movies.models import Movie


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(
        _('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    biography = models.TextField(blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    facebook = models.URLField(max_length=255, blank=True, null=True)
    instagram = models.URLField(max_length=255, blank=True, null=True)
    youtube = models.URLField(max_length=255, blank=True, null=True)
    twitter = models.URLField(max_length=255, blank=True, null=True)
    medium = models.URLField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(
        upload_to='users/%Y/%m/%d', null=True, blank=True)
    role = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    # Movie Stats
    movies_watched_count = models.IntegerField(default=0)
    movies_watchlist_count = models.IntegerField(default=0)
    movies_like_count = models.IntegerField(default=0)
    movies_score_count = models.IntegerField(default=0)
    movies_average_score = models.IntegerField(default=0)
    # Member List
    following = models.ManyToManyField(
        'self', blank=True, symmetrical=False, related_name="user_following")
    followers = models.ManyToManyField(
        'self', blank=True, symmetrical=False, related_name="user_followers")

    def __str__(self):
        return self.email


class MovieLog(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='movielog_user')       
    watched = models.BooleanField(default=False)    
    like = models.BooleanField(default=False)    
    watchlist = models.BooleanField(default=False)        
    score = models.IntegerField(default=0)
    watched_at = models.DateField(blank=True, null=True)    
    comment = models.TextField(blank=True, null=True)
    spoiler_alert = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username + ": " + self.movie.title