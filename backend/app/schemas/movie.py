"""Esquemas Pydantic para la entidad Movie. Necesario para la validación de datos y la
serialización/deserialización de objetos."""

from pydantic import BaseModel, ConfigDict

class MovieRead(BaseModel):
    """Esquema para leer una película (respuesta de la API)."""
    movie_id: int
    title: str
    release_year: int

    # Permite convertir objetos SQLAlchemy a Pydantic automáticamente
    model_config = ConfigDict(from_attributes=True)