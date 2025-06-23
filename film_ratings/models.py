from django.db import models

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
import datetime

RECOMMENDATION_CHOICES = (
    ("Y", 'Yes'),
    ("N", 'No'),
    ("S", 'To someone who likes the genre')
)

class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField(blank= True, null=True)
    description = models.TextField(null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    tmdb_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_title = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
    visuals = models.FloatField("visuals")
    acting = models.FloatField("acting")
    thought_provoking = models.FloatField("meaning")
    dialog = models.FloatField("dialogue")
    makes_me_cry = models.FloatField("crying")
    genre_execution = models.FloatField("genre")
    rewatchability = models.FloatField("rewatch")
    fun_to_watch = models.FloatField("fun_to_watch")
    average = models.FloatField(blank=True, null=True)
    recommend = models.CharField(
        choices=RECOMMENDATION_CHOICES, 
        max_length=128,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Review of {self.movie_title} by {self.user.username}"
    
    def average_rating(self):
        ratings = [
            self.visuals, self.acting, self.thought_provoking, self.dialog, self.makes_me_cry, self.genre_execution, self.rewatchability, self.fun_to_watch if self.fun_to_watch else 8,
        ]
        return round((sum(ratings) / len(ratings)), 2)
    
    def save(self, *args, **kwargs):
        self.average = self.average_rating()
        super().save(*args, **kwargs)