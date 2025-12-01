import pygame
import random
import math

# BASE CLASS
class Obstacle:
  def draw(self, surface):
    raise NotImplementedError

  def update(self, dt):
    pass

  def collides(self, x, y):
    raise NotImplementedError

# RECTANGLE OBSTACLE (STATIC)
class RectObstacle(Obstacle):
  def __init__(self, x, y, w, h, color=(200, 50, 50)):
      self.rect = pygame.Rect(x, y, w, h)
      self.color = color

  def draw(self, surface):
      pygame.draw.rect(surface, self.color, self.rect)

  def collides(self, x, y):
      return self.rect.collidepoint(x, y)

  def collides_circle(self, cx, cy, r):
      # Find closest point on rect to circle center
      closest_x = max(self.rect.left, min(cx, self.rect.right))
      closest_y = max(self.rect.top, min(cy, self.rect.bottom))
      dx = cx - closest_x
      dy = cy - closest_y
      return dx*dx + dy*dy <= r*r
# CIRCLE OBSTACLE (STATIC)
class CircleObstacle(Obstacle):
    def __init__(self, x, y, radius, color=(50, 150, 200)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def collides(self, x, y):
        dx, dy = x - self.x, y - self.y
        return dx*dx + dy*dy <= self.radius*self.radius

    def collides_circle(self, cx, cy, r):
        dx = cx - self.x
        dy = cy - self.y
        # collide if distance <= (obstacle_radius + robot_radius)
        return dx*dx + dy*dy <= (self.radius + r) * (self.radius + r)

# # MOVING RECTANGLE OBSTACLE
# class MovingRectObstacle(Obstacle):
#     def __init__(self, x, y, w, h, vx, vy, bounds, color=(180, 40, 200)):
#         self.rect = pygame.Rect(x, y, w, h)
#         self.vx = vx
#         self.vy = vy
#         self.bounds = bounds  # (width, height)
#         self.color = color

#     def update(self, dt):
#         self.rect.x += self.vx * dt
#         self.rect.y += self.vy * dt

#         if self.rect.left < 0 or self.rect.right > self.bounds[0]:
#             self.vx *= -1
#         if self.rect.top < 0 or self.rect.bottom > self.bounds[1]:
#             self.vy *= -1

#     def draw(self, surface):
#         pygame.draw.rect(surface, self.color, self.rect)

#     def collides(self, x, y):
#         return self.rect.collidepoint(x, y)

#     def collides_circle(self, cx, cy, r):
#         closest_x = max(self.rect.left, min(cx, self.rect.right))
#         closest_y = max(self.rect.top, min(cy, self.rect.bottom))
#         dx = cx - closest_x
#         dy = cy - closest_y
#         return dx*dx + dy*dy <= r*r

# # MOVING CIRCLE OBSTACLE
# class MovingCircleObstacle(Obstacle):
#     def __init__(self, x, y, radius, vx, vy, bounds, color=(255, 120, 0)):
#         self.x = x
#         self.y = y
#         self.radius = radius
#         self.vx = vx
#         self.vy = vy
#         self.bounds = bounds  # (width, height)
#         self.color = color

#     def update(self, dt):
#         self.x += self.vx * dt
#         self.y += self.vy * dt

#         if self.x - self.radius < 0 or self.x + self.radius > self.bounds[0]:
#             self.vx *= -1
#         if self.y - self.radius < 0 or self.y + self.radius > self.bounds[1]:
#             self.vy *= -1

#     def draw(self, surface):
#         pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

#     def collides(self, x, y):
#         dx = x - self.x
#         dy = y - self.y
#         return dx*dx + dy*dy <= self.radius*self.radius

#     def collides_circle(self, cx, cy, r):
#         dx = cx - self.x
#         dy = cy - self.y
#         return dx*dx + dy*dy <= (self.radius + r) * (self.radius + r)

# OBSTACLE MANAGER (YOUR MAIN CLASS)
class ObstacleManager:
  def __init__(self, width=800, height=600):
    self.width = width
    self.height = height
    self.obstacles = []

  # RANDOM GENERATION
  def generate_static(self, count=5):
    for _ in range(count):
      if random.choice([True, False]):  
        w, h = random.randint(40, 120), random.randint(40, 120)
        x = random.randint(0, self.width - w)
        y = random.randint(0, self.height - h)
        self.obstacles.append(RectObstacle(x, y, w, h))
      else:
        radius = random.randint(20, 60)
        x = random.randint(radius, self.width - radius)
        y = random.randint(radius, self.height - radius)
        self.obstacles.append(CircleObstacle(x, y, radius))

  # def generate_moving(self, count=3):
  #   for _ in range(count):
  #     if random.choice([True, False]):
  #       radius = random.randint(20, 50)
  #       x = random.randint(radius, self.width - radius)
  #       y = random.randint(radius, self.height - radius)
  #       vx, vy = random.uniform(-120, 120), random.uniform(-120, 120)
  #       self.obstacles.append(
  #           MovingCircleObstacle(x, y, radius, vx, vy, (self.width, self.height))
  #       )
  #     else:
  #       w, h = random.randint(40, 100), random.randint(40, 100)
  #       x = random.randint(0, self.width - w)
  #       y = random.randint(0, self.height - h)
  #       vx, vy = random.uniform(-120, 120), random.uniform(-120, 120)
  #       self.obstacles.append(
  #           MovingRectObstacle(x, y, w, h, vx, vy, (self.width, self.height))
  #       )

  def update(self, dt):
    for o in self.obstacles:
      o.update(dt)

  def draw(self, surface):
    for o in self.obstacles:
      o.draw(surface)

  def collides(self, cx, cy, r=0):
    """
    Test whether a circle (center cx,cy radius r) collides with any obstacle.
    If r==0 it will fall back to point tests via collides(x,y) for backwards compatibility.
    """
    if r <= 0:
        return any(o.collides(cx, cy) for o in self.obstacles)

    for o in self.obstacles:
        # use collides_circle if available; otherwise fallback to point test of center
        if hasattr(o, "collides_circle"):
            if o.collides_circle(cx, cy, r):
                return True
        else:
            if o.collides(cx, cy):
                return True
    return False