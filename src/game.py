import pygame
from src.settings import *
from src.robot.robot import Robot
from src.menu import Menu
from src.utils.img_utils import image_to_rgb_array
from src.text.text_engine import TextEngine

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

        # Text mode variables
        self.text_engine = TextEngine(spacing=20)
        self.text_path = []
        self.text_index = 0
        self.user_text = ""      # text typed by user
        self.text_entered = False
        self.input_active = True
        
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
                    # Optional: reset text mode 
                    self.user_text = "" 
                    self.text_entered = False
                    self.text_path = []
                    self.text_index = 0
                # Text mode typing
                if self.cur_state == "text" and not self.text_entered:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.text_entered = True
                            self.input_active = False
                            # Build path
                            self.text_engine = TextEngine(spacing=20, scale=2)
                            self.text_path = self.text_engine.build_path(self.user_text, 50, 300)
                            self.text_index = 0
                            if self.text_path:
                                self.robot.x, self.robot.y, _ = self.text_path[0]
                        elif event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            self.user_text += event.unicode
            
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

    #  Text mode 
    def run_text_mode(self):
        self.screen.fill(WHITE)
        self.draw_back_button()
        font = pygame.font.SysFont('Arial', 32) 
        if not self.text_entered:
            # Show typing prompt
            prompt_surface = font.render("Enter text and press Enter:", True, BLACK)
            self.screen.blit(prompt_surface, (50, 20))
            input_surface = font.render(self.user_text, True, BLACK)
            self.screen.blit(input_surface, (50, 60))
        else:
            # Draw lines
            for i in range(1, self.text_index):
                x1, y1, pen1 = self.text_path[i-1]
                x2, y2, pen2 = self.text_path[i]
                if pen2:
                    pygame.draw.line(self.screen, BLACK, (x1, y1), (x2, y2), DRAWING_WIDTH)

            # Move robot to next point
            if self.text_index < len(self.text_path):
                target_x, target_y, pen = self.text_path[self.text_index]
                self.robot.move_to(target_x, target_y)

                # Draw line if pen is down
                if pen and self.text_index > 0:
                    prev_x, prev_y, _ = self.text_path[self.text_index-1]
                    pygame.draw.line(self.screen, BLACK, (prev_x, prev_y), (self.robot.x, self.robot.y), DRAWING_WIDTH)

                # Check if robot reached target
                if (round(self.robot.x), round(self.robot.y)) == (round(target_x), round(target_y)):
                    self.text_index += 1

            # Draw robot
            self.robot.draw_robot(self.screen)

