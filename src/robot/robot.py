import pygame
from src.settings import *;

class Robot:
  
  def __init__(self):
    self.x = WIDTH // 2
    self.y = HEIGHT // 2
    self.speed = ROBOT_SPEED
    
  def move_to(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = (dx**2 + dy**2)**0.5
        if dist < self.speed:## move robot immediatley without interpolation
            self.x, self.y = target_x, target_y
        else:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed

  def draw(self, screen):
      pygame.draw.rect(screen, PURPLE, (self.x, self.y, ROBOT_SIZE, ROBOT_SIZE), 0, 30) 