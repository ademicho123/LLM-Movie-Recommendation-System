import requests
from config import MOVIE_DB_API_KEY

BASE_URL = "https://api.themoviedb.org/3"

def search_movie(query):
    """Search for movies based on user query."""
    url = f"{BASE_URL}/search/movie?query={query}&api_key={MOVIE_DB_API_KEY}"
    response = requests.get(url)
    return response.json()

def get_popular_movies():
    """Fetch popular movies."""
    url = f"{BASE_URL}/movie/popular?api_key={MOVIE_DB_API_KEY}"
    response = requests.get(url)
    return response.json()

def get_top_rated_movies():
    """Fetch top-rated movies."""
    url = f"{BASE_URL}/movie/top_rated?api_key={MOVIE_DB_API_KEY}"
    response = requests.get(url)
    return response.json()
