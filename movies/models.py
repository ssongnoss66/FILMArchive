from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail

# Create your models here.
genre_CHOICES = [
    ("드라마", "드라마"),
    ("판타지", "판타지"),
    ("서부", "서부"),
    ("공포", "공포"),
    ("로맨스", "로맨스"),
    ("모험", "모험"),
    ("스릴러", "스릴러"),
    ("느와르", "느와르"),
    ("컬트", "컬트"),
    ("다큐멘터리", "다큐멘터리"),
    ("코미디", "코미디"),
    ("가족", "가족"),
    ("미스터리", "미스터리"),
    ("전쟁", "전쟁"),
    ("애니메이션", "애니메이션"),
    ("범죄", "범죄"),
    ("뮤지컬", "뮤지컬"),
    ("SF", "SF"),
    ("액션", "액션"),
    ("무협", "무협"),
    ("에로", "에로"),
    ("서스펜스", "서스펜스"),
    ("서사", "서사"),
    ("블랙코미디", "블랙코미디"),
    ("실험", "실험"),
    ("영화카툰", "영화카툰"),
    ("영화음악", "영화음악"),
    ("영화패러디포스터", "영화패러디포스터"),
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