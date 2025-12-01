from src.settings import *
from src.environment.obstacles import ObstacleManager
import pygame

class Env:
  def __init__(self, border):
    self.border = border

    # Create obstacle manager sized to the paper area
    w = border.rect.width
    h = border.rect.height

    self.obstacles = ObstacleManager(width=w, height=h)

    # Spawn obstacles
    self.obstacles.generate_static(4)
    #self.obstacles.generate_moving(3)

  def update(self, dt):
    self.obstacles.update(dt)

  def draw(self, screen):
    # Draw inside border
    sub_surface = screen.subsurface(self.border.rect)
    self.obstacles.draw(sub_surface)


class Border:
    def __init__(self):
        # Create a rectangle representing the paper
        self.rect = pygame.Rect(*PAPER_RECT)
        
    def draw(self, screen):
        # Draw the paper background
        pygame.draw.rect(screen, PAPER_COLOR, self.rect)
        # Draw the border lines (width of 3 pixels)
        pygame.draw.rect(screen, BORDER_COLOR, self.rect, 3)

    def is_inside(self, x, y):
        # Helper to check if a specific point is inside the paper
        return self.rect.collidepoint(x, y)