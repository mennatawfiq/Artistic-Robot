import pygame


WIDTH, HEIGHT = 1000, 650

BUTTON_WIDTH = 300
BUTTON_HEIGHT = 60

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0) 
LIGHT_BLUE = (100, 100, 255)
PURPLE = (112, 57, 156)

ROBOT_SIZE = 25
ROBOT_SPEED = 6
ROBOT_ANGLE = 90

DRAWING_WIDTH = 3
IMAGE_RESOLUTION = 32
PIXEL_SIZE = 10

# Notebook/Border Settings
PAPER_COLOR = (240, 240, 240) # Off-white for the paper
BORDER_COLOR = (0, 0, 0)      # Black outline
PAPER_MARGIN = 50 
PAPER_RECT = pygame.Rect(
    PAPER_MARGIN,               # Left
    PAPER_MARGIN,               # Top
    WIDTH - (PAPER_MARGIN * 2), # Width
    HEIGHT - (PAPER_MARGIN * 2) # Height
)

LINE_SPACING = 90  # How far down to jump for a new line

MENU_BUTTONS = [
            {"text": "Raster Draw", "action": "raster"},
            {"text": "Vector Draw", "action": "vector"},
            {"text": "Write Text", "action": "text_menu"}
        ]

TEXT_BUTTONS = [
            {"text": "Single Robot", "action": "text_single"},
            {"text": "Cooperative Robots", "action": "text_cooperative"}
        ]