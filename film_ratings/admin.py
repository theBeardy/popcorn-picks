from django.contrib import admin

from .models import Movie, Review

@admin.register(Movie)

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'id')

@admin.register(Review)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie_title', 'average', 'recommend')