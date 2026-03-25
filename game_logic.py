from typing import List, Tuple

Grid = List[List[int]]


def count_live_neighbors(grid: Grid, row: int, col: int, boundary: str = "open") -> int:
    """
    Count live neighbors for a cell.
    
    Args:
        grid: Current state grid
        row: Row index
        col: Column index
        boundary: "open" or "torus" (should be imported from config)
    
    Returns:
        Number of live neighbors (0-8)
    """
    height = len(grid)
    width = len(grid[0])
    count = 0

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue

            if boundary == "torus":
                nr = (row + dr) % height
                nc = (col + dc) % width
                count += grid[nr][nc]
            else:  
                nr, nc = row + dr, col + dc
                if 0 <= nr < height and 0 <= nc < width:
                    count += grid[nr][nc]

    return count


def next_generation(grid: Grid, boundary: str = "open") -> Grid:
    """
    Compute next generation of the Game of Life.
    
    Args:
        grid: Current generation
        boundary: "open" or "torus" (from config)
    
    Returns:
        New generation grid (original unchanged)
    """
    height = len(grid)
    width = len(grid[0])
    
    new_grid = [[0 for _ in range(width)] for _ in range(height)]
    
    for row in range(height):
        for col in range(width):
            neighbors = count_live_neighbors(grid, row, col, boundary)
            
            if grid[row][col] == 1:
                if neighbors == 2 or neighbors == 3:
                    new_grid[row][col] = 1
            else:
                if neighbors == 3:
                    new_grid[row][col] = 1
                    
    return new_grid


def apply_boundary_condition(grid: Grid, row: int, col: int, boundary: str = "torus") -> Tuple[int, int]:
    """
    Transform coordinates according to boundary conditions.
    
    Args:
        grid: Grid for dimensions
        row: Original row
        col: Original column
        boundary: "torus" only (open returns original)
    
    Returns:
        Transformed coordinates
    """
    if boundary == "torus":
        return (row % len(grid), col % len(grid[0]))
    return (row, col)