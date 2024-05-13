from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail

# Create your models here.
genre_CHOICES = [
    (28, "Action"),
    (12, "Adventure"),
    (16, "Animation"),
    (35, "Comedy"),
    (80, "Crime"),
    (99, "Documentary"),
    (18, "Drama"),
    (10751, "Family"),
    (14, "Fantasy"),
    (36, "History"),
    (27, "Horror"),
    (10402, "Music"),
    (9648, "Mystery"),
    (10749, "Romance"),
    (878, "Science Fiction"),
    (10770, "TV Movie"),
    (53, "Thriller"),
    (10752, "War"),
    (37, "Western"),
]

country_CHOICES = [
    ("프랑스", "프랑스"),
    ("영국", "영국"),
    ("홍콩", "홍콩"),
    ("일본", "일본"),
    ("한국", "한국"),
    ("미국", "미국"),
    ("기타", "기타")
]

class Movie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.title
    original_title = models.CharField(max_length=50, null=True, blank=True)
    rate = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    def image_path(instance, filename):
        return f'movies/{instance.title}/{filename}'
    poster = models.ImageField(upload_to=image_path)
    poster_thumbnail = ImageSpecField(source='poster',
                                      processors=[Thumbnail(200, 260)],
                                      format='JPEG',
                                      options={'quality': 100})
    release_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=50, null=True, blank=True, choices=genre_CHOICES)
    country = models.CharField(max_length=50, null=True, blank=True, choices=country_CHOICES)
    running_time = models.CharField(max_length=50, null=True, blank=True)
    age = models.CharField(max_length=50, null=True, blank=True)
    wish_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='wish_movies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MoviePhoto(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    def image_path(instance, filename):
        return f'movies/{filename}'
    image_movie = models.ImageField(upload_to=image_path, null=True, blank=True)
    image_movie_thumbnail = ImageSpecField(source='image_movie',
                                      processors=[Thumbnail(300, 200)],
                                      format='JPEG',
                                      options={'quality': 100})
    
class MoviePeople(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=50, null=True, blank=True)
    part = models.CharField(max_length=50, null=True, blank=True)
    character_name = models.CharField(max_length=50, null=True, blank=True)
    def image_path(instance, filename):
        return f'movies/{instance.movie.title}/{filename}'
    person_photo = models.ImageField(null=True, blank=True)
    personphoto_thumbnail = ImageSpecField(source='person_photo',
                                      processors=[Thumbnail(200, 200)],
                                      format='JPEG',
                                      options={'quality': 100})