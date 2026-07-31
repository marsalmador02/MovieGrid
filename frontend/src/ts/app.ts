const API_BASE_URL = "http://localhost:8000/api/v1";

/** A single row or column header returned by the API. */
interface GridAxis {
  id: number;
  name: string;
}

/** Response shape for GET /grid/new. */
interface GridResponse {
  grid_id: string;
  rows: GridAxis[];
  columns: GridAxis[];
}

/** Response shape for POST /grid/guess. */
interface GuessResponse {
  correct: boolean;
  matched_name: string | null;
}

let currentGridId: string | null = null;

/**
 * Requests a newly generated grid from the backend.
 *
 * @returns The grid to render, including its `grid_id` for subsequent guesses.
 * @throws If the request fails or the backend returns a non-OK status.
 */
async function fetchNewGrid(): Promise<GridResponse> {
  const response = await fetch(`${API_BASE_URL}/grid/new`);
  if (!response.ok) {
    throw new Error(`Failed to fetch grid: ${response.status}`);
  }
  return response.json();
}

/**
 * Submits a guess and returns whether it's correct.
 *
 * @param rowId Person ID of the row being answered.
 * @param columnId Person ID of the column being answered.
 * @param guess The name the player typed.
 */
async function submitGuess(rowId: number, columnId: number, guess: string): Promise<GuessResponse> {
  const response = await fetch(`${API_BASE_URL}/grid/guess`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      grid_id: currentGridId,
      row_id: rowId,
      column_id: columnId,
      guess: guess,
    }),
  });
  if (!response.ok) {
    throw new Error(`Failed to submit guess: ${response.status}`);
  }
  return response.json();
}

/**
 * Creates a cell for the grid.
 *
 * @param rowId Person ID of the row.
 * @param columnId Person ID of the column.
 * @returns The created table cell.
 */
function createCell(rowId: number, columnId: number): HTMLTableCellElement {
  const td = document.createElement("td");

  const input = document.createElement("input");
  input.type = "text";
  input.placeholder = "Your guess...";

  input.addEventListener("keydown", async (event: KeyboardEvent) => {
    if (event.key !== "Enter") return;

    const guessText = input.value.trim();
    if (!guessText) return;

    input.disabled = true;
    const result = await submitGuess(rowId, columnId, guessText);

    if (result.correct) {
      td.textContent = result.matched_name;
      td.classList.add("correct");
      checkForCompletion();
    } else {
      td.classList.add("incorrect");
      input.disabled = false;
      input.value = "";
      input.placeholder = "Try again...";
    }
  });

  td.appendChild(input);
  return td;
}

/**
 * Renders the grid in the DOM.
 *
 * @param grid The grid data to render.
 */
function renderGrid(grid: GridResponse): void {
  const container = document.getElementById("grid-container")!;
  container.innerHTML = "";

  const table = document.createElement("table");

  const headerRow = document.createElement("tr");
  headerRow.appendChild(document.createElement("th"));
  for (const col of grid.columns) {
    const th = document.createElement("th");
    th.textContent = col.name;
    headerRow.appendChild(th);
  }
  table.appendChild(headerRow);

  for (const row of grid.rows) {
    const tr = document.createElement("tr");

    const th = document.createElement("th");
    th.textContent = row.name;
    tr.appendChild(th);

    for (const col of grid.columns) {
      tr.appendChild(createCell(row.id, col.id));
    }

    table.appendChild(tr);
  }

  container.appendChild(table);
}

/**
 * Checks if the game is completed.
 */
function checkForCompletion(): void {
  const remaining = document.querySelectorAll("#grid-container td:not(.correct)");
  if (remaining.length === 0) {
    setTimeout(() => alert("Congratulations! You completed the grid!"), 100);
  }
}

/**
 * Starts the game by fetching a new grid and rendering it.
 */
async function startGame(): Promise<void> {
  const grid = await fetchNewGrid();
  currentGridId = grid.grid_id;

  document.getElementById("welcome-screen")!.style.display = "none";
  const gridContainer = document.getElementById("grid-container")!;
  gridContainer.style.display = "block";

  renderGrid(grid);
}

document.getElementById("start-button")!.addEventListener("click", startGame);