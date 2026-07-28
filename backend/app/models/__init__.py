"""
Initializing the ORM model package.

Exports the models to make it easier to import them from other modules.
"""

from app.models.movie import Movie
from app.models.person import Person
from app.models.genre import Genre
from app.models.movie_genre import MovieGenre
from app.models.credit import Credit

__all__ = ["Movie", "Person", "Genre", "MovieGenre", "Credit"]