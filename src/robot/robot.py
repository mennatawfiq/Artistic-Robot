import pygame
from src.settings import *;

class Robot:
  
  def __init__(self):
    self.x = 50
    self.y = 50

  def manual_control(self):
      keys = pygame.key.get_pressed()
      new_x, new_y = self.x, self.y
      if keys[pygame.K_LEFT]:
          new_x -= ROBOT_SPEED
      if keys[pygame.K_RIGHT]:
          new_x += ROBOT_SPEED
      if keys[pygame.K_UP]:
          new_y -= ROBOT_SPEED
      if keys[pygame.K_DOWN]:
          new_y += ROBOT_SPEED
      if new_x > 0 and new_x < WIDTH - ROBOT_SIZE:
          self.x = new_x
      if new_y > 0 and new_y < HEIGHT - ROBOT_SIZE:
          self.y = new_y

  def draw(self, screen):
      pygame.draw.rect(screen, BLUE, (self.x, self.y, ROBOT_SIZE, ROBOT_SIZE)) 