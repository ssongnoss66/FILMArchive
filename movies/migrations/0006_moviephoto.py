# Generated by Django 3.2.18 on 2023-05-19 07:27

from django.db import migrations, models
import django.db.models.deletion
import movies.models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20230512_1439'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoviePhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_movie', models.ImageField(blank=True, null=True, upload_to=movies.models.MoviePhoto.image_path)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
        ),
    ]
