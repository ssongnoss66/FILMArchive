from django.shortcuts import render
from magazines.models import Magazine
from movies.models import Movie

def base(request):
    movies_country = Movie.objects.all().order_by('country')
    movies_genre = Movie.objects.all().order_by('genre')
    magazines = Magazine.objects.all()
    
    context = {
        'magazines': magazines,
        'movies_genre': movies_genre,
        'movies_country': movies_country,
    }
    return render(request, 'base.html', context)