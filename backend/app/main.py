"""
Entry point for the REST API.

Creates the FastAPI application, configures CORS and registers all routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes_grid import router as grid_router

app = FastAPI(
    title="MovieGrid API",
    description="Backend for MovieGrid, a movie-trivia grid game.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", summary="Health check")
def root():
    """Simple endpoint to verify the API is running."""
    return {"message": "Movie Grid API is running"}


app.include_router(grid_router, prefix="/api/v1")