import pygame
from src.settings import *;

class Robot:
  
  def __init__(self):
    self.x = WIDTH // 2
    self.y = HEIGHT // 2

  def draw(self, screen):
      pygame.draw.rect(screen, PURPLE, (self.x, self.y, ROBOT_SIZE, ROBOT_SIZE), 0, 30) 