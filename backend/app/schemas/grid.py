from pydantic import BaseModel

class GridAxis(BaseModel):
    id: int
    name: str


class GridResponse(BaseModel):
    rows: list[GridAxis]
    columns: list[GridAxis]