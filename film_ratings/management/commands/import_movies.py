from django.core.management.base import BaseCommand
from film_ratings.models import Movie, Review
from film_ratings.utils import fetch_movie_data

class Command(BaseCommand):
    help = "Imports a batch of movies from a list of titles using TMDb."

    def add_arguments(self, parser):
        parser.add_argument('titles', nargs='+', type=str, help="List of movie titles")

    def handle(self, *args, **options):
        for title in options['titles']:
            existing = Movie.objects.filter(title__iexact=title).first()
            if existing:
                self.stdout.write(self.style.WARNING(f"'{title}' already exists. Skipping."))

            data = fetch_movie_data(title)
            if not data:
                self.stdout.write(self.style.ERROR(f"Failed to fetch data for '{title}"))
                continue

            Movie.objects.create(
                title=data["title"],
                release_year=data["release_year"],
                description=data["description"],
                poster_url=data["poster_url"],
                tmdb_id=data["tmdb_id"]
            )
            self.stdout.write(self.style.SUCCESS(f"Added '{title}' successfully."))