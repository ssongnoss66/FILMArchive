from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

# Create your models here.
class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='user_followers')
    image = ProcessedImageField(
        null=True,
        blank=True,
        processors=[Thumbnail(200,200)],
        format= 'JPEG',
        options= {'quality':90},
        upload_to = '',
    )