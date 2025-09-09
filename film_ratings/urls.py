from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("movie/<int:movie_id>/", views.film_details, name="film_details"),
    path("movie_form/", views.new_film_form, name="movie_form"),
    path("movie/<int:movie_id>/review/new/", views.review_from_details, name="review_new"),
    path("search_movies/", views.search_movies, name="search_movies"),
    path("autocomplete_movies/", views.autocomplete_movies, name="autocomplete_movies"),
    path("search_autocomplete/", views.search_autocomplete, name="search_autocomplete"),
    path("select_movie/", views.select_movie, name="select_movie"),
    path("search_select_movie/", views.search_select_movie, name="search_select_movie")
]
