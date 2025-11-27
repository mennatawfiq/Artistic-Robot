import pygame
from src.settings import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Serif', 32)
        self.title_font = pygame.font.SysFont('Serif', 44, bold=True)
        self.buttons = [
            {"text": "Upload Image", "rect": pygame.Rect(0, 0, 300, 60), "action": "upload"},
            {"text": "Enter Text", "rect": pygame.Rect(0, 0, 300, 60), "action": "text"}
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
        
        # Draw title
        title = self.title_font.render("Autonomous Robotic Art", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font.render("Select Drawing Mode", True, BLACK)
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, 160))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw buttons
        for button in self.buttons:
            # Button background
            pygame.draw.rect(self.screen, PURPLE, button["rect"], border_radius=10)
            pygame.draw.rect(self.screen, BLACK, button["rect"], 2, border_radius=10)
            
            # Button text
            text = self.font.render(button["text"], True, WHITE)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    return button["action"]
        return None