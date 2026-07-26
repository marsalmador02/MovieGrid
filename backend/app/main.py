"""Punto de entrada de la API REST.

Crea la aplicación FastAPI y define los endpoints iniciales de prueba.
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models import Movie
from app.schemas.movie import MovieRead

app = FastAPI()

# Dependencia para inyección de sesión de base de datos
def get_db():
    """Obtiene una sesión de la base de datos.

    Esta función se usa como dependencia de FastAPI para inyectar una
    sesión SQLAlchemy en cada endpoint que la necesite.

    Yields:
        Session: Sesión de base de datos.

    Asegura que la sesión se cierre correctamente al finalizar la petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.get("/")
def root():
    """Endpoint de bienvenida para verificar que la API está activa.

    Returns:
        dict: Mensaje de estado de la API.
    """
    return {"message": "Movie Grid API is running"}

@app.get("/movies/", response_model=list[MovieRead])
def list_movies(db: Session = Depends(get_db)):
    """Retorna las primeras 10 películas de la base de datos."""
    movies = db.query(Movie).limit(10).all()
    return movies