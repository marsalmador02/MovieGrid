import httpx
from app.core.config import settings
from app.core.database import SessionLocal
from app.models import Movie, Genre, MovieGenre, Person, Credit

TMDB_BASE_URL = "https://api.themoviedb.org/3"
MAX_CAST_PER_MOVIE = 10
PAGES = 100


def _headers():
    return {"Authorization": f"Bearer {settings.TMDB_API_KEY}"}


def get_popular_movies_page(page):
    response = httpx.get(f"{TMDB_BASE_URL}/movie/popular", headers=_headers(), params={"page": page})
    response.raise_for_status()
    return response.json()["results"]


def get_genre_list():
    response = httpx.get(f"{TMDB_BASE_URL}/genre/movie/list", headers=_headers())
    response.raise_for_status()
    return response.json()["genres"]


def get_movie_credits(movie_id):
    response = httpx.get(f"{TMDB_BASE_URL}/movie/{movie_id}/credits", headers=_headers())
    response.raise_for_status()
    return response.json()


def guardar_generos(db, generos_tmdb):
    for g in generos_tmdb:
        if not db.get(Genre, g["id"]):
            db.add(Genre(genre_id=g["id"], name=g["name"]))
    db.commit()


def guardar_pelicula(db, movie_data):
    release_date = movie_data.get("release_date")
    if not release_date:
        return None

    try:
        release_year = int(release_date[:4])
    except ValueError:
        return None

    pelicula = db.get(Movie, movie_data["id"])
    if not pelicula:
        pelicula = Movie(
            movie_id=movie_data["id"],
            title=movie_data["title"],
            release_year=release_year,
        )
        db.add(pelicula)
        db.commit()
    return pelicula


def vincular_generos(db, pelicula, genre_ids):
    for genre_id in genre_ids:
        vinculo = db.get(MovieGenre, {"movie_id": pelicula.movie_id, "genre_id": genre_id})
        if not vinculo:
            db.add(MovieGenre(movie_id=pelicula.movie_id, genre_id=genre_id))
    db.commit()


def guardar_persona(db, person_id, full_name):
    persona = db.get(Person, person_id)
    if not persona:
        persona = Person(person_id=person_id, full_name=full_name)
        db.add(persona)
        db.commit()
    return persona


def guardar_credito(db, movie_id, person_id, role, character_name=None):
    existente = db.query(Credit).filter_by(movie_id=movie_id, person_id=person_id, role=role).first()
    if not existente:
        db.add(Credit(movie_id=movie_id, person_id=person_id, role=role, character_name=character_name))
        db.commit()


def procesar_creditos(db, pelicula):
    credits_data = get_movie_credits(pelicula.movie_id)

    cast_ordenado = sorted(credits_data["cast"], key=lambda c: c.get("order", 999))
    for actor in cast_ordenado[:MAX_CAST_PER_MOVIE]:
        persona = guardar_persona(db, actor["id"], actor["name"])
        guardar_credito(db, pelicula.movie_id, persona.person_id, "ACTOR", actor.get("character"))

    directores = [c for c in credits_data["crew"] if c["job"] == "Director"]
    for director in directores:
        persona = guardar_persona(db, director["id"], director["name"])
        guardar_credito(db, pelicula.movie_id, persona.person_id, "DIRECTOR")


db = SessionLocal()

generos_tmdb = get_genre_list()
guardar_generos(db, generos_tmdb)

total_procesadas = 0

for page in range(1, PAGES + 1):
    print(f"--- Página {page}/{PAGES} ---")
    peliculas = get_popular_movies_page(page)

    for movie_data in peliculas:
        pelicula = guardar_pelicula(db, movie_data)
        if pelicula is None:
            print(f"Saltando '{movie_data.get('title')}' (sin fecha válida)")
            continue
        vincular_generos(db, pelicula, movie_data["genre_ids"])
        procesar_creditos(db, pelicula)

        total_procesadas += 1
        print(f"[{total_procesadas}] {pelicula.title} ({pelicula.release_year})")

db.close()
print(f"Completado. {total_procesadas} películas procesadas.")