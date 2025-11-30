import pygame
import os
import sys

# Settings
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
IMAGE_RESOLUTION = (100, 100)
DRAWING_WIDTH = 2

# Mock classes for missing dependencies
class Robot:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
    
    def draw_raster(self, screen, img_arr):
        font = pygame.font.SysFont('Arial', 24)
        text = font.render("Raster Mode - Drop an image file", True, BLACK)
        screen.blit(text, (50, 100))
    
    def draw_robot(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 10)
    
    def draw_vector(self, screen):
        font = pygame.font.SysFont('Arial', 24)
        text = font.render("Vector Mode - Drop an image file", True, BLACK)
        screen.blit(text, (50, 100))
    
    def move_to(self, x, y):
        dx = x - self.x
        dy = y - self.y
        distance = (dx**2 + dy**2)**0.5
        if distance > 1:
            self.x += dx * 0.1
            self.y += dy * 0.1

class TextEngine:
    def __init__(self, spacing=20, scale=2):
        self.spacing = spacing
        self.scale = scale
    
    def build_path(self, text, start_x, start_y):
        path = []
        x, y = start_x, start_y
        
        for char in text:
            path.append((x, y, True))
            path.append((x + 20, y, True))
            path.append((x + 20, y, False))
            x += 30
        
        return path

def image_to_rgb_array(img_path, resolution):
    print(f"Mock: Processing image {img_path}")
    return None

# Menu Classes
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Serif', 32)
        self.title_font = pygame.font.SysFont('Serif', 44, bold=True)
        self.buttons = [
            {"text": "Raster Draw", "rect": pygame.Rect(0, 0, 300, 60), "action": "raster"},
            {"text": "Vector Draw", "rect": pygame.Rect(0, 0, 300, 60), "action": "vector"},
            {"text": "Enter Text", "rect": pygame.Rect(0, 0, 300, 60), "action": "text_menu"}  # CHANGED to text_menu
        ]
        self.setup_buttons()

    def setup_buttons(self):
        total_height = len(self.buttons) * 60  
        start_y = (HEIGHT - total_height) // 2
        
        for i, button in enumerate(self.buttons):
            button["rect"].centerx = WIDTH // 2
            button["rect"].y = start_y + i * 70
    
    def draw(self):
        self.screen.fill(WHITE)
        
        title = self.title_font.render("Autonomous Robotic Art", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font.render("Select Drawing Mode", True, BLACK)
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, 160))
        self.screen.blit(subtitle, subtitle_rect)
        
        for button in self.buttons:
            pygame.draw.rect(self.screen, PURPLE, button["rect"], border_radius=10)
            pygame.draw.rect(self.screen, BLACK, button["rect"], 2, border_radius=10)
            
            text = self.font.render(button["text"], True, WHITE)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    print(f"Menu: Button '{button['text']}' clicked, action: {button['action']}")
                    return button["action"]
        return None

class TextMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Serif', 32)
        self.title_font = pygame.font.SysFont('Serif', 44, bold=True)
        self.buttons = [
            {"text": "Single Robot", "rect": pygame.Rect(0, 0, 300, 60), "action": "text_single"},
            {"text": "Cooperative Robots", "rect": pygame.Rect(0, 0, 300, 60), "action": "text_cooperative"}
        ]
        self.setup_buttons()

    def setup_buttons(self):
        total_height = len(self.buttons) * 60  
        start_y = (HEIGHT - total_height) // 2
        
        for i, button in enumerate(self.buttons):
            button["rect"].centerx = WIDTH // 2
            button["rect"].y = start_y + i * 70
    
    def draw(self):
        self.screen.fill(WHITE)
        
        title = self.title_font.render("Text Drawing Mode", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font.render("Select Robot Type", True, BLACK)
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, 160))
        self.screen.blit(subtitle, subtitle_rect)
        
        for button in self.buttons:
            pygame.draw.rect(self.screen, PURPLE, button["rect"], border_radius=10)
            pygame.draw.rect(self.screen, BLACK, button["rect"], 2, border_radius=10)
            
            text = self.font.render(button["text"], True, WHITE)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    print(f"TextMenu: Button '{button['text']}' clicked, action: {button['action']}")
                    return button["action"]
        return None

# Main Game Class
class Game:
    def __init__(self):
        pygame.init()
        self.last_img_arr = None
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Autonomous Robotic Art Simulator")
        
        self.cur_state = "menu"
        self.menu = Menu(self.screen)
        self.text_menu = TextMenu(self.screen)
        
        self.robot = Robot()
        self.back_button = pygame.Rect(5, 5, 30, 30)
        self.clock = pygame.time.Clock()
        self.running = True

        self.text_engine = TextEngine(spacing=20)
        self.text_path = []
        self.text_index = 0
        self.user_text = ""
        self.text_entered = False
        self.input_active = True
        
    def run(self):
        while self.running:
            print(f"DEBUG - Current state: {self.cur_state}")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.DROPFILE:
                    print(f"File dropped: {event.file}")
                
                if self.cur_state == "menu":
                    action = self.menu.handle_event(event)
                    if action:
                        self.cur_state = action
                        print(f"MAIN: Changing state to: {action}")
                
                elif self.cur_state == "text_menu":
                    action = self.text_menu.handle_event(event)
                    if action:
                        self.cur_state = action
                        print(f"MAIN: Changing state to: {action}")
                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    print(f"MAIN: Mouse click at: {event.pos}")
                    if self.back_button.collidepoint(event.pos):
                        print("MAIN: Back button clicked!")
                        if self.cur_state in ["text_single", "text_cooperative"]:
                            self.cur_state = "text_menu"
                            print("MAIN: Back to text_menu")
                        else:
                            self.cur_state = "menu"
                            print("MAIN: Back to main menu")
                        
                        if self.cur_state != "text_single" and self.cur_state != "text_cooperative":
                            self.user_text = "" 
                            self.text_entered = False
                            self.text_path = []
                            self.text_index = 0
                            print("MAIN: Text variables reset")
                
                if self.cur_state in ["text_single", "text_cooperative"] and not self.text_entered:
                    if event.type == pygame.KEYDOWN:
                        print(f"MAIN: Key pressed: {event.key}")
                        if event.key == pygame.K_RETURN:
                            self.text_entered = True
                            self.input_active = False
                            print("MAIN: Enter pressed")
                            self.text_engine = TextEngine(spacing=20, scale=2)
                            self.text_path = self.text_engine.build_path(self.user_text, 50, 300)
                            self.text_index = 0
                            if self.text_path:
                                self.robot.x, self.robot.y, _ = self.text_path[0]
                        elif event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                            print(f"MAIN: Backspace, text: '{self.user_text}'")
                        else:
                            self.user_text += event.unicode
                            print(f"MAIN: Added '{event.unicode}', text: '{self.user_text}'")
            
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
                self.run_text_mode(single_robot=True)
            elif self.cur_state == "text_cooperative":
                self.run_text_mode(single_robot=False)
            
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

    def run_text_mode(self, single_robot=True):
        self.screen.fill(WHITE)
        self.draw_back_button()
        
        font = pygame.font.SysFont('Arial', 24)
        mode_text = "Single Robot" if single_robot else "Cooperative Robots"
        mode_surface = font.render(f"Mode: {mode_text}", True, BLACK)
        self.screen.blit(mode_surface, (WIDTH - 200, 20))
        
        font = pygame.font.SysFont('Arial', 32) 
        if not self.text_entered:
            prompt_surface = font.render("Enter text and press Enter:", True, BLACK)
            self.screen.blit(prompt_surface, (50, 20))
            input_surface = font.render(self.user_text, True, BLACK)
            self.screen.blit(input_surface, (50, 60))
        else:
            for i in range(1, self.text_index):
                x1, y1, pen1 = self.text_path[i-1]
                x2, y2, pen2 = self.text_path[i]
                if pen2:
                    pygame.draw.line(self.screen, BLACK, (x1, y1), (x2, y2), DRAWING_WIDTH)

            if self.text_index < len(self.text_path):
                target_x, target_y, pen = self.text_path[self.text_index]
                self.robot.move_to(target_x, target_y)

                if pen and self.text_index > 0:
                    prev_x, prev_y, _ = self.text_path[self.text_index-1]
                    pygame.draw.line(self.screen, BLACK, (prev_x, prev_y), (self.robot.x, self.robot.y), DRAWING_WIDTH)

                if (round(self.robot.x), round(self.robot.y)) == (round(target_x), round(target_y)):
                    self.text_index += 1

            self.robot.draw_robot(self.screen)
            if not single_robot:
                pygame.draw.circle(self.screen, BLUE, (int(self.robot.x) + 50, int(self.robot.y) + 50), 10)

if __name__ == "__main__":
    game = Game()
    game.run()