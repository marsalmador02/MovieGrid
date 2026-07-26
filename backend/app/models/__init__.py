"""Inicialización del paquete de modelos ORM.

Exporta los modelos para facilitar su importación desde otros módulos.
"""

from app.models.movie import Movie
from app.models.person import Person
from app.models.genre import Genre
from app.models.movie_genre import MovieGenre
from app.models.credit import Credit

__all__ = ["Movie", "Person", "Genre", "MovieGenre", "Credit"]