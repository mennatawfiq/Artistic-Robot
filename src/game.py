import pygame
from src.settings import *
from src.robot.robot import Robot
from src.menu import Menu
from src.utils.img_utils import image_to_rgb_array

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        self.last_img_arr = None
        
        # Create the screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Autonomous Robotic Art Simulator")
        
        # Game states
        self.cur_state = "menu"  # menu, raster, vector, text
        # self.last_state = None
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
                elif event.type == pygame.DROPFILE and self.cur_state == "raster":
                    img_path = event.file
                    print("Dropped file:", img_path)
                    self.last_img_arr = image_to_rgb_array(img_path, IMAGE_RESOLUTION) # <<<<<< draw this image pixel by pixel 
                    print("Array shape:", self.last_img_arr.shape)
                    # self.last_state = None
                elif event.type == pygame.DROPFILE and self.cur_state == "vector":
                    img_path = event.file
                    print("Dropped file:", img_path)
                    self.last_img_arr = image_to_rgb_array(img_path, IMAGE_RESOLUTION) # <<<<<< draw this image with vectors
                    print("Array shape:", self.last_img_arr.shape)
                
                if self.cur_state == "menu":
                    action = self.menu.handle_event(event)
                    if action:
                        self.last_state = self.cur_state
                        self.cur_state = action
                        print(f"Selected mode: {action}")
                
                # Handle back button in all modes except menu
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_button.collidepoint(event.pos):
                        self.cur_state = "menu"
                        self.last_img_arr = None # **remove this to conserve last drawing
            
            # Update and draw based on current state
            # if self.last_state != self.cur_state:
            if self.cur_state == "menu":
                self.menu.draw()
            elif self.cur_state == "raster":
                self.run_raster_mode()
            elif self.cur_state == "vector":
                self.run_vector_mode()
            elif self.cur_state == "text":
                self.run_text_mode()
            # self.last_state = self.cur_state
            
            pygame.display.flip()
            self.clock.tick(60)

    def draw_back_button(self):
      pygame.draw.circle(self.screen, GRAY, self.back_button.center, self.back_button.width // 2)
      pygame.draw.circle(self.screen, BLACK, self.back_button.center, self.back_button.width // 2, 2)

      font = pygame.font.SysFont('Serif', 28, bold=True)
      text = font.render("←", True, BLACK)  
      text_rect = text.get_rect(center=self.back_button.center)
      self.screen.blit(text, text_rect)

    def run_raster_mode(self):
        self.screen.fill(WHITE)
        self.draw_back_button()
        self.robot.draw_raster(self.screen, self.last_img_arr)

    def run_vector_mode(self):
        self.screen.fill(WHITE)
        self.draw_back_button()
        self.robot.draw_robot(self.screen)
        self.robot.draw_vector(self.screen)

    def run_text_mode(self):
        self.screen.fill(WHITE)
        self.draw_back_button()
        self.robot.draw_robot(self.screen)
        self.robot.draw_text(self.screen)
