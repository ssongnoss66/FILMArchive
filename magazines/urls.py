from django.urls import path
from . import views

app_name = 'magazines'
urlpatterns = [
    path('create/', views.create, name='create'),
    path('<int:magazine_id>/', views.detail, name='detail'),
    path('<int:magazine_id>/delete/', views.delete, name='delete'),
    path('<int:magazine_id>/update/', views.update, name='update'),
    path('<int:magazine_id>/movie/', views.mgzn_movie, name='mgzn_movie'),
    path('<int:magazine_id>/movie/<int:movie_id>/delete/', views.mgzn_movie_delete, name='mgzn_movie_delete'),
]
