from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('pickup/', views.pickup, name='pickup'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('<int:movie_id>/delete/', views.delete, name='delete'),
    path('<int:movie_id>/update', views.update, name='update'),
    path('<int:movie_id>/person/', views.person, name='person'),
    path('<int:movie_id>/person/<int:person_id>/delete/', views.person_delete, name='person_delete'),
    path('<int:movie_id>/grouper_wsh/', views.grouper_wsh, name='grouper_wsh'),
    path('<int:movie_id>/wish/', views.wish, name='wish'),
    path('genre/<str:genre>', views.genre, name='genre'),
    path('country/<str:country>', views.country, name='country'),
    path('magazine/<int:magazine_id>', views.magazine, name='magazine'),
    path('every_movies/', views.every_movies, name='every_movies'),
]
