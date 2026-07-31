from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Genre(Base):
    """A TMDB movie genre."""
    __tablename__ = "genre"
    
    genre_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(100), nullable=False, unique=True)

    movies = relationship("MovieGenre", back_populates="genre")