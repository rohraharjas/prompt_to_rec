import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def get_movie_poster(movie_id: int) -> str:
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"{TMDB_IMAGE_BASE_URL}{poster_path}"
        else:
            print("Poster not found for movie ID:", movie_id)
            return None
    else:
        print(f"Failed to fetch movie data: {response.status_code}")
        print(response.content)
        return None

# TEST
# poster_url = get_movie_poster(550)  
# print(poster_url)