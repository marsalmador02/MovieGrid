"""
Entry point for the REST API.

Creates the FastAPI application and defines the initial test endpoints.
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, get_db
from app.models import Movie
from app.schemas.movie import MovieRead
from app.api.v1.routes_grid import router as grid_router

app = FastAPI()

def get_db():
    """
    Get a database session.

    This function is used as a FastAPI dependency to inject a
    SQLAlchemy session into every endpoint that needs it.

    Yields:
        Session: Database session.

    Ensures the session is properly closed at the end of the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    """
    Welcome endpoint to verify the API is active.

    Returns:
        dict: API status message.
    """
    return {"message": "Movie Grid API is running"}


@app.get("/movies/", response_model=list[MovieRead])
def list_movies(db: Session = Depends(get_db)):
    """
    Return the first 10 movies from the database.
    """
    movies = db.query(Movie).limit(10).all()
    return movies

app.include_router(grid_router, prefix="/api/v1")