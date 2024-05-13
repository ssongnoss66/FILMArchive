from django.shortcuts import render, redirect
from .models import Movie, MoviePeople, MoviePhoto
from magazines.models import Magazine, MagazineMovie
from .forms import MovieForm, MoviePeopleForm, MoviePhotoForm
from reviews.models import Review
from reviews.forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Avg, Q
import itertools
from django.http import HttpResponseRedirect
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import json
import urllib.parse
import urllib.request
import requests
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('TMDB_KEY')

# Create your views here.

class URLMaker():
    # base_url 설정 - 클래스 변수 : 클래스 사용 내내 고정된 값 - 모든 클래스에서 공유 가능
    base_url = 'https://developers.themoviedb.org/3'

    # 생성자 - api_key를 인스턴스 변수로 초기화하여 생성
    def __init__(self, key):
        self.key = key

    # 인스턴스 메서드
    # url 반환 
    def get_url(self, category, feature, **kwargs): # param으로 가변인자로 받아온다. - query string방식 이용을 위해
        # - class 속성인 base_url에 접근
        # - category, feature는 인스턴스에 할당되어 있는 변수가 아닌
        #   함수의 인자 argument로 들어온 값이기 때문에 self.변수명 형태가 아니라
        #   인자값(아규먼트값)을 바로 사용한다.
        url = f'{URLMaker.base_url}/{category}/{feature}'

        # 인스턴스 생성 시, 인스턴스 변수로 저장된 api_key 값을 받아온다.
        url += f'?api_key={self.key}'

        # 가변인자로 받아온 값을 쿼리스트링 방식으로 url에 이어준다.
        for key, value in kwargs.items():
            url += f'&{key}={value}'

        return url

    # 인스턴스 메서드
    # 영화 제목을 입력받아 영화 아이디를 반환
    # - 요청으로 받을 응답에 영화정보 데이터(json)가 있을 것이고, 그 id를 반환해줄 것이다.
    def movie_id(self, title):

        # 인스턴스 메서드인 get_url() 호출 (self/movie는 영화제목을 받아 영화정보를 반환)
        # - title을 입력하면 해당 영화제목에 맞는 영화 정보 url을 반환해준다.
        url = self.get_url('search', 'movie', region='KR', language='ko', query=title)

        # 만들어진 url을 통해 서버에 요청해, 응답을 받아온다.
        response = requests.get(url)

        # 받아온 데이터를 json -> dict으로 변환해준다.
        movie_dict = response.json()

        # 만약 영화 제목에 해당하는 값이 있다면 
        if movie_dict.get('results'):
            # movie_dict에서 movie_id를 추출한다.
            result = movie_dict.get('results')[0].get('id')
            # 영화 제목에 해당하는 id 반환
            return result
        # 해당하는 값이 없다면, - result가 비어있다면
        else:
            return None  # None을 출력한다.

def index(request):
    maker = URLMaker('[api_key]')
    print(maker.get_url('movie', 'popular', region='KR', language='ko'))
    # Review.objects.all().delete()
    # movie 평균 평점 갱신
    avg_movies = Movie.objects.annotate(avg_rate=Avg('review__rate'))
    for movie in avg_movies:
        if movie.avg_rate:
            movie.rate = round(movie.avg_rate, 1)
            movie.save()
    movies = Movie.objects.all()
    movies_rate = Movie.objects.filter(rate__isnull=False).order_by('-rate')
    movies_country = Movie.objects.all().order_by('country')
    movies_genre = movies.order_by('genre')
    movies_new = Movie.objects.all().order_by('-created_at')
    magazines = Magazine.objects.all().order_by('-publish_date')

    context = {
        'magazines': magazines,
        'movies_genre': movies_genre,
        'movies_country': movies_country,
        'movies_rate': movies_rate,
        'movies_new': movies_new,
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)
        
def create(request):
    # Movie.objects.all().delete()
    if request.method == 'POST':
        movie_form = MovieForm(request.POST, request.FILES)
        photo_form = MoviePhotoForm(request.POST, request.FILES)
        if movie_form.is_valid():
            movie = movie_form.save(commit=False)
            movie.user = request.user
            movie.save()
            photo = photo_form.save(commit=False)
            photo.movie = movie
            photo.save()
            return redirect('movies:detail', movie.pk)
    else:
        movie_form = MovieForm()
        photo_form = MoviePhotoForm()
        movies_country = Movie.objects.all().order_by('country')
        movies_genre = Movie.objects.all().order_by('genre')
        magazines = Magazine.objects.all()
        
    context = {
        'magazines': magazines,
        'movies_genre': movies_genre,
        'movies_country': movies_country,
        'movie_form': movie_form,
        'photo_form': photo_form,
    }
    return render(request, 'movies/create.html', context)

def detail(request, movie_id):
    movie = Movie.objects.get(pk = movie_id)
    moviepeople = movie.moviepeople_set.all()
    reviews = Review.objects.filter(movie_id=movie_id)
    reviews_num = reviews.count()
    
    # Initialize the count for each number
    count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    # Count the occurrences of each rate value
    for review in reviews:
        rate = review.rate
        if rate in count:
            count[rate] += 1

    # Extract the x and y values from the count dictionary
    x = list(count.keys())
    y = list(count.values())

    # Create the plot within the main thread
    fig, ax = plt.subplots(figsize=(5, 3))
    bars = ax.bar(x, y, color='#cff0cc')

    # Find the maximum count
    max_count = max(y)

    # Find the index of the bar with the maximum count
    max_index = y.index(max_count)

    # Set the color of the bar with the maximum count to black
    bars[max_index].set_color('#3aa159')

    # Remove the border line
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Remove the y-axis ticks
    ax.yaxis.set_ticks([])

    # Save the plot to a memory buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_image = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    moviephotos = movie.moviephoto_set.all()
    if moviephotos.first():
        first_moviephoto = moviephotos.first().image_movie_thumbnail.url
    else:
        first_moviephoto = '/static/beach.jpg'
    movies_country = Movie.objects.all().order_by('country')
    movies_genre = Movie.objects.all().order_by('genre')
    magazines = Magazine.objects.all()
    if request.method == 'POST':
        if Review.objects.filter(user=request.user, movie=movie).exists():
            review = Review.objects.get(user=request.user, movie=movie)
            rate = request.POST.get('rate')  # Get the selected rating value from the form data
            review.rate = int(rate)
            review.movie = movie
            review.user=request.user
            review.save()
             # movie 평균 평점 갱신
            avg_movies = Movie.objects.annotate(avg_rate=Avg('review__rate'))
            for movie in avg_movies:
                if movie.avg_rate:
                    movie.rate = round(movie.avg_rate, 1)
                    movie.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            rate = request.POST.get('rate')  # Get the selected rating value from the form data
            review = Review(rate=int(rate), movie=movie, user=request.user)
            review.save()
             # movie 평균 평점 갱신
            avg_movies = Movie.objects.annotate(avg_rate=Avg('review__rate'))
            for movie in avg_movies:
                if movie.avg_rate:
                    movie.rate = round(movie.avg_rate, 1)
                    movie.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    context = {
        'magazines': magazines,
        'movies_genre': movies_genre,
        'movies_country': movies_country,
        'movie': movie,
        'moviepeople': moviepeople,
        'reviews': reviews,
        'moviephotos': moviephotos,
        'first_moviephoto': first_moviephoto,
        'graph_image': graph_image,
        'reviews_num': reviews_num
    }
    return render(request, 'movies/detail.html', context)

def delete(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    if request.user == movie.user:
        movie.delete()
    return redirect('movies:index')

def update(request, movie_id):
    movie = Movie.objects.get(pk = movie_id)
    image = MoviePhoto.objects.filter(movie_id=movie_id)
    images = movie.moviephoto_set.all()
    if request.method=="POST":
        update_form = MovieForm(request.POST, request.FILES, instance=movie)
        if update_form.is_valid():
            update = update_form.save(commit=False)
            update.user = request.user
            update.save()
            for img in request.FILES.getlist('image_movie'):
                photo = MoviePhoto()
                photo.movie = movie
                photo.image_movie = img
                photo.save()
            images_to_delete = request.POST.getlist('delete_images')
            for image_id in images_to_delete:
                image = MoviePhoto.objects.get(pk=image_id)
                image.delete()
            return redirect('movies:detail', movie.pk)
    else:
        update_form = MovieForm(instance=movie)
        image_form = MoviePhotoForm
        movies_country = Movie.objects.all().order_by('country')
        movies_genre = Movie.objects.all().order_by('genre')
        magazines = Magazine.objects.all()
    context = {
        'magazines': magazines,
        'movies_genre': movies_genre,
        'movies_country': movies_country,
        'update_form': update_form,
        'image_form': image_form,
        'movie': movie,
        'images': images,
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
        movies_country = Movie.objects.all().order_by('country')
        movies_genre = Movie.objects.all().order_by('genre')
        magazines = Magazine.objects.all()
    context = {
        'magazines': magazines,
        'movies_genre': movies_genre,
        'movies_country': movies_country,
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

@login_required
def wish(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    if request.user in movie.wish_users.all():
        movie.wish_users.remove(request.user)
        is_wished = False
    else:
        movie.wish_users.add(request.user)
        is_wished = True
    context = {
        'is_wished': is_wished,
    }
    return JsonResponse(context)

@login_required
def grouper_wsh(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    if request.user in movie.wish_users.all():
        movie.wish_users.remove(request.user)
    else:
        movie.wish_users.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def genre(request, genre):
    movies = Movie.objects.filter(genre = genre).order_by('-rate')
    movies_country = Movie.objects.all().order_by('country')
    movies_genre = Movie.objects.all().order_by('genre')
    magazines = Magazine.objects.all()
    
    context = {
        'magazines': magazines,
        'movies_genre': movies_genre,
        'movies_country': movies_country,
        'movies': movies,
        'genre': genre,
    }
    return render(request, 'movies/genre.html', context)

def country(request, country):
    movies = Movie.objects.filter(country = country).order_by('-rate')
    movies_country = Movie.objects.all().order_by('country')
    movies_genre = Movie.objects.all().order_by('genre')
    magazines = Magazine.objects.all()
    
    context = {
        'magazines': magazines,
        'movies_genre': movies_genre,
        'movies_country': movies_country,
        'movies': movies,
        'country': country,
    }
    return render(request, 'movies/country.html', context)

def magazine(request, magazine_id):
    magazine = Magazine.objects.get(pk=magazine_id)
    movies_all = magazine.magazinemovie_set.all()
    movies_raw = [movie.movie for movie in movies_all]
    def get_rate(movie):
        return movie.rate or 0  # Use 0 as the default value if rate is None
    movies = sorted(movies_raw, key=get_rate, reverse=True)  # Sort movies by rate
    movies_country = Movie.objects.all().order_by('country')
    movies_genre = Movie.objects.all().order_by('genre')
    magazines = Magazine.objects.all()
    context = {
        'magazines': magazines,
        'movies_genre': movies_genre,
        'movies_country': movies_country,
        'movies': movies,
        'magazine': magazine,
    }
    return render(request, 'movies/magazine.html', context)

def every_movies(request):
    movies = Movie.objects.all().order_by('-rate')
    movies_country = Movie.objects.all().order_by('country')
    movies_genre = Movie.objects.all().order_by('genre')
    magazines = Magazine.objects.all()
    context = {
        'magazines': magazines,
        'movies_genre': movies_genre,
        'movies_country': movies_country,
        'movies': movies,
    }
    return render(request, 'movies/every_movies.html', context)