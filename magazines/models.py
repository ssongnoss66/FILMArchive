from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from movies.models import Movie

# Create your models here.
class Magazine(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mgzn_title = models.CharField(max_length=50, null=True, blank=True)
    def image_path(instance, filename):
        return f'magazines/{instance.mgzn_title}/{filename}'
    cover = models.ImageField(upload_to=image_path)
    cover_thumbnail = ImageSpecField(source='cover',
                                      processors=[Thumbnail(200, 260)],
                                      format='JPEG',
                                      options={'quality': 100})
    publish_date = models.DateField(null=True, blank=True)
    official = models.URLField(null=True, blank=True)
    where_to_buy = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MagazineMovie(models.Model):
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)