from django.core.management.base import BaseCommand
from django.conf import settings
from film_ratings.models import Movie
import requests
import time

TMDB_API_KEY = settings.TMDB_API_KEY

class Command(BaseCommand):
    help = 'Updates missing fields in Movie model using TMDb API'

    def handle(self, *args, **kwargs):
        movies_to_update = Movie.objects.filter(
            tmdb_id__isnull=True
        ) | Movie.objects.filter(description__isnull=True) | Movie.objects.filter(poster_url__isnull=True)

        updated_count = 0

        for movie in movies_to_update.distinct():
            print(f"Updating: {movie.title} ({movie.release_year})")
            try:
                # Search TMDb by title and year
                search_url = 'https://api.themoviedb.org/3/search/movie'
                params = {
                    'api_key': TMDB_API_KEY,
                    'query': movie.title,
                    'year': movie.release_year,
                    'language': 'en-US',
                }
                response = requests.get(search_url, params=params)
                response.raise_for_status()
                results = response.json().get('results')

                if not results:
                    print(f"  No TMDb results for: {movie.title}")
                    continue

                # Use the first result
                match = results[0]
                tmdb_id = match['id']

                # Get full details
                detail_url = f'https://api.themoviedb.org/3/movie/{tmdb_id}'
                detail_params = {
                    'api_key': TMDB_API_KEY,
                    'language': 'en-US',
                }
                detail_resp = requests.get(detail_url, params=detail_params)
                detail_resp.raise_for_status()
                data = detail_resp.json()

                updated = False
                if not movie.tmdb_id:
                    movie.tmdb_id = data['id']
                    updated = True
                if not movie.poster_url and data.get('poster_path'):
                    movie.poster_url = f"https://image.tmdb.org/t/p/w200{data['poster_path']}"
                    updated = True
                if not movie.description and data.get('overview'):
                    movie.description = data['overview']
                    updated = True

                if updated:
                    movie.save()
                    updated_count += 1
                    print(f"  ✅ Updated {movie.title}")
                else:
                    print(f"  ℹ️ Already complete")

                time.sleep(0.25)  # Be kind to the API

            except Exception as e:
                print(f"  ❌ Error updating {movie.title}: {e}")

        print(f"\nDone! {updated_count} movies updated.")