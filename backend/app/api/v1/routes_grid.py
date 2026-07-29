from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Person
from app.schemas.grid import GridResponse, GridAxis
from app.services.grid_generator import generate_people_only_grid, get_person_pool

router = APIRouter(prefix="/grid", tags=["grid"])


@router.get("/new", response_model=GridResponse)
def new_grid(db: Session = Depends(get_db)):
    pool = get_person_pool(db, min_credits=5)
    rows, columns, _ = generate_people_only_grid(db, pool)

    all_ids = rows + columns
    names = {p.person_id: p.full_name for p in db.query(Person).filter(Person.person_id.in_(all_ids))}

    return GridResponse(
        rows=[GridAxis(id=pid, name=names[pid]) for pid in rows],
        columns=[GridAxis(id=pid, name=names[pid]) for pid in columns],
    )