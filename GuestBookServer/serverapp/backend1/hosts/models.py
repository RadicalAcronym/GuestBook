# Copyright Mark B. Skouson, 2019
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from datetime import date


class CustomUserManager(BaseUserManager):
    """
    This is a custom user manager for when email is the unique identifier
    for authentication
    """
    def create_user(self, email, password, **other_fields):
        """
        Create a user with a given name and password
        inputs: 
            email address
            Password
            other fields: Other fields you want to pass
        """
        if not email:
            raise ValueError(_('First argument must be a valid email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **other_fields):
        """
        Create a superuser with the given email and password
        inputs: 
            email address
            Password
            other fields: Other fields you want to pass
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError(_('For superuser, is_staff must be True'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('For superuser, is_superuser must be True'))

        return self.create_user(email, password, **other_fields)
           

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # other than email and password
    objects = CustomUserManager()
    def __str__(self):
        return self.email


class Event(models.Model):
    # Relations
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             default=None)
    # Attributes
    event_title = models.CharField(
        'Event Title',
        max_length=250,
    )
    event_date = models.DateField('Event Date')
    event_time = models.TimeField('Event Time', default='12:00')
    unique_code = models.CharField(
        'Unique Code',
        max_length=250,
        default='1aPwklekr',
    )
    num_vid_clips = models.IntegerField(
        'Number of video clips',
        default=0,
    )
    max_num_vid_clips = models.IntegerField(
        'Max number of video clips',
        default=100,
    )

    class Meta:
        ordering = ['event_date', 'event_time']

    def __str__(self):
        return self.event_title


class Video(models.Model):
    # Relations
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                             default=None)
    # Attributes
    video_title = models.CharField(
        'Event Title',
        max_length=250,
        default='vid.mp4',
    )
    guest_name = models.CharField(
        'Guest Name',
        max_length=250,
        default='anonymous'
    )
    thumbnailfpname = models.CharField(
        'Thumbnail Filename',
        max_length=5000,
        default='unknown'
    )
    processedfpname = models.CharField(
        'Video Filename',
        max_length=5000,
        default='unknown'
    )
    minifpname = models.CharField(
        'Mini Video Filename',
        max_length=5000,
        default='unknown'
    )
    upload_date = models.DateField('Upload Date', default='20200101')
    upload_time = models.TimeField('Upload Time', default='12:00')

    class Meta:
        ordering = ['upload_date', 'upload_time']

    def __str__(self):
        return self.video_title
