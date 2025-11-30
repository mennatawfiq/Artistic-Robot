from src.settings import *
import pygame

class Env:

  def __init(self):
    pass

  def draw(self):
    pass


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