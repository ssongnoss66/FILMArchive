from django.shortcuts import render, redirect
from .models import Magazine, MagazineMovie, Movie
from .forms import MagazineForm, MagazineMovieForm

# Create your views here.
def create(request):
    if request.method == "POST":
        magazine_form = MagazineForm(request.POST, request.FILES)
        if magazine_form.is_valid():
            magazine = magazine_form.save(commit=False)
            magazine.user = request.user
            magazine.save()
            return redirect('magazines:detail', magazine.pk)
    else:
        magazine_form = MagazineForm()
        movies_country = Movie.objects.all().order_by('country')
        movies_genre = Movie.objects.all().order_by('genre')
        magazines = Magazine.objects.all()
        
    context = {
        'magazines': magazines,
        'movies_genre': movies_genre,
        'movies_country': movies_country,
        'magazine_form': magazine_form,
    }
    return render(request, 'magazines/create.html', context)

def detail(request, magazine_id):
    magazine = Magazine.objects.get(pk=magazine_id)
    movies = magazine.magazinemovie_set.all()
    mgzn_movies = [movie.movie for movie in movies]
    movies_country = Movie.objects.all().order_by('country')
    movies_genre = Movie.objects.all().order_by('genre')
    magazines = Magazine.objects.all()
    context = {
        'magazines': magazines,
        'movies_genre': movies_genre,
        'movies_country': movies_country,
        'magazine': magazine,
        'mgzn_movies': mgzn_movies,
    }
    return render(request, 'magazines/detail.html', context)

def delete(request, magazine_id):
    magazine = Magazine.objects.get(pk=magazine_id)
    if request.user == magazine.user:
        magazine.delete()
    return redirect('movies:index')

def update(request, magazine_id):
    magazine = Magazine.objects.get(pk=magazine_id)
    if request.method == "POST":
        update_form = MagazineForm(request.POST, request.FILES, instance=magazine)
        if update_form.is_valid():
            update = update_form.save(commit=False)
            update.user = request.user
            update.save()
            return redirect('magazines:detail', magazine.pk)
    else:
        update_form = MagazineForm(instance=magazine)
        movies_country = Movie.objects.all().order_by('country')
        movies_genre = Movie.objects.all().order_by('genre')
        magazines = Magazine.objects.all()
    context = {
        'magazines': magazines,
        'movies_genre': movies_genre,
        'movies_country': movies_country,
        'update_form': update_form,
        'magazine': magazine,
    }
    return render(request, 'magazines/update.html', context)
    

def mgzn_movie(request, magazine_id):
    magazine = Magazine.objects.get(pk=magazine_id)
    if request.method=="POST":
        mgzn_movie_form = MagazineMovieForm(request.POST)
        if mgzn_movie_form.is_valid():
            mgzn_movie = mgzn_movie_form.save(commit=False)
            mgzn_movie.magazine = magazine
            mgzn_movie.save()
            return redirect('magazines:detail', magazine.pk)
    else:
        mgzn_movie_form = MagazineMovieForm()
        movies_country = Movie.objects.all().order_by('country')
        movies_genre = Movie.objects.all().order_by('genre')
        magazines = Magazine.objects.all()
        
    context = {
        'magazines': magazines,
        'movies_genre': movies_genre,
        'movies_country': movies_country,
        'magazine': magazine,
        'mgzn_movie_form': mgzn_movie_form,
    }
    return render(request, 'magazines/mgzn_movie.html', context)

def mgzn_movie_delete(request, magazine_id, movie_id):
    magazine = Magazine.objects.get(pk=magazine_id)
    mgzn_movie = MagazineMovie.objects.get(movie_id=movie_id)
    if request.user == magazine.user:
        mgzn_movie.delete()
    return redirect('magazines:detail', magazine.pk)