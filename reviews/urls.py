from django.urls import path
from . import views

app_name = 'reviews'
urlpatterns = [
    path('<int:movie_id>/create/', views.create, name='create'),
    path('<int:movie_id>/<int:review_id>/', views.detail, name='detail'),
    path('<int:movie_id>/<int:review_id>/delete', views.delete, name='delete'),
    path('<int:movie_id>/<int:review_id>/update', views.update, name='update'),
]
    # path('<int:movie_id>/<int:review_id>/likes/', views.likes, name='likes'),
    # path('<int:movie_id>/<int:review_id>/comments/', views.comments, name='comments'),
    # path('<int:movie_id>/<int:review_id>/comments/int:comment_pk/delete/', views.comment_delete, name='comment_delete'),

