# FILMArchive

### accounts/models.py

```python
class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
```

### accounts/views.py

```python
@login_required
def follow(request, user_pk):
    User = get_user_model()
    you = User.objects.get(pk=user_pk)
    me = request.user
    if you != me:
        if me in you.followers.all():
            you.followers.remove(me)
        else:
            you.followers.add(me)
    return redirect('accounts:profile', you.username)
```

### accounts/profile.html

```html
<form action="{% url 'accounts:follow' person.pk %}" method=="POST">
    {% csrf_token %}
    {% if request.user in person.followers.all %}
        <input type="submit" value="UnFollow" class="btn btn-info btn-fill pull-right">
    {% else %}
        <input type="submit" value="Follow" class="btn btn-info btn-fill pull-right">
    {% endif %}
</form>
```

### movies/views.py

```python
def index(request,...):
    # movie 평균 평점 갱신
    avg_movies = Movie.objects.annotate(avg_rate=Avg('review__rate'))
    for movie in avg_movies:
        if movie.avg_rate:
            movie.rate = round(movie.avg_rate, 1)
            movie.save()
    ...

def genre(request, genre):
    movies = Movie.objects.filter(genre = genre).order_by('-rate')
    context = {
        'movies': movies,
        'genre': genre,
    }
    return render(request, 'movies/genre.html', context)

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
```

### movies/update.html

```html
{% extends 'base.html' %}

{% block style %}
<style>
  body {
    margin: 5rem;
  }
</style>
{% endblock style %}

{% block content %}
<form action="{% url 'movies:update' movie.pk %}" method="POST" enctype="multipart/form-data">
  {% csrf_token %}
  {% for field in update_form %}
  <div class="input-group mb-3">
    <span class="input-group-text" style = "width: 13rem;" id="{{ field.auto_id }}">{{ field.label }}</span>
    {{ field }}
  </div> 
  {% endfor %}
  <div class="mb-3">
      <p class="mb-1">추가할 이미지</p>
      {{ image_form }}
    </div>
    <p class="mb-1">삭제할 이미지</p>
    <ul>
      {% for image in images %}
      <li>
        <img src="{{ image.image_movie_thumbnail.url }}" alt="{{ image.image_movie }}" width="100px;">
        <input type="checkbox" name="delete_images" value="{{ image.id }}" id="delete_images-{{ image.id }}">
        <label for="delete_images-{{ image.id }}">{{ image.image_movie }}</label>
      </li>
      {% endfor %}
    </ul>
  <div class="d-grid gap-2 mb-2">
    <input type="submit" class="btn btn-primary" value="UPDATE">
  </div>
</form>
{% endblock content %}
```

### movies/index.html

```html
<div class="row">
<h2>장르별 영화</h2>
{% regroup movies_genre by genre as genre_list %}
{% for genre in genre_list %}
<div class="card mb-3" style="width: 15rem;">
    <ul class="list-group list-group-flush">
    <li class="list-group-item"><a href="{% url 'movies:genre' genre.grouper %}">{{ genre.grouper }}</a></li>
    </ul>
</div>
{% endfor %}
</div>
```

### magazines/views.py

```python
def detail(request, magazine_id):
    magazine = Magazine.objects.get(pk=magazine_id)
    movies = magazine.magazinemovie_set.all()
    mgzn_movies = [movie.movie for movie in movies]
    context = {
        'magazine': magazine,
        'mgzn_movies': mgzn_movies,
    }
    return render(request, 'magazines/detail.html', context)
```

### 별점

https://velog.io/@hellocdpa/220305-%EB%A6%AC%EB%B7%B0-%EB%B3%84%EC%A0%90-%EA%B8%B0%EB%8A%A5-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0

### 그래프

https://wikidocs.net/124976

## 검색 API

https://whatisthenext.tistory.com/137
https://vanillacreamdonut.tistory.com/124