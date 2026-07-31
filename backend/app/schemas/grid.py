from pydantic import BaseModel


class GridAxis(BaseModel):
    id: int
    name: str


class GridResponse(BaseModel):
    grid_id: str
    rows: list[GridAxis]
    columns: list[GridAxis]


class GuessRequest(BaseModel):
    grid_id: str
    row_id: int
    column_id: int
    guess: str


class GuessResponse(BaseModel):
    correct: bool
    matched_name: str | None = None