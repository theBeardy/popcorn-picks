from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("movie/<int:movie_id>/", views.film_details, name="film_details"),
    path("movie_form/", views.new_film_form, name="movie_form"),
]
