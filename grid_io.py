import random


def create_empty_grid(rows: int, cols: int) -> list[list[int]]:
    """
    Creates an empty grid (all cells dead)

    Args:
        rows: number of rows
        cols: number of columns

    Returns:
        2D list filled with zeros
    """
    return [[0 for _ in range(cols)] for _ in range(rows)]


def random_grid(rows: int, cols: int, prob: float = 0.5) -> list[list[int]]:
    """
    Fills the grid with random values with given probability of life

    Args:
        rows: number of rows
        cols: number of columns
        prob: probability that a cell will be alive (from 0 to 1)

    Returns:
        2D list with random 0 and 1 values
    """
    grid = create_empty_grid(rows, cols)
    for i in range(rows):
        for j in range(cols):
            if random.random() < prob:
                grid[i][j] = 1
    return grid


def load_grid_from_file(filename: str) -> list[list[int]]:
    """
    Reads grid from a text file

    File format:
    - First line: two numbers - number of rows and columns
    - Following lines: grid rows as strings of 0 and 1 (no spaces)

    Args:
        filename: name of the file to read

    Returns:
        2D list with cell states
    """
    with open(filename, 'r') as f:
        rows, cols = map(int, f.readline().split())

        grid = create_empty_grid(rows, cols)

        for i in range(rows):
            line = f.readline().strip()
            for j in range(min(cols, len(line))):
                grid[i][j] = int(line[j])

    return grid


def save_grid_to_file(grid: list[list[int]], filename: str) -> None:
    """
    Saves grid to a file

    File format:
    - First line: number of rows and columns
    - Following lines: grid rows as strings of 0 and 1

    Args:
        grid: grid to save
        filename: name of the file to save to
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    with open(filename, 'w') as f:
        f.write(f"{rows} {cols}\n")

        for i in range(rows):
            line = ''.join(str(grid[i][j]) for j in range(cols))
            f.write(line + '\n')


def set_cell(grid: list[list[int]], row: int, col: int, value: int) -> None:
    """
    Sets the state of a specific cell

    Args:
        grid: grid
        row: row index
        col: column index
        value: new value (0 or 1)
    """
    if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
        grid[row][col] = value

