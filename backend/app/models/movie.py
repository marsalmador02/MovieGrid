"""Modelo ORM para la tabla 'movie'."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Movie(Base):
    __tablename__ = 'movie'

    movie_id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String, nullable=False)
    release_year = Column(Integer, nullable=False)

    credits = relationship("Credit", back_populates="movie", cascade="all, delete-orphan")
    genres = relationship("MovieGenre", back_populates="movie", cascade="all, delete-orphan")