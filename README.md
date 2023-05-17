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