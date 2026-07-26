"""Modelo ORM para la tabla 'movie_genre'."""

from sqlalchemy import Column, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.core.database import Base

class MovieGenre(Base):
    __tablename__ = "movie_genre"

    movie_id = Column(Integer, ForeignKey("movie.movie_id", ondelete="CASCADE"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genre.genre_id", ondelete="CASCADE"), primary_key=True)

    movie = relationship("Movie", back_populates="genres")
    genre = relationship("Genre", back_populates="movies")

    __table_args__ = (
        Index("idx_movie_genre_genre_id", "genre_id"),
    )