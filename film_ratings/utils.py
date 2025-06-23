import requests
from django.conf import settings

def fetch_movie_data(title):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "query": title
    }
    response = requests.get(url, params=params)
    
    try:
        data = response.json()
    except Exception as e:
        print("Error parsing JSON:", e)
        return None

    print("Status Code:", response.status_code)
    print("Results:", data.get("results"))

    if data.get("results"):
        movie = data["results"][0]
        return {
            "title": movie.get("title"),
            "release_year": movie.get("release_date", "")[:4],
            "poster_url": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else "",
            "description": movie.get("overview"),
            "tmdb_id": movie.get("id")
        }
    else:
        return None