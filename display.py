import pygame
import ru_local as ru

_display_state = {
    'screen': None,
    'clock': None,
    'rows': 0,
    'cols': 0,
    'cell_size': 20,
    'window_width': 0,
    'window_height': 0,
    'grid_height': 0,
    'ui_height': 80,
    'font_small': None,
    'font_medium': None,
    'colors': {
        'alive': (255, 255, 255),
        'dead': (0, 0, 0),
        'grid': (40, 40, 40),
        'text': (0, 255, 0),
        'ui_background': (30, 30, 30)
    }
}


def init_display(rows: int, cols: int, cell_size: int = 14) -> tuple[pygame.Surface, pygame.time.Clock]:
    """
    The function calculates window dimensions based on grid size and UI panel height,
    initializes Pygame, creates the window, and sets up fonts for text rendering.

    Args:
        rows: Number of rows in the grid
        cols: Number of columns in the grid
        cell_size: Size of each cell in pixels (default: 20)

    Returns:
        Tuple containing (screen_surface, clock_object) for use in main loop
    """
    global _display_state
    
    _display_state['rows'] = rows
    _display_state['cols'] = cols
    _display_state['cell_size'] = cell_size
    
    _display_state['grid_height'] = rows * cell_size
    _display_state['window_width'] = cols * cell_size
    _display_state['window_height'] = _display_state['grid_height'] + _display_state['ui_height']
    
    pygame.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode((
        _display_state['window_width'], 
        _display_state['window_height']
    ))
    pygame.display.set_caption("Conway's Game of Life")
    
    _display_state['font_small'] = pygame.font.Font(None, 24)
    _display_state['font_medium'] = pygame.font.Font(None, 32)
    
    clock = pygame.time.Clock()
    
    _display_state['screen'] = screen
    _display_state['clock'] = clock
    
    return screen, clock


def draw_grid(screen: pygame.Surface, grid: list[list[int]], generation: int, speed: float) -> None:
    """
    Render the complete game grid with living/dead cells and grid lines.
    
    Args:
        screen: Pygame surface to draw on
        grid: 2D list representing cell states (0 = dead, 1 = alive)
        generation: Current generation number (displayed in UI)
        speed: Current simulation speed in seconds (displayed in UI)
    """
    rows = _display_state['rows']
    cols = _display_state['cols']
    cell_size = _display_state['cell_size']
    colors = _display_state['colors']
    grid_height = _display_state['grid_height']
    
    grid_rect = pygame.Rect(0, 0, cols * cell_size, rows * cell_size)
    pygame.draw.rect(screen, colors['dead'], grid_rect)
    
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 1:
                rect = pygame.Rect(
                    col * cell_size,
                    row * cell_size,
                    cell_size - 1,
                    cell_size - 1
                )
                pygame.draw.rect(screen, colors['alive'], rect)
    
    for x in range(0, cols * cell_size + 1, cell_size):
        pygame.draw.line(
            screen, 
            colors['grid'],
            (x, 0), 
            (x, grid_height),
            1
        )
    
    for y in range(0, rows * cell_size + 1, cell_size):
        pygame.draw.line(
            screen,
            colors['grid'],
            (0, y),
            (cols * cell_size, y),
            1
        )



def get_cell_from_mouse(pos: tuple[int, int], cell_size: int) -> tuple[int, int] | None:
    """
    Convert mouse coordinates to grid cell indices.

    Args:
        pos: Mouse position as (x, y) tuple
        cell_size: Size of each cell in pixels
    
    Returns:
        Tuple (row, col) if mouse is over the grid, None if outside grid area
    """
    x, y = pos
    
    if x < 0 or x >= _display_state['cols'] * cell_size or y < 0 or y >= _display_state['rows'] * cell_size:
        return None
    
    col = x // cell_size
    row = y // cell_size
    
    if 0 <= row < _display_state['rows'] and 0 <= col < _display_state['cols']:
        return (row, col)
    return None


def draw_ui(screen: pygame.Surface, generation: int, speed: float, running: bool) -> None:
    """
    Render the user interface panel with game information and controls.
    
    Args:
        screen: Pygame surface to draw on
        generation: Current generation number to display
        speed: Current simulation speed to display
        running: Boolean indicating if simulation is running (True) or paused (False)
    """
    colors = _display_state['colors']
    font_small = _display_state['font_small']
    font_medium = _display_state['font_medium']
    
    grid_height = _display_state['grid_height']
    window_width = _display_state['window_width']
    ui_height = _display_state['ui_height']
    
    ui_rect = pygame.Rect(0, grid_height, window_width, ui_height)
    pygame.draw.rect(screen, colors['ui_background'], ui_rect)
    
    gen_text = font_medium.render(f"{ru.GENERATION_LABEL} {generation}", True, colors['text'])
    screen.blit(gen_text, (10, grid_height + 5))
    
    speed_text = font_small.render(f"{ru.SPEED_LABEL} {speed:.1f}s", True, colors['text'])
    screen.blit(speed_text, (180, grid_height + 10))

    status = ru.SIM_RUNNING if running else ru.SIM_PAUSED
    status_color = (0, 255, 0) if running else (255, 255, 0)
    status_text = font_small.render(status, True, status_color)
    screen.blit(status_text, (320, grid_height + 10))
    
    hints1_text = font_small.render(ru.HINTS_LINE1, True, (150, 150, 150))
    screen.blit(hints1_text, (10, grid_height + 35))

    hints2_text = font_small.render(ru.HINTS_LINE2, True, (150, 150, 150))
    screen.blit(hints2_text, (10, grid_height + 55))


def handle_color_scheme(alive_color: tuple = None, dead_color: tuple = None, grid_color: tuple = None) -> None:
    """
    Change the color scheme of the display.
    
    Args:
        alive_color: RGB tuple for living cells
        dead_color: RGB tuple for dead cells background
        grid_color: RGB tuple for grid lines
    """
    if alive_color is not None:
        _display_state['colors']['alive'] = alive_color
    if dead_color is not None:
        _display_state['colors']['dead'] = dead_color
    if grid_color is not None:
        _display_state['colors']['grid'] = grid_color