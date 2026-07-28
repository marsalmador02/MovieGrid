import random
from sqlalchemy import func
from app.core.database import SessionLocal
from app.models import Credit, Person


def get_person_pool(db, min_credits=5):
    """Returns person IDs with at least N credits, to ensure they have
    enough connections to be a good grid axis."""
    result = (
        db.query(Credit.person_id, func.count(Credit.movie_id).label("num_credits"))
        .group_by(Credit.person_id)
        .having(func.count(Credit.movie_id) >= min_credits)
        .all()
    )
    return [r[0] for r in result]


def get_connected_people_to_person(db, person_id):
    """Returns people who have worked with person_id (share at least one movie)."""
    person_movies = (
        db.query(Credit.movie_id)
        .filter(Credit.person_id == person_id)
        .scalar_subquery()
    )
    result = (
        db.query(Credit.person_id)
        .filter(Credit.movie_id.in_(person_movies))
        .filter(Credit.person_id != person_id)
        .distinct()
        .all()
    )
    return [r[0] for r in result]


def generate_people_only_grid(db, pool, max_attempts=200):
    """Picks 3 people for rows and 3 for columns, checking that
    all 9 intersections have at least one valid answer."""

    for attempt in range(max_attempts):
        selected = random.sample(pool, 6)
        rows, columns = selected[:3], selected[3:]

        connected = {
            person_id: get_connected_people_to_person(db, person_id)
            for person_id in selected
        }

        valid_grid = True
        grid_intersections = {}

        for row in rows:
            for col in columns:
                intersection = set(connected[row]).intersection(connected[col])
                if not intersection:
                    valid_grid = False
                    break
                grid_intersections[(row, col)] = intersection
            if not valid_grid:
                break

        if valid_grid:
            print(f"Valid grid found on attempt {attempt + 1}")
            return rows, columns, grid_intersections

    raise RuntimeError(f"No valid grid found after {max_attempts} attempts")


db = SessionLocal()

pool = get_person_pool(db, min_credits=5)
print(f"Candidate pool: {len(pool)} people")

rows, columns, intersections = generate_people_only_grid(db, pool)

names = {p.person_id: p.full_name for p in db.query(Person).filter(Person.person_id.in_(rows + columns))}

print("\nRows:   ", [names[r] for r in rows])
print("Columns:", [names[c] for c in columns])

db.close()