import pygame
from src.settings import *
from src.robot.robot import Robot
from src.menu import Menu, TextMenu
from src.utils.img_utils import image_to_rgb_array
from src.text.text_engine import TextEngine
from src.cooperative.cooperative_robot import CooperativeRobot

class Game:
    def __init__(self):
        pygame.init()
        self.last_img_arr = None
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Autonomous Robotic Art Simulator")
        
        # Game states
        self.cur_state = "menu"
        self.menu = Menu(self.screen)
        self.text_menu = TextMenu(self.screen)
        
        self.robot = Robot()
        self.back_button = pygame.Rect(5, 5, 30, 30)  
        self.clock = pygame.time.Clock()
        self.running = True

        self.text_engine = TextEngine(spacing=20, scale=2)
        self.text_path = []
        self.text_index = 0
        self.user_text = ""
        self.text_entered = False
        self.input_active = True
        
        # Cooperative mode
        self.cooperative_robot = CooperativeRobot(self.screen, self.text_engine)
        
        print("=== DEBUG: Game initialized ===")
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.DROPFILE and self.cur_state == "raster":
                    img_path = event.file
                    print("Dropped file:", img_path)
                    self.last_img_arr = image_to_rgb_array(img_path, IMAGE_RESOLUTION)
                    print("Array shape:", self.last_img_arr.shape)
                elif event.type == pygame.DROPFILE and self.cur_state == "vector":
                    img_path = event.file
                    print("Dropped file:", img_path)
                    self.last_img_arr = image_to_rgb_array(img_path, IMAGE_RESOLUTION)
                    print("Array shape:", self.last_img_arr.shape)
                
                # Handle menu events
                if self.cur_state == "menu":
                    action = self.menu.handle_event(event)
                    if action:
                        print(f"*** ACTION FROM MENU: '{action}' ***")
                        self.cur_state = action
                
                # Handle text menu events
                elif self.cur_state == "text_menu":
                    action = self.text_menu.handle_event(event)
                    if action:
                        print(f"*** ACTION FROM TEXT MENU: '{action}' ***")
                        self.cur_state = action
                        self._reset_text_mode()
                
                # Handle back button
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_button.collidepoint(event.pos):
                        print("*** BACK BUTTON CLICKED ***")
                        if self.cur_state in ["text_single", "text_cooperative"]:
                            self.cur_state = "text_menu"
                        elif self.cur_state == "text_menu":
                            self.cur_state = "menu"
                        else:
                            self.cur_state = "menu"
                        self._reset_text_mode()
                
                # Handle cooperative mode typing
                if self.cur_state == "text_cooperative":
                    if self.cooperative_robot.handle_typing(event):
                        print("Cooperative: Text entry complete")
                
                # Handle single mode typing
                elif self.cur_state == "text_single" and not self.text_entered:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.text_entered = True
                            self.input_active = False
                            self.text_path = self.text_engine.build_path(self.user_text, 50, 300)
                            self.text_index = 0
                            if self.text_path:
                                self.robot.x, self.robot.y, _ = self.text_path[0]
                        elif event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            self.user_text += event.unicode
            
            # Update game state
            if self.cur_state == "text_cooperative":
                self.cooperative_robot.update()
            
            # Draw based on current state
            if self.cur_state == "menu":
                self.menu.draw()
            elif self.cur_state == "text_menu":
                self.text_menu.draw()
                self.draw_back_button()
            elif self.cur_state == "raster":
                self.run_raster_mode()
            elif self.cur_state == "vector":
                self.run_vector_mode()
            elif self.cur_state == "text_single":
                self.run_single_robot_mode()
            elif self.cur_state == "text_cooperative":
                self.cooperative_robot.draw(self.draw_back_button)
            
            pygame.display.flip()
            self.clock.tick(60)

    def _reset_text_mode(self):
        """Reset all text mode variables"""
        self.user_text = ""
        self.text_entered = False
        self.text_path = []
        self.text_index = 0
        self.cooperative_robot.reset()

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

    def run_single_robot_mode(self):
        """Single robot mode"""
        self.screen.fill(WHITE)
        self.draw_back_button()
        
        font = pygame.font.SysFont('Arial', 24)
        mode_surface = font.render("Mode: Single Robot", True, BLACK)
        self.screen.blit(mode_surface, (WIDTH - 200, 20))
        
        font = pygame.font.SysFont('Arial', 32) 
        if not self.text_entered:
            prompt_surface = font.render("Enter text and press Enter:", True, BLACK)
            self.screen.blit(prompt_surface, (50, 20))
            input_surface = font.render(self.user_text, True, BLACK)
            self.screen.blit(input_surface, (50, 60))
        else:
            # Draw completed lines
            for i in range(1, self.text_index):
                if i < len(self.text_path):
                    x1, y1, pen1 = self.text_path[i-1]
                    x2, y2, pen2 = self.text_path[i]
                    if pen2:
                        pygame.draw.line(self.screen, BLACK, (x1, y1), (x2, y2), DRAWING_WIDTH)

            # Move robot
            if self.text_index < len(self.text_path):
                target_x, target_y, pen = self.text_path[self.text_index]
                self.robot.move_to(target_x, target_y)

                if pen and self.text_index > 0:
                    prev_x, prev_y, _ = self.text_path[self.text_index-1]
                    pygame.draw.line(self.screen, BLACK, (prev_x, prev_y), (self.robot.x, self.robot.y), DRAWING_WIDTH)

                if (round(self.robot.x), round(self.robot.y)) == (round(target_x), round(target_y)):
                    self.text_index += 1

            self.robot.draw_robot(self.screen)