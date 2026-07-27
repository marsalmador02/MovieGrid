import httpx
from app.core.config import settings
from app.core.database import SessionLocal
from app.models import Movie, Genre, MovieGenre

TMDB_BASE_URL = "https://api.themoviedb.org/3"

def get_popular_movies_page1():
    headers = {"Authorization": f"Bearer {settings.TMDB_API_KEY}"}
    response = httpx.get(f"{TMDB_BASE_URL}/movie/popular", headers=headers)
    response.raise_for_status()
    return response.json()

def get_genre_list():
    headers = {"Authorization": f"Bearer {settings.TMDB_API_KEY}"}
    response = httpx.get(f"{TMDB_BASE_URL}/genre/movie/list", headers=headers)
    response.raise_for_status()
    return response.json()["genres"]

data = get_popular_movies_page1()
primera = data["results"][0]
generos_tmdb = get_genre_list()

db = SessionLocal()

pelicula = db.get(Movie, primera["id"])
if not pelicula:
    pelicula = Movie(
        movie_id=primera["id"],
        title=primera["title"],
        release_year=int(primera["release_date"][:4]),
    )
    db.add(pelicula)
    db.commit()
    print(f"Película guardada: {pelicula.title}")
else:
    print(f"Película ya existía: {pelicula.title}")

for g in generos_tmdb:
    genero_existente = db.get(Genre, g["id"])
    if not genero_existente:
        db.add(Genre(genre_id=g["id"], name=g["name"]))
db.commit()
print("Tabla de géneros actualizada.")

for genre_id in primera["genre_ids"]:
    vinculo_existente = db.get(MovieGenre, {"movie_id": pelicula.movie_id, "genre_id": genre_id})
    if not vinculo_existente:
        db.add(MovieGenre(movie_id=pelicula.movie_id, genre_id=genre_id))
db.commit()
print(f"Géneros vinculados: {primera['genre_ids']}")

db.close()