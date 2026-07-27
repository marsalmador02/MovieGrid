import httpx
from app.core.config import settings
from app.core.database import SessionLocal
from app.models import Movie, Genre, MovieGenre, Person, Credit

TMDB_BASE_URL = "https://api.themoviedb.org/3"
MAX_CAST_PER_MOVIE = 10


def get_popular_movies_page1():
    headers = {"Authorization": f"Bearer {settings.TMDB_API_KEY}"}
    response = httpx.get(f"{TMDB_BASE_URL}/movie/popular", headers=headers)
    response.raise_for_status()
    return response.json()["results"]


def get_movie_credits(movie_id):
    headers = {"Authorization": f"Bearer {settings.TMDB_API_KEY}"}
    response = httpx.get(f"{TMDB_BASE_URL}/movie/{movie_id}/credits", headers=headers)
    response.raise_for_status()
    return response.json()


def guardar_persona(db, person_id, full_name):
    persona = db.get(Person, person_id)
    if not persona:
        persona = Person(person_id=person_id, full_name=full_name)
        db.add(persona)
        db.commit()
    return persona


def guardar_credito(db, movie_id, person_id, role, character_name=None):
    existente = (
        db.query(Credit) # query? 
        .filter_by(movie_id=movie_id, person_id=person_id, role=role)
        .first()
    )
    if not existente:
        db.add(Credit(movie_id=movie_id, person_id=person_id, role=role, character_name=character_name))
        db.commit()


db = SessionLocal()

peliculas = get_popular_movies_page1()
primera = peliculas[0]

pelicula = db.get(Movie, primera["id"])
print(f"Trayendo créditos de: {pelicula.title}")

credits_data = get_movie_credits(primera["id"])

# 1. Reparto: los primeros N actores, ordenados por 'order' (orden de aparición en los créditos)
cast_ordenado = sorted(credits_data["cast"], key=lambda c: c.get("order"))
top_cast = cast_ordenado[:MAX_CAST_PER_MOVIE]

for actor in top_cast:
    persona = guardar_persona(db, actor["id"], actor["name"])
    guardar_credito(db, pelicula.movie_id, persona.person_id, "ACTOR", actor.get("character"))
    print(f"  Actor guardado: {actor['name']} como {actor.get('character')}")

# 2. Director: filtramos el crew por job == "Director"
directores = [c for c in credits_data["crew"] if c["job"] == "Director"]

for director in directores:
    persona = guardar_persona(db, director["id"], director["name"])
    guardar_credito(db, pelicula.movie_id, persona.person_id, "DIRECTOR")
    print(f"  Director guardado: {director['name']}")

db.close()
print("Créditos guardados.")