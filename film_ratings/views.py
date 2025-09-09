import requests
from django.conf import settings
from django.db.models import Avg
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Review
from .forms import MovieForm, MovieFormModal
from .utils import fetch_movie_data

def index(request):
    film_list = Movie.objects.annotate(average_rating=Avg('review__average')).order_by('-average_rating')
    return render(request, "film_ratings/index.html", {"film_list": film_list})

TMDB_API_KEY = settings.TMDB_API_KEY  

def search_autocomplete(request):
    query = request.GET.get('movie_search', '')
    results = []

    if query:
        # Search local DB
        local_matches = Movie.objects.filter(title__icontains=query)[:5]
        for m in local_matches:
            results.append({
                'source': 'local',
                'id': m.id,
                'title': m.title,
                'year': m.release_year,
                'poster_url': m.poster_url
            })

        # Also search TMDb
        url = 'https://api.themoviedb.org/3/search/movie'
        params = {
            'api_key': TMDB_API_KEY,
            'query': query,
            'include_adult': 'false',
            'language': 'en-US',
        }
        try:
            response = requests.get(url, params=params, timeout=3)
            if response.status_code == 200:
                data = response.json()
                for item in data.get('results', [])[:5]:
                    results.append({
                        'source': 'tmdb',
                        'id': item['id'],
                        'title': item['title'],
                        'year': item.get('release_date', '')[:4],
                        'poster_url': f"https://image.tmdb.org/t/p/w200{item['poster_path']}" if item.get('poster_path') else None
                    })
        except requests.RequestException:
            pass  # Handle TMDb failure silently or log it

    return render(request, 'partials/search_autocomplete.html', {'results': results})

def search_select_movie(request):
    source = request.GET.get('source')
    movie_id = request.GET.get('id')

    movie = None

    if source == 'local':
        movie = get_object_or_404(Movie, id=movie_id)
    elif source == 'tmdb':
        url = f'https://api.themoviedb.org/3/movie/{movie_id}'
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'en-US',
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            release_year = data.get('release_date', '')[:4]
            poster_url = f"https://image.tmdb.org/t/p/w200{data.get('poster_path')}" if data.get('poster_path') else None
            description = data.get('overview', '')

            movie, created = Movie.objects.get_or_create(
                title=data['title'],
                release_year=release_year,
                defaults={
                    'poster_url': poster_url,
                    'description': description,
                    'tmdb_id': data['id'],
                }
            )

            # If movie existed but missing fields, update them
            updated = False
            if not movie.poster_url and poster_url:
                movie.poster_url = poster_url
                updated = True
            if not movie.description and description:
                movie.description = description
                updated = True
            if not movie.tmdb_id:
                movie.tmdb_id = data['id']
                updated = True
            if updated:
                movie.save()
        
    redirect_url = reverse('film_ratings:film_details', args=[movie.id])
    response = HttpResponse()
    response['HX-Redirect'] = redirect_url
    return response

def select_movie(request):
    source = request.GET.get('source')
    movie_id = request.GET.get('id')

    movie = None

    if source == 'local':
        movie = get_object_or_404(Movie, id=movie_id)
    elif source == 'tmdb':
        url = f'https://api.themoviedb.org/3/movie/{movie_id}'
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'en-US',
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            release_year = data.get('release_date', '')[:4]
            poster_url = f"https://image.tmdb.org/t/p/w200{data.get('poster_path')}" if data.get('poster_path') else None
            description = data.get('overview', '')

            movie, created = Movie.objects.get_or_create(
                title=data['title'],
                release_year=release_year,
                defaults={
                    'poster_url': poster_url,
                    'description': description,
                    'tmdb_id': data['id'],
                }
            )

            # If movie existed but missing fields, update them
            updated = False
            if not movie.poster_url and poster_url:
                movie.poster_url = poster_url
                updated = True
            if not movie.description and description:
                movie.description = description
                updated = True
            if not movie.tmdb_id:
                movie.tmdb_id = data['id']
                updated = True
            if updated:
                movie.save()

    return render(request, 'partials/selected_movie_card.html', {'movie': movie})

def autocomplete_movies(request):
    query = request.GET.get('movie_title', '')
    results = []

    if query:
        # Search local DB
        local_matches = Movie.objects.filter(title__icontains=query)[:5]
        for m in local_matches:
            results.append({
                'source': 'local',
                'id': m.id,
                'title': m.title,
                'year': m.release_year,
                'poster_url': m.poster_url
            })

        # Also search TMDb
        url = 'https://api.themoviedb.org/3/search/movie'
        params = {
            'api_key': TMDB_API_KEY,
            'query': query,
            'include_adult': 'false',
            'language': 'en-US',
        }
        try:
            response = requests.get(url, params=params, timeout=3)
            if response.status_code == 200:
                data = response.json()
                for item in data.get('results', [])[:5]:
                    results.append({
                        'source': 'tmdb',
                        'id': item['id'],
                        'title': item['title'],
                        'year': item.get('release_date', '')[:4],
                        'poster_url': f"https://image.tmdb.org/t/p/w200{item['poster_path']}" if item.get('poster_path') else None
                    })
        except requests.RequestException:
            pass  # Handle TMDb failure silently or log it

    return render(request, 'partials/movie_suggestions.html', {'results': results})

def search_movies(request):
    if request.method == "POST":
        movie_search = request.POST['movie_search']
        movie_results = Movie.objects.filter(title__icontains=movie_search) \
            .annotate(average_rating=Avg('review__average'))
        
        user_reviews = {}
        if request.user.is_authenticated:
            user_review_qs = Review.objects.filter(
                movie_title__in=movie_results, user=request.user
            )
            user_reviews = {review.movie_title.id: review.average for review in user_review_qs}

        return render(request, 'film_ratings/search_movies.html', { 
            'movie_search' : movie_search,
            'movie_results' : movie_results,
            'user_reviews' : user_reviews,
        })
    else:
        return render(request, 'film_ratings/search_movies.html', {})

def film_details(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    # Get all reviews for this movie
    reviews = Review.objects.filter(movie_title=movie)

    # Optionally: calculate average rating across all reviews
    average_rating = reviews.aggregate(avg=Avg('average'))['avg']

    # Optional: get latest review or the first review
    latest_review = reviews.order_by('-id').first()

    context = {
        "movie": movie,
        "reviews": reviews,
        "latest_review": latest_review,
        "average_rating": average_rating,
    }

    return render(request, "film_ratings/film_details.html", context)

def create_or_get_movie(title):
    movie, created = Movie.objects.get_or_create(title=title)
    if created or not movie.description:
        data = fetch_movie_data(title)
        if data:
            movie.release_year = data["release_year"]
            movie.description = data["description"]
            movie.poster_url = data["poster_url"]
            movie.tmdb_id = data["tmdb_id"]
            movie.save()
    return movie

@login_required(login_url='/users/login/')
def new_film_form(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            # Extract title from fake field
            title_input = form.cleaned_data['movie_title'].strip()

            # Try to get or create the Movie
            movie = Movie.objects.filter(title__iexact=title_input).first()
            if not movie:
                tmdb_data = fetch_movie_data(title_input)
                if tmdb_data:
                    movie = Movie.objects.create(
                        title=tmdb_data['title'],
                        release_year=tmdb_data['release_year'],
                        description=tmdb_data['description'],
                        poster_url=tmdb_data['poster_url'],
                        tmdb_id=tmdb_data['tmdb_id']
                    )
                else:
                    form.add_error("movie_title", "Could not find this film on TMDb.")
                    return render(request, 'film_ratings/movie_form.html', {'form': form})

            # Save review
            review = form.save(commit=False)
            review.movie_title = movie  # ✅ This is a Movie instance now
            review.user = request.user
            review.save()
            return redirect('film_ratings:index')
    else:
        form = MovieForm()

    return render(request, 'film_ratings/movie_form.html', {'form': form})

@login_required(login_url='/users/login/')
def review_from_details(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    form = MovieFormModal(request.POST)
    if form.is_valid():
            # Extract title from fake field
            title = movie.title

            # Save review
            review = form.save()
            review.movie_title = movie  # ✅ This is a Movie instance now
            review.user = request.user
            review.save()
            return redirect('film_ratings:index')
    else:
        form = MovieFormModal()

    return render(request, 'partials/review_new.html', {'form':form, 'movie':movie})

@login_required(login_url='/users/login/')
def edit_review_view(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    form = MovieFormModal(instance=movie)
    if form.is_valid():
        review = form.save()
        review.movie_title = movie
        review.user = request.user
        review.save()
        return redirect('film_ratings:index')
    else:
        form = MovieFormModal()
        
    return render(request, 'partials/review_new.html', {'form':form, 'movie':movie})