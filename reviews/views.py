from django.shortcuts import render, redirect
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from movies.models import Movie
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def create(request, movie_id):
    movie = Movie.objects.get(pk = movie_id)
    if request.method == "POST":
        if Review.objects.filter(user=request.user, movie=movie).exists():
            review_old = Review.objects.get(user=request.user, movie=movie)
            review_form = ReviewForm(request.POST, instance=review_old)
        else:
            review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.rate = request.POST.get('rate')
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
    movie = Movie.objects.get(pk=movie_id)
    review = Review.objects.get(pk=review_id)
    comments = review.comment_set.all()
    comment_form = CommentForm()
    context = {
        'review': review,
        'movie': movie,
        'comment_form': comment_form,
        'comments': comments,
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

@login_required
def likes(request, movie_id, review_id):
    movie = Movie.objects.get(pk=movie_id)
    review = Review.objects.get(pk=review_id)
    if request.user in review.like_users.all():
        review.like_users.remove(request.user)
    else:
        review.like_users.add(request.user)
    return redirect('reviews:detail', movie.pk, review.pk)

def comments(request, movie_id, review_id):
    movie = Movie.objects.get(pk=movie_id)
    review = Review.objects.get(pk=review_id)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.review = review
        comment.save()
        return redirect('reviews:detail', movie_id=movie_id, review_id=review_id)
    context = {
        'comment_form': comment_form,
        'movie': movie,
    }
    return render(request, 'reviews/detail.html', context)

def comment_delete(request, movie_id, review_id, comment_id):
    movie = Movie.objects.get(pk=movie_id)
    review = Review.objects.get(pk=review_id)
    Comment.objects.get(pk=comment_id).delete()
    return redirect('reviews:detail', movie.pk, review.pk)