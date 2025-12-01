import pygame
from src.settings import *
from src.robot.robot import Robot
from src.menu import Menu, TextMenu
from src.utils.img_utils import image_to_rgb_array
from src.text.text_engine import TextEngine
from src.cooperative.cooperative_robot import CooperativeRobot
from src.environment.env import Border

class Game:
    def __init__(self):
        pygame.init()
        self.last_img_arr = None
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Autonomous Robotic Art Simulator")
        
        # Game states
        self.cur_state = "menu"
        self.menu = Menu(self.screen, MENU_BUTTONS)
        self.text_menu = TextMenu(self.screen)
        
        self.robot = Robot()
        
        # Back button
        self.back_button = pygame.Rect(5, 5, 30, 30)
        
        # Create border of the paper
        self.border = Border()
        
        # Main game loop
        self.clock = pygame.time.Clock()
        self.running = True

        # Vector mode
        self.draw_entered = False
        self.vector_drawing = []
        self.current_stroke = []

        # Text mode variables
        self.text_engine = TextEngine(spacing=10, scale=1.5)
        self.text_path = []
        self.text_index = 0
        self.user_text = ""
        self.text_entered = False
        self.input_active = True
        self.is_robot_initialized = False
        
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
                        self.last_img_arr = None
                        self.draw_entered = False
                        self.vector_drawing = []
                        self.current_stroke = []
                        if hasattr(self, 'vector_initialized'):
                            delattr(self, 'vector_initialized')
                        self.is_robot_initialized = False 
                        self.user_text = ""
                        self.text_entered = False
                        self.text_path = []
                        self.text_index = 0
                        print(f"Selected mode: {action}")
                
                # Handle text menu events
                elif self.cur_state == "text_menu":
                    action = self.text_menu.handle_event(event)
                    if action:
                        print(f"*** ACTION FROM TEXT MENU: '{action}' ***")
                        self.cur_state = action
                        self._reset_text_mode()
                
                # Handle back button
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
                            
                            self.text_path = self.text_engine.build_path(
                                self.user_text, 
                                PAPER_RECT,
                                LINE_SPACING
                            )
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
                self.menu.draw("Autonomous Robotic Art", "Select Drawing Mode")
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
            
    def wrap_text(self, text, font, max_width):
        """Splits a string into a list of lines that fit within max_width."""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            # Test if adding the next word exceeds width
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] < max_width:
                current_line.append(word)
            else:
                # If current line is not empty, save it and start new line
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Case for a single super long word
                    lines.append(word)
                    current_line = []
                    
        # Add the last remaining line
        if current_line:
            lines.append(' '.join(current_line))
        return lines

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
        self.border.draw(self.screen)
        self.draw_back_button()
        font = pygame.font.SysFont('Serif', 28)
        
        if not self.draw_entered:
            prompt_surface = font.render("Draw inside the frame, then press ENTER to see robot redraw it", True, BLACK)
            self.screen.blit(prompt_surface, (WIDTH // 2 - 400, 10))
            
            mouse_pressed = pygame.mouse.get_pressed()[0]
            if mouse_pressed:
                mouse_pos = pygame.mouse.get_pos()
                # check if mouse is inside the drawing frame
                if PAPER_RECT.collidepoint(mouse_pos):
                    if not hasattr(self, 'vector_drawing'):
                        self.vector_drawing = []
                        self.current_stroke = []
                    
                    self.current_stroke.append(mouse_pos)
            else:
                if hasattr(self, 'current_stroke') and len(self.current_stroke) > 0:
                    self.vector_drawing.append(self.current_stroke[:])
                    self.current_stroke = []
            
            # draw
            if hasattr(self, 'vector_drawing'):
                for stroke in self.vector_drawing:
                    if len(stroke) > 1:
                        pygame.draw.lines(self.screen, BLACK, False, stroke, 3)
                # draw stroke as user enters it
                if hasattr(self, 'current_stroke') and len(self.current_stroke) > 1:
                    pygame.draw.lines(self.screen, BLACK, False, self.current_stroke, 3)
            
            # check for ENTER key 
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN] and hasattr(self, 'vector_drawing') and len(self.vector_drawing) > 0:
                self.draw_entered = True
                # init robot for vector drawing
                if not hasattr(self, 'vector_initialized'):
                    self.robot.init_vector_drawing(self.vector_drawing)
                    self.vector_initialized = True
        else:
            self.robot.draw_vector(self.screen)

    def run_single_robot_mode(self):
        """Single robot mode"""
        self.screen.fill(WHITE)
        # Draw the border of the paper
        self.border.draw(self.screen)
        self.draw_back_button()

        # Reset Robot Position
        if not self.is_robot_initialized:
            self.reset_robot_to_start()
            self.is_robot_initialized = True
            
        if not self.text_entered:
            # Show typing prompt
            font = pygame.font.SysFont('Arial', 32)
            full_line = "Enter text and press Enter: " + self.user_text + "|"
            prompt_surface = font.render(full_line, True, BLACK)
            self.screen.blit(prompt_surface,(PAPER_RECT.left, PAPER_RECT.top - 40))
            #input_surface = font.render(self.user_text+ "|", True, BLUE)
            #self.screen.blit(input_surface,(PAPER_RECT.left + 20, PAPER_RECT.top + 20))
            self.robot.draw_robot(self.screen)
        else:
            if len(self.text_path) > 1:
                for i in range(1, self.text_index):
                    p1 = self.text_path[i-1]
                    p2 = self.text_path[i]
                    if p2[2] == 1: # If pen is DOWN
                        pygame.draw.line(self.screen, BLACK, (p1[0], p1[1]), (p2[0], p2[1]), 2)

            # Move Robot
            if self.text_index < len(self.text_path):
                target_x, target_y, pen = self.text_path[self.text_index]
                
                # Move robot towards target
                self.robot.move_to(target_x, target_y)
                
                # If robot arrived at point, go to next point
                if abs(self.robot.x - target_x) < 2 and abs(self.robot.y - target_y) < 2:
                    self.text_index += 1

            self.robot.draw_robot(self.screen)
            
    def reset_robot_to_start(self):
            start_x = PAPER_RECT.left + 20
            start_y = PAPER_RECT.top + 20
            
            if hasattr(self.robot, 'rect'):
                self.robot.rect.x = start_x
                self.robot.rect.y = start_y
            else:
                self.robot.x = start_x
                self.robot.y = start_y


