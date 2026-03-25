# Part of case-study #14
# Developers: Ponasenko.E, Limanova.E, Smorodina.A, Nazarenko.V
#


import ru_local as ru
import pygame
import sys
from grid_io import (
    create_empty_grid,
    random_grid,
    save_grid_to_file,
    set_cell,
    load_grid_from_file
)
from game_logic import next_generation
from display import (
    init_display,
    draw_grid,
    draw_ui,
    get_cell_from_mouse
)


#def handle_events(grid, running, speed, generation, rows, cols, cell_size):
def handle_events(grid: list[list[int]], running: bool, speed: float, generation: int, rows: int, 
                  cols: int, cell_size: int) -> tuple[list[list[int]], bool, float, int, bool]:
    """
    Handle all Pygame events.

    Args:
        grid: current game grid
        running: simulation running flag
        speed: simulation speed in seconds
        generation: current generation number
        rows: number of rows in grid
        cols: number of columns in grid
        cell_size: size of each cell in pixels

    Returns:
        tuple: (grid, running, speed, generation, should_quit)
    """
    should_quit = False
    new_grid = grid

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            should_quit = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = not running

            elif event.key == pygame.K_s and not running:
                new_grid = next_generation(grid)
                generation += 1

            elif event.key == pygame.K_r:
                new_grid = random_grid(rows, cols, 0.3)
                generation = 0
                running = False

            elif event.key == pygame.K_c:
                new_grid = create_empty_grid(rows, cols)
                generation = 0
                running = False

            elif event.key == pygame.K_l:
                try:
                    new_grid = load_grid_from_file("saved_grid.txt")
                    generation = 0
                    running = False
                    print(ru.LOAD_CONFIGURATION)
                except:
                    print(ru.FILE_NOT_SAVED)

            elif event.key == pygame.K_f:
                save_grid_to_file(grid, "saved_grid.txt")
                print(ru.SAVE_SUCCESS)

            elif event.key in (pygame.K_EQUALS, pygame.K_PLUS):
                speed = max(0.05, speed - 0.05)

            elif event.key == pygame.K_MINUS:
                speed = min(2.0, speed + 0.05)

            elif event.key == pygame.K_q:
                should_quit = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if running:
                running = False
                print(ru.DRAWING_PAUSE)

            if event.button == 1:
                cell = get_cell_from_mouse(event.pos, cell_size)
                if cell:
                    row, col = cell
                    set_cell(grid, row, col, 1)
                    new_grid = grid

            elif event.button == 3:
                cell = get_cell_from_mouse(event.pos, cell_size)
                if cell:
                    row, col = cell
                    set_cell(grid, row, col, 0)
                    new_grid = grid

    return new_grid, running, speed, generation, should_quit


def print_controls():
    """Print control instructions to console."""
    print("\n" + "=" * 50)
    print(ru.GAME_TITLE)
    print("=" * 50)
    print(ru.CONTROLS_HEADER)
    print(f"  {ru.SPACE_CONTROL}")
    print(f"  {ru.MANUAL_STEP}")
    print(f"  {ru.RANDOM_CONFIG}")
    print(f"  {ru.CLEAR_GRID}")
    print(f"  {ru.SAVE_GRID}")
    print(f"  {ru.SPEED_CONTROL}")
    print(f"  {ru.MOUSE_LEFT}")
    print(f"  {ru.MOUSE_RIGHT}")
    print(f"  {ru.QUIT_GAME}")
    print("=" * 50 + "\n")


def main():
    """Main function for Conway's Game of Life."""
    rows = 40
    cols = 40
    cell_size = 14
    speed = 0.1
    running = False
    generation = 0
    fps = 60

    try:
        pygame.init()
        print(ru.INIT_SUCCESS)
    except Exception as e:
        print(f"{ru.INIT_ERROR} {e}")
        print(ru.INSTALL_HINT)
        return

    grid = random_grid(rows, cols, 0.3)

    try:
        screen, clock = init_display(rows, cols, cell_size)
        print(ru.DISPLAY_SUCCESS)
    except Exception as e:
        print(f"{ru.DISPLAY_ERROR} {e}")
        pygame.quit()
        return

    print_controls()

    last_update_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()

        grid, running, speed, generation, should_quit = handle_events(
            grid, running, speed, generation, rows, cols, cell_size
        )

        if should_quit:
            break

        if running:
            time_since_last = (current_time - last_update_time) / 1000.0
            if time_since_last >= speed:
                grid = next_generation(grid)
                generation += 1
                last_update_time = current_time

        draw_grid(screen, grid, generation, speed)
        draw_ui(screen, generation, speed, running)
        pygame.display.flip()

        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()