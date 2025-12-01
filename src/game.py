import pygame
from src.settings import *
from src.robot.robot import Robot
from src.menu import Menu
from src.utils.img_utils import image_to_rgb_array
from src.text.text_engine import TextEngine
from src.environment.env import Border
from src.environment.env import Env
from src.environment.obstacles import ObstacleManager

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
        self.menu = Menu(self.screen)
        
        # Create a robot 
        self.robot = Robot()
        
        # Back button
        self.back_button = pygame.Rect(5, 5, 30, 30)
        
        # Create border of the paper
        self.border = Border()
        
        # Main game loop
        self.clock = pygame.time.Clock()
        self.running = True

        # Text mode variables
        self.text_engine = TextEngine(spacing=10, scale=1.5)
        self.text_path = []
        self.text_index = 0
        self.user_text = ""      
        self.text_entered = False
        self.input_active = True
        self.is_robot_initialized = False

        # Create obstacles
        self.env = Env(self.border)
        
    def run(self):
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.DROPFILE and self.cur_state == "raster":
                    img_path = event.file
                    self.last_img_arr = image_to_rgb_array(img_path, IMAGE_RESOLUTION) 
                elif event.type == pygame.DROPFILE and self.cur_state == "vector":
                    img_path = event.file
                    self.last_img_arr = image_to_rgb_array(img_path, IMAGE_RESOLUTION) 
                
                if self.cur_state == "menu":
                    action = self.menu.handle_event(event)
                    if action:
                        self.last_state = self.cur_state
                        self.cur_state = action
                        self.is_robot_initialized = False 
                        self.user_text = ""
                        self.text_entered = False
                        self.text_path = []
                        self.text_index = 0
                
                # Handle back button
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_button.collidepoint(event.pos):
                        self.cur_state = "menu"
                        self.last_img_arr = None 
                        
                        self.user_text = "" 
                        self.text_entered = False
                        self.text_path = []
                        self.text_index = 0

                        #REGENERATE RANDOM OBSTACLES
                        w = self.env.border.rect.width
                        h = self.env.border.rect.height

                        self.env.obstacles = ObstacleManager(width=w, height=h)
                        self.env.obstacles.generate_static(4) 

                # Text mode typing
                if self.cur_state == "text" and not self.text_entered:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.text_entered = True
                            self.input_active = False
                            
                            # --- CRITICAL UPDATE HERE ---
                            # Pass self.env to build_path so it can see obstacles!
                            self.text_path = self.text_engine.build_path(
                                self.user_text, 
                                PAPER_RECT,
                                LINE_SPACING,
                                self.env 
                            )
                            # -----------------------------
                            
                            self.text_index = 0
                            if self.text_path:
                                self.robot.x, self.robot.y, _ = self.text_path[0]
                                self.robot.rect.topleft = (self.robot.x, self.robot.y)
                        elif event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            self.user_text += event.unicode
            
            # Update and draw
            if self.cur_state == "menu":
                self.menu.draw()
            elif self.cur_state == "raster":
                self.run_raster_mode()
            elif self.cur_state == "vector":
                self.run_vector_mode()
            elif self.cur_state == "text":
                self.run_text_mode()
            
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
        # self.border.draw(self.screen)
        # self.env.update(1/60)
        # self.env.draw(self.screen)
        self.robot.draw_raster(self.screen, self.last_img_arr)

    def run_vector_mode(self):
        self.screen.fill(WHITE)
        self.draw_back_button()
        # self.border.draw(self.screen)
        # self.env.update(1/60)
        # self.env.draw(self.screen)
        self.robot.draw_robot(self.screen)
        self.robot.draw_vector(self.screen)

    def run_text_mode(self):
        self.screen.fill(WHITE)
        self.border.draw(self.screen)
        self.env.update(1/60)
        self.env.draw(self.screen)
        self.draw_back_button()

        if not self.is_robot_initialized:
            self.reset_robot_to_start()
            self.is_robot_initialized = True
            
        if not self.text_entered:
            font = pygame.font.SysFont('Arial', 32)
            full_line = "Enter text: " + self.user_text + "|"
            prompt_surface = font.render(full_line, True, BLACK)
            self.screen.blit(prompt_surface,(PAPER_RECT.left, PAPER_RECT.top - 40))
            self.robot.draw_robot(self.screen)
        else:
            # --- DRAW INK HISTORY ---
            if len(self.text_path) > 1:
                for i in range(1, self.text_index):
                    p1 = self.text_path[i-1]
                    p2 = self.text_path[i]
                    
                    # ONLY DRAW IF PEN IS DOWN (p2[2] == 1)
                    if p2[2] == 1: 
                        pygame.draw.line(self.screen, BLACK, (p1[0], p1[1]), (p2[0], p2[1]), 2)

            # Move Robot
            if self.text_index < len(self.text_path):
                target_x, target_y, pen = self.text_path[self.text_index]
                
                # Move robot
                reached = self.robot.move_to(target_x, target_y, self.env)
                
                if reached:
                    self.text_index += 1
            
            else:
                parking_x = WIDTH - 50
                parking_y = HEIGHT - 50
                self.robot.move_to(parking_x, parking_y, self.env)
            
            self.robot.draw_robot(self.screen)

    def reset_robot_to_start(self):
            start_x = PAPER_RECT.left + 20
            start_y = PAPER_RECT.top + 20
            self.robot.x = start_x
            self.robot.y = start_y
            self.robot.rect.topleft = (start_x, start_y)