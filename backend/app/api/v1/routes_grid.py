from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Person
from app.schemas.grid import GridResponse, GridAxis, GuessRequest, GuessResponse
from app.services.grid_generator import create_and_store_grid, active_grids

router = APIRouter(prefix="/grid", tags=["grid"])


@router.get("/new", response_model=GridResponse)
def new_grid(db: Session = Depends(get_db)):
    grid_id = create_and_store_grid(db)
    grid_data = active_grids[grid_id]

    all_ids = grid_data["rows"] + grid_data["columns"]
    names = {p.person_id: p.full_name for p in db.query(Person).filter(Person.person_id.in_(all_ids))}

    return GridResponse(
        grid_id=grid_id,
        rows=[GridAxis(id=pid, name=names[pid]) for pid in grid_data["rows"]],
        columns=[GridAxis(id=pid, name=names[pid]) for pid in grid_data["columns"]],
    )


@router.post("/guess", response_model=GuessResponse)
def submit_guess(guess_request: GuessRequest, db: Session = Depends(get_db)):
    grid_data = active_grids.get(guess_request.grid_id)
    if grid_data is None:
        raise HTTPException(status_code=404, detail="Grid not found or expired")

    valid_person_ids = grid_data["intersections"].get((guess_request.row_id, guess_request.column_id))
    if valid_person_ids is None:
        raise HTTPException(status_code=400, detail="Invalid row/column for this grid")

    matched_person = (
        db.query(Person)
        .filter(Person.person_id.in_(valid_person_ids))
        .filter(Person.full_name.ilike(guess_request.guess.strip()))
        .first()
    )

    if matched_person:
        return GuessResponse(correct=True, matched_name=matched_person.full_name)
    return GuessResponse(correct=False)