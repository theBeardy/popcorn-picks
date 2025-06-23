from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from film_ratings.models import Movie, Review
from film_ratings.utils import fetch_movie_data
import csv

class Command(BaseCommand):
    help = "Import Movies and Reviews from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        path = options['csv_file']
        with open(path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            reader.fieldnames = [field.strip().lower() for field in reader.fieldnames]
            for row in reader:
                print(row.keys())
                title = row.get('title')
                if not title:
                    self.stdout.write(self.style.ERROR("Missing 'title' in row"))
                    continue
                title = title.strip()
                existing = Movie.objects.filter(title__iexact=title).first()
                if existing:
                    self.stdout.write(self.style.WARNING(f"'{title}' already exists. Skipping."))
                
                data = fetch_movie_data(title)
                if not data:
                    self.stdout.write(self.style.ERROR(f"Failed to fetch data for {title}"))
                    continue

                movie = Movie.objects.create(
                    title=data["title"],
                    release_year=data["release_year"],
                    description=data["description"],
                    poster_url=data["poster_url"],
                    tmdb_id=data["tmdb_id"]
                )

                Review.objects.create(
                    user = User.objects.get(username='admin'),
                    movie_title=movie,
                    visuals=float(row['visuals'].strip()),
                    acting=float(row['acting'].strip()),
                    thought_provoking=float(row['thought_provoking'].strip()),
                    dialog=float(row['dialog'].strip()),
                    makes_me_cry=float(row['makes_me_cry'].strip()),
                    genre_execution=float(row['genre_execution'].strip()),
                    rewatchability=float(row['rewatch'].strip()),
                    fun_to_watch=float(row['fun_to_watch'].strip()),
                    recommend=row['recommend'],
                )
                self.stdout.write(self.style.SUCCESS(f"Added '{title}' successfully."))