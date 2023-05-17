from django.shortcuts import render, redirect
from .models import Movie, MoviePeople
from magazines.models import Magazine, MagazineMovie
from .forms import MovieForm, MoviePeopleForm
from reviews.models import Review
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Avg, Q

# Create your views here.
def index(request):
    # movie 평균 평점 갱신
    avg_movies = Movie.objects.annotate(avg_rate=Avg('review__rate'))
    for movie in avg_movies:
        if movie.avg_rate:
            movie.rate = round(movie.avg_rate, 1)
            movie.save()
    movies_rate = Movie.objects.filter(rate__isnull=False).order_by('-rate')
    movies_genre = Movie.objects.all().order_by('genre')
    movies_country = Movie.objects.all().order_by('country')
    movies_genre = Movie.objects.all().order_by('genre')
    magazines = Magazine.objects.all()
    
    context = {
        'movies_rate': movies_rate,
        'magazines': magazines,
        'movies_genre': movies_genre,
        'movies_country': movies_country,
    }
    return render(request, 'movies/index.html', context)

def create(request):
    # Movie.objects.all().delete()
    if request.method == 'POST':
        movie_form = MovieForm(request.POST, request.FILES)
        if movie_form.is_valid():
            movie = movie_form.save(commit=False)
            movie.user = request.user
            movie.save()
            return redirect('movies:detail', movie.pk)
    else:
        movie_form = MovieForm()
    context = {
        'movie_form': movie_form
    }
    return render(request, 'movies/create.html', context)

def detail(request, movie_id):
    movie = Movie.objects.get(pk = movie_id)
    moviepeople = movie.moviepeople_set.all()
    reviews = Review.objects.filter(movie_id=movie_id)
    context = {
        'movie': movie,
        'moviepeople': moviepeople,
        'reviews': reviews,
    }
    return render(request, 'movies/detail.html', context)

def delete(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    if request.user == movie.user:
        movie.delete()
    return redirect('movies:index')

def update(request, movie_id):
    movie = Movie.objects.get(pk = movie_id)
    if request.method=="POST":
        update_form = MovieForm(request.POST, request.FILES, instance=movie)
        if update_form.is_valid():
            update = update_form.save(commit=False)
            update.user = request.user
            update.save()
            return redirect('movies:detail', movie.pk)
    else:
        update_form = MovieForm(instance=movie)
    context = {
        'update_form': update_form,
        'movie': movie,
    }
    return render(request, 'movies/update.html', context)

def person(request, movie_id):
    movie = Movie.objects.get(pk = movie_id)
    if request.method == "POST":
        person_form = MoviePeopleForm(request.POST, request.FILES)
        if person_form.is_valid():
            person = person_form.save(commit=False)
            person.movie = movie
            person.save()
            return redirect('movies:detail', movie.pk)
    else:
        person_form = MoviePeopleForm()
    context = {
        'person_form': person_form,
        'movie': movie,
    }
    return render(request, 'movies/person.html', context)

def person_delete(request, movie_id, person_id):
    person = MoviePeople.objects.get(pk = person_id)
    movie = Movie.objects.get(pk = movie_id)
    if request.user == movie.user:
        person.delete()
    return redirect('movies:detail', movie.pk)

def wish(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    if request.user in movie.wish_users.all():
        movie.wish_users.remove(request.user)
    else:
        movie.wish_users.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def genre(request, genre):
    movies = Movie.objects.filter(genre = genre).order_by('-rate')
    context = {
        'movies': movies,
        'genre': genre,
    }
    return render(request, 'movies/genre.html', context)

def country(request, country):
    movies = Movie.objects.filter(country = country).order_by('-rate')
    context = {
        'movies': movies,
        'country': country,
    }
    return render(request, 'movies/country.html', context)

def magazine(request, magazine_id):
    magazine = Magazine.objects.get(pk=magazine_id)
    movies_all = magazine.magazinemovie_set.all()
    movies = [movie.movie for movie in movies_all]
    context = {
        'movies': movies,
        'magazine': magazine,
    }
    return render(request, 'movies/magazine.html', context)