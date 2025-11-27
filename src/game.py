import pygame
from src.settings import *
from src.robot.robot import Robot
from src.menu import Menu

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Create the screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Autonomous Robotic Art Simulator")
        
        # Game states
        self.state = "menu"  # menu, upload, text
        self.menu = Menu(self.screen)
        
        # Create a robot 
        self.robot = Robot()
        
        # Back button
        self.back_button = pygame.Rect(5, 5, 30, 30)  

        # Main game loop
        self.clock = pygame.time.Clock()
        self.running = True
        
    def run(self):
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.state == "menu":
                    action = self.menu.handle_event(event)
                    if action:
                        self.state = action
                        print(f"Selected mode: {action}")
                
                # Handle back button in all modes except menu
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_button.collidepoint(event.pos):
                        self.state = "menu"
            
            # Update and draw based on current state
            if self.state == "menu":
                self.menu.draw()
            elif self.state == "upload":
                self.run_upload_mode()
            elif self.state == "text":
                self.run_text_mode()
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def draw_back_button(self):
      # Draw circular button
      pygame.draw.circle(self.screen, GRAY, self.back_button.center, self.back_button.width // 2)
      pygame.draw.circle(self.screen, BLACK, self.back_button.center, self.back_button.width // 2, 2)
      
      # Draw back arrow icon (←) instead of text
      font = pygame.font.SysFont('Arial', 24, bold=True)
      text = font.render("←", True, BLACK)  # Using left arrow symbol
      text_rect = text.get_rect(center=self.back_button.center)
      self.screen.blit(text, text_rect)
    
    def run_upload_mode(self):
        self.screen.fill(WHITE)
        self.draw_back_button()
        self.robot.draw(self.screen)
    
    def run_text_mode(self):
        self.screen.fill(WHITE)
        self.draw_back_button()
        self.robot.draw(self.screen)
        