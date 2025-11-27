import pygame
from src.settings import *;
from src.robot.robot import Robot

class Game:

    def __init__(self):
        
        # Initialize Pygame
        pygame.init()

        # Create the screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Robot Navigation Sim")

        # Create a robot
        self.robot = Robot()

        # Main game loop
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(WHITE)
            self.robot.manual_control()
            self.robot.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
