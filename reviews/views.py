from django.shortcuts import render, redirect
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from movies.models import Movie

# Create your views here.
def create(request, movie_id):
    movie = Movie.objects.get(pk = movie_id)
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review=review_form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('movies:detail', movie.pk)
    else:
        review_form = ReviewForm()
    context = {
        'movie': movie,
        'review_form': review_form
    }
    return render(request, 'reviews/create.html', context)

def detail(request, movie_id, review_id):
    review = Review.objects.get(pk=review_id)
    context = {
        'review': review,
    }
    return render(request, 'reviews/detail.html', context)

def delete(request, movie_id, review_id):
    Review.objects.get(pk=review_id).delete()
    return redirect('movies:detail', movie_id)

def update(request, movie_id, review_id):
    movie = Movie.objects.get(pk=movie_id)
    review = Review.objects.get(pk=review_id)
    if request.method == "POST":
        update_form = ReviewForm(request.POST, instance=review)
        if update_form.is_valid():
            update_form.save(commit=False)
            update.user = request.user
            update.save()
            return redirect('reviews:detail', movie.pk, review.pk)
    else:
        update_form = ReviewForm(instance=review)
    context = {
        'update_form': update_form,
        'movie': movie,
        'review': review,
    }
    return render(request, 'reviews/update.html', context)