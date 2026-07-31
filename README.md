# MovieGrid

A daily puzzle game inspired by [Immaculate Grid](https://www.immaculategrid.com/), built around movies, actors and directors instead of sports. Players fill a 3x3 grid where each row and column represents an actor or director, and each cell must be answered with a person who worked with both.

This is a personal portfolio project built to learn and demonstrate a full-stack Python/TypeScript workflow: REST API design, relational data modeling, third-party API ingestion, constraint-based procedural generation and a vanilla TypeScript frontend.

## Table of contents

- [Tech stack](#tech-stack)
- [Setup](#setup)
- [API reference](#api-reference)

## Tech stack

**Backend**
- Python, FastAPI
- SQLAlchemy 2.0 (ORM) + Alembic (migrations)
- PostgreSQL
- httpx (TMDB API client)
- Pydantic (schemas/validation)

**Frontend**
- TypeScript (vanilla, no framework)
- Compiled with `tsc` to ES2020 modules
- Served in development with `browser-sync`

**External data source**
- [TMDB API](https://www.themoviedb.org/documentation/api): movies, cast and crew credits

## Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
# create a .env with DATABASE_URL and TMDB_API_KEY
alembic upgrade head
uvicorn app.main:app --reload

# Data ingestion (run once against an empty database)
python -m ingestion.prueba_tmdb

# Frontend
cd frontend
npm install
npm run dev   # compiles TypeScript in watch mode + serves on localhost:5000
```

The backend expects a `.env` file with:

```
DATABASE_URL=postgresql://user:password@localhost:5432/movie_grid
TMDB_API_KEY=your_tmdb_read_access_token
```

## API reference

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/v1/grid/new` | Generates a new grid and returns `grid_id`, `rows` and `columns`. |
| `POST` | `/api/v1/grid/guess` | Validates a guess for a given `grid_id`, `row_id`, `column_id`. Returns `{correct, matched_name}`. |

Interactive documentation is available at `/docs` (Swagger UI) once the backend is running.

**Example: `GET /api/v1/grid/new`**
```json
{
  "grid_id": "33f01ab4-5e89-491d-8b80-713ff3846e09",
  "rows": [
    {"id": 28782, "name": "Monica Bellucci"},
    {"id": 380, "name": "Robert De Niro"},
    {"id": 58873, "name": "Dan Fogler"}
  ],
  "columns": [
    {"id": 21007, "name": "Jonah Hill"},
    {"id": 15009, "name": "Justin Theroux"},
    {"id": 17401, "name": "Stephen Root"}
  ]
}
```

**Example: `POST /api/v1/grid/guess`**
```json
// Request
{
  "grid_id": "33f01ab4-5e89-491d-8b80-713ff3846e09",
  "row_id": 380,
  "column_id": 15009,
  "guess": "Leonardo DiCaprio"
}

// Response
{
  "correct": true,
  "matched_name": "Leonardo DiCaprio"
}
```