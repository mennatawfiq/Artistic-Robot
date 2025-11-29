import pygame
import math
from src.settings import *

class Robot:
  
  def __init__(self):
    self.x = 50
    self.y = 50
    self.current_row = 0
    self.current_col = 0
    self.drawing = False
    self.pixel_size = PIXEL_SIZE  
    self.grid_spacing = 2 * PIXEL_SIZE 
    self.angle = 0  
    self.drawing_step = 20  
    self.completed_pixels = []  

  def get_pixel_center(self, row, col, img_arr):
    if row % 2 == 0:  
      actual_col = col
    else:  
      actual_col = img_arr.shape[1] - 1 - col
    
    start_x = WIDTH // 2 - self.pixel_size * (IMAGE_RESOLUTION - 2)
    start_y = HEIGHT // 2 - self.pixel_size * (IMAGE_RESOLUTION - 2)
    center_x = start_x + actual_col * self.grid_spacing
    center_y = start_y + row * self.grid_spacing
    return center_x, center_y

  def draw_robot(self, screen):
      pygame.draw.rect(screen, PURPLE, (self.x, self.y, ROBOT_SIZE, ROBOT_SIZE), 0, 25) 

  def draw_raster(self, screen, img_arr):
    if img_arr is None:
      font = pygame.font.SysFont('Serif', 24)
      text = font.render("Drag and drop an image here", True, BLACK)
      text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
      screen.blit(text, text_rect)
      return

    for px, py, color in self.completed_pixels:
      pygame.draw.circle(screen, color, (px, py), self.pixel_size, 3)

    # if we're finished, return
    total_pixels = img_arr.shape[0] * img_arr.shape[1]
    if len(self.completed_pixels) >= total_pixels:
      return
    
    # get pixel color and center
    if self.current_row % 2 == 0:  # even rows: left to right
      actual_col = self.current_col
    else:  # odd rows: right to left
      actual_col = img_arr.shape[1] - 1 - self.current_col
    color = tuple(img_arr[self.current_row][actual_col])
    center_x, center_y = self.get_pixel_center(self.current_row, self.current_col, img_arr)
    
    # calc robot position on the circle
    if self.angle < 360:
      rad = math.radians(self.angle - 90)  
      self.x = center_x + self.pixel_size * math.cos(rad) - ROBOT_SIZE // 2
      self.y = center_y + self.pixel_size * math.sin(rad) - ROBOT_SIZE // 2

      if self.angle > 0:
        points = []
        num_points = max(2, int(self.angle / 5))
        for i in range(num_points + 1):
          angle = -90 + (self.angle * i / num_points)
          rad = math.radians(angle)
          px = center_x + self.pixel_size * math.cos(rad)
          py = center_y + self.pixel_size * math.sin(rad)
          points.append((px, py))

        if len(points) > 1:
          pygame.draw.lines(screen, color, False, points, 3)

      self.angle += self.drawing_step
    else:
      self.completed_pixels.append((center_x, center_y, color))
      self.angle = 0
      
      self.current_col += 1
      if self.current_col >= img_arr.shape[1]:
        self.current_col = 0
        self.current_row += 1
    
    self.draw_robot(screen)


  def draw_vector(self, screen):
    pass

  def draw_text(self, screen):
    pass