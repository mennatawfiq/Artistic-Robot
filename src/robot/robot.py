import pygame
import math
from collections import deque
from src.settings import * # NEED THIS

class Robot:
  def __init__(self):
    self.pixel_size = PIXEL_SIZE  
    self.grid_spacing = 2 * PIXEL_SIZE 
    self.angle = 0  
    self.drawing_step = 40 
    self.completed_pixels = []  
    self.x = WIDTH // 2
    self.y = HEIGHT // 2
    self.speed = ROBOT_SPEED
    
    self.rect = pygame.Rect(self.x, self.y, ROBOT_SIZE, ROBOT_SIZE)
    
    self.current_path = [] 
    self.last_target_x = None
    self.last_target_y = None
    
    # Stuck variables
    self.stuck_timer = 0
    self.last_pos = (self.x, self.y)

  def check_collision_global(self, x, y, radius, env):
      """
      Helper to check collision converting Global -> Local
      """
      local_x = x - PAPER_RECT.left
      local_y = y - PAPER_RECT.top
      return env.obstacles.collides(local_x, local_y, radius)

  def move_to(self, target_x, target_y, env=None):
    self.rect.topleft = (int(self.x), int(self.y))

    dist_to_goal = math.hypot(target_x - self.x, target_y - self.y)
    if dist_to_goal < self.speed * 1.5:
        self.x = target_x
        self.y = target_y
        self.stuck_timer = 0 
        self.current_path = []
        return True

    # Stuck Detection
    moved_dist = math.hypot(self.x - self.last_pos[0], self.y - self.last_pos[1])
    self.last_pos = (self.x, self.y)
    if moved_dist < 0.5: self.stuck_timer += 1
    else: self.stuck_timer = max(0, self.stuck_timer - 1)

    # Ghost Mode
    if self.stuck_timer > 30:
        dir_x = (target_x - self.x) / (dist_to_goal + 0.01)
        dir_y = (target_y - self.y) / (dist_to_goal + 0.01)
        self.x += dir_x * (self.speed * 0.8)
        self.y += dir_y * (self.speed * 0.8)
        if self.stuck_timer > 90:
            self.x = target_x
            self.y = target_y
            self.stuck_timer = 0
            return True
        return False

    # Normal Movement
    if self.last_target_x is None or abs(target_x - self.last_target_x) > 1 or abs(target_y - self.last_target_y) > 1:
        self.current_path = []
        self.last_target_x = target_x
        self.last_target_y = target_y

    if self.current_path:
        wp_x, wp_y = self.current_path[0]
        d_wp = math.hypot(wp_x - self.x, wp_y - self.y)
        if d_wp < self.speed * 2:
            self.current_path.pop(0)
            if not self.current_path: return False 
        else:
            self.x += ((wp_x - self.x) / d_wp) * self.speed
            self.y += ((wp_y - self.y) / d_wp) * self.speed
            return False

    if env:
        # Use Corrected Global Check
        if self.is_line_clear(self.x, self.y, target_x, target_y, env):
             self.move_direct(target_x, target_y)
             return False
        
        if not self.current_path:
            self.current_path = self.find_path_bfs(target_x, target_y, env)
            if self.current_path: return False 
            
        self.move_slide_fallback(target_x, target_y, env)
        return False
    else:
        self.move_direct(target_x, target_y)
        return False

  def is_line_clear(self, start_x, start_y, end_x, end_y, env):
      dist = math.hypot(end_x - start_x, end_y - start_y)
      if dist == 0: return True
      steps = int(dist / 15) 
      for i in range(steps + 1):
          t = i / max(steps, 1)
          check_x = start_x + (end_x - start_x) * t
          check_y = start_y + (end_y - start_y) * t
          # USE GLOBAL CHECK
          if self.check_collision_global(check_x + ROBOT_SIZE/2, check_y + ROBOT_SIZE/2, ROBOT_SIZE * 0.7, env):
              return False
      return True

  def find_path_bfs(self, target_x, target_y, env):
      grid_size = 20 
      def to_grid(x, y): return int(x // grid_size), int(y // grid_size)
      def to_world(gx, gy): return gx * grid_size, gy * grid_size
      
      start_node = to_grid(self.x, self.y)
      end_node = to_grid(target_x, target_y)
      
      queue = deque([start_node])
      came_from = {start_node: None}
      max_col = WIDTH // grid_size + 2
      max_row = HEIGHT // grid_size + 2
      found = False
      
      while queue:
          current = queue.popleft()
          if current == end_node:
              found = True
              break
          cx, cy = current
          neighbors = [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1), (cx+1, cy+1), (cx-1, cy-1), (cx+1, cy-1), (cx-1, cy+1)]
          for nx, ny in neighbors:
              if 0 <= nx < max_col and 0 <= ny < max_row:
                  if (nx, ny) not in came_from:
                      wx, wy = to_world(nx, ny)
                      
                      # USE GLOBAL CHECK
                      is_blocked = self.check_collision_global(wx + grid_size/2, wy + grid_size/2, ROBOT_SIZE * 0.6, env)
                      
                      if (nx, ny) == end_node: is_blocked = False 
                      if not is_blocked:
                          came_from[(nx, ny)] = current
                          queue.append((nx, ny))
      if found:
          path = []
          curr = end_node
          while curr != start_node:
              wx, wy = to_world(curr[0], curr[1])
              path.append((wx + grid_size/2, wy + grid_size/2))
              curr = came_from[curr]
          path.reverse()
          return path
      return []

  def move_direct(self, tx, ty):
      dx = tx - self.x
      dy = ty - self.y
      d = math.hypot(dx, dy)
      if d == 0: return
      self.x += (dx/d) * self.speed
      self.y += (dy/d) * self.speed

  def move_slide_fallback(self, target_x, target_y, env):
      dx = target_x - self.x
      dy = target_y - self.y
      dist = math.hypot(dx, dy)
      if dist == 0: return True
      
      vel_x = (dx/dist) * self.speed
      vel_y = (dy/dist) * self.speed

      self.x += vel_x
      self.rect.x = int(self.x)
      # GLOBAL CHECK
      if env and self.check_collision_global(self.rect.centerx, self.rect.centery, ROBOT_SIZE/2.2, env):
          self.x -= vel_x 
          self.rect.x = int(self.x)

      self.y += vel_y
      self.rect.y = int(self.y)
      # GLOBAL CHECK
      if env and self.check_collision_global(self.rect.centerx, self.rect.centery, ROBOT_SIZE/2.2, env):
          self.y -= vel_y 
          self.rect.y = int(self.y)
      return False

  # Drawing (unchanged)
  def get_pixel_center(self, row, col, img_arr):
    if row % 2 == 0: actual_col = col
    else: actual_col = img_arr.shape[1] - 1 - col
    start_x = WIDTH // 2 - self.pixel_size * (IMAGE_RESOLUTION - 2)
    start_y = HEIGHT // 2 - self.pixel_size * (IMAGE_RESOLUTION - 1)
    center_x = start_x + actual_col * self.grid_spacing
    center_y = start_y + row * self.grid_spacing
    return center_x, center_y

  def draw_robot(self, screen):
      self.rect.topleft = (int(self.x), int(self.y))
      pygame.draw.rect(screen, PURPLE, self.rect, 0, 5)

  def draw_raster(self, screen, img_arr):
      # ... (Original code, no changes needed) ...
      pass
  
  def draw_vector(self, screen): pass