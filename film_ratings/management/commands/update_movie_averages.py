from django.core.management.base import BaseCommand
from film_ratings.models import Movie

class Command(BaseCommand):
    help = 'Recalculates and updates average rating for all movies.'

    def handle(self, *args, **kwargs):
        count = 0

        for movie in Movie.objects.all():
            scores = [
                movie.visuals,
                movie.acting,
                movie.thought_provoking,
                movie.dialog,
                movie.makes_me_cry,
                movie.genre_execution,
                movie.rewatchability,
                movie.fun_to_watch,
            ]
            movie.average = round(sum(scores)/len(scores), 2)
            movie.save()
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} movie(s).'))