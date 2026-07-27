import httpx
from app.core.config import settings
from app.core.database import SessionLocal
from app.models import Movie

TMDB_BASE_URL = "https://api.themoviedb.org/3"

def get_popular_movies_page1():
    headers = {"Authorization": f"Bearer {settings.TMDB_API_KEY}"}
    response = httpx.get(f"{TMDB_BASE_URL}/movie/popular", headers=headers)
    response.raise_for_status()
    return response.json()

data = get_popular_movies_page1()
primera = data["results"][0]

print(f"Guardando: {primera['title']} ({primera['release_date']})")

db = SessionLocal()

nueva_pelicula = Movie(
    movie_id=primera["id"],
    title=primera["title"],
    release_year=int(primera["release_date"][:4]),
)

db.add(nueva_pelicula)
db.commit()

print("Guardada correctamente.")
db.close()