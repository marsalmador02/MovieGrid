"""Pydantic schemas for the grid game. Requests and responses for
GET /grid/new and POST /grid/guess."""

from pydantic import BaseModel, Field


class GridAxis(BaseModel):
    """A single row or column header in the grid. A person the player must connect to."""

    id: int = Field(description="TMDB person ID.")
    name: str = Field(description="Full name of the actor or director.")


class GridResponse(BaseModel):
    """Response for a newly generated grid."""

    grid_id: str = Field(description="UUID identifying this grid, required for subsequent guesses.")
    rows: list[GridAxis] = Field(description="The 3 row headers.")
    columns: list[GridAxis] = Field(description="The 3 column headers.")


class GuessRequest(BaseModel):
    """A player's attempt to fill one cell of the grid."""

    grid_id: str = Field(description="The grid this guess belongs to.")
    row_id: int = Field(description="TMDB person ID of the row being answered.")
    column_id: int = Field(description="TMDB person ID of the column being answered.")
    guess: str = Field(description="The name the player typed in.")


class GuessResponse(BaseModel):
    """Result of validating a guess."""

    correct: bool = Field(description="Whether the guess is a valid answer for this cell.")
    matched_name: str | None = Field(
        default=None, description="The canonical name of the matched person if correct. Otherwise null."
    )