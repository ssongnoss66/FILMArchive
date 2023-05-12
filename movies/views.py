from django.shortcuts import render, redirect
from .models import Movie, MoviePeople
from .forms import MovieForm, MoviePeopleForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'movies/index.html')

def create(request):
    Movie.objects.all().delete()
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
    context = {
        'movie': movie,
        'moviepeople': moviepeople,
    }
    return render(request, 'movies/detail.html', context)

def delete(request, movie_id):
    Movie.objects.get(pk=movie_id).delete()
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