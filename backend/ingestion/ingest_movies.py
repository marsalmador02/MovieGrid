"""
This script ingests popular movies from the TMDB API into the local database. It fetches movie details, genres and credits for each movie and saves them in the corresponding tables.
"""
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


def save_genres(db, tmdb_genres):
    for g in tmdb_genres:
        if not db.get(Genre, g["id"]):
            db.add(Genre(genre_id=g["id"], name=g["name"]))
    db.commit()


def save_movie(db, movie_data):
    release_date = movie_data.get("release_date")
    if not release_date:
        return None

    try:
        release_year = int(release_date[:4])
    except ValueError:
        return None

    movie = db.get(Movie, movie_data["id"])
    if not movie:
        movie = Movie(
            movie_id=movie_data["id"],
            title=movie_data["title"],
            release_year=release_year,
        )
        db.add(movie)
        db.commit()
    return movie


def link_genres(db, movie, genre_ids):
    for genre_id in genre_ids:
        existing_link = db.get(MovieGenre, {"movie_id": movie.movie_id, "genre_id": genre_id})
        if not existing_link:
            db.add(MovieGenre(movie_id=movie.movie_id, genre_id=genre_id))
    db.commit()


def save_person(db, person_id, full_name):
    person = db.get(Person, person_id)
    if not person:
        person = Person(person_id=person_id, full_name=full_name)
        db.add(person)
        db.commit()
    return person


def save_credit(db, movie_id, person_id, role, character_name=None):
    existing = db.query(Credit).filter_by(movie_id=movie_id, person_id=person_id, role=role).first()
    if not existing:
        db.add(Credit(movie_id=movie_id, person_id=person_id, role=role, character_name=character_name))
        db.commit()


def process_credits(db, movie):
    credits_data = get_movie_credits(movie.movie_id)

    sorted_cast = sorted(credits_data["cast"], key=lambda c: c.get("order", 999))
    for actor in sorted_cast[:MAX_CAST_PER_MOVIE]:
        person = save_person(db, actor["id"], actor["name"])
        save_credit(db, movie.movie_id, person.person_id, "ACTOR", actor.get("character"))

    directors = [c for c in credits_data["crew"] if c["job"] == "Director"]
    for director in directors:
        person = save_person(db, director["id"], director["name"])
        save_credit(db, movie.movie_id, person.person_id, "DIRECTOR")


db = SessionLocal()

tmdb_genres = get_genre_list()
save_genres(db, tmdb_genres)

total_processed = 0

for page in range(1, PAGES + 1):
    print(f"--- Page {page}/{PAGES} ---")
    movies = get_popular_movies_page(page)

    for movie_data in movies:
        movie = save_movie(db, movie_data)
        if movie is None:
            print(f"Skipping '{movie_data.get('title')}' (no valid release date)")
            continue
        link_genres(db, movie, movie_data["genre_ids"])
        process_credits(db, movie)

        total_processed += 1
        print(f"[{total_processed}] {movie.title} ({movie.release_year})")

db.close()
print(f"Completed. {total_processed} movies processed.")