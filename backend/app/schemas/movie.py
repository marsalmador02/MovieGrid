"""
Pydantic schemas for the Movie entity. Required for data validation and the
serialization/deserialization of objects.
"""

from pydantic import BaseModel, ConfigDict

class MovieRead(BaseModel):
    """
    Schema for reading a movie (API response).
    """
    movie_id: int
    title: str
    release_year: int

    model_config = ConfigDict(from_attributes=True)