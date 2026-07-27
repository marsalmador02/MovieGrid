import httpx
from app.core.config import settings

TMDB_BASE_URL = "https://api.themoviedb.org/3"

def get_popular_movies_page1():
    headers = {"Authorization": f"Bearer {settings.TMDB_API_KEY}"}
    response = httpx.get(f"{TMDB_BASE_URL}/movie/popular", headers=headers)
    response.raise_for_status()
    return response.json()

data = get_popular_movies_page1()
print(f"Total de resultados: {data['total_results']}")
print(f"Primera película: {data['results'][0]['title']}")