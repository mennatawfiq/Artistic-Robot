import pygame
from src.settings import *
from src.robot.robot import Robot
from src.text.text_engine import TextEngine

class CooperativeRobot:
    def __init__(self, screen, text_engine):
        self.screen = screen
        self.text_engine = text_engine
        
        # Robots
        self.robot1 = Robot()
        self.robot2 = Robot()
        
        # Paths and indices
        self.robot1_path = []
        self.robot2_path = []
        self.robot1_index = 0
        self.robot2_index = 0
        
        # Text variables
        self.user_text = ""
        self.text_entered = False
        
        # Colors
        self.RED_COLOR = (255, 0, 0)
        self.BLUE_COLOR = (0, 0, 255)
        self.BLACK_COLOR = (0, 0, 0)
        
    def reset(self):
        """Reset all cooperative mode variables"""
        self.user_text = ""
        self.text_entered = False
        self.robot1_path = []
        self.robot2_path = []
        self.robot1_index = 0
        self.robot2_index = 0
        self.robot1 = Robot()
        self.robot2 = Robot()
    
    def set_text(self, text):
        """Set the text to be drawn"""
        self.user_text = text
        self.text_entered = True
        self._create_cooperative_paths()
    
    def handle_typing(self, event):
        """Handle text typing events"""
        if not self.text_entered:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.text_entered = True
                    self._create_cooperative_paths()
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                else:
                    self.user_text += event.unicode
        return False
    
    def update(self):
        """Update cooperative robots movement"""
        # Move robot 1 
        if self.robot1_index < len(self.robot1_path):
            target_x, target_y, pen = self.robot1_path[self.robot1_index]
            self.robot1.move_to(target_x, target_y)
            
            if (round(self.robot1.x), round(self.robot1.y)) == (round(target_x), round(target_y)):
                self.robot1_index += 1
        
        # Move robot 2 
        if self.robot2_index < len(self.robot2_path):
            target_x, target_y, pen = self.robot2_path[self.robot2_index]
            self.robot2.move_to(target_x, target_y)
            
            if (round(self.robot2.x), round(self.robot2.y)) == (round(target_x), round(target_y)):
                self.robot2_index += 1
    
    def draw(self, back_button_callback):
        """Draw cooperative robots and text"""
        self.screen.fill(WHITE)
        back_button_callback()
        
        # Display current mode
        font = pygame.font.SysFont('Arial', 24)
        mode_surface = font.render("Mode: Cooperative Robots (Split Work)", True, self.BLACK_COLOR)
        self.screen.blit(mode_surface, (WIDTH - 300, 20))
        
        font = pygame.font.SysFont('Arial', 32) 
        
        if not self.text_entered:
            # Show typing prompt
            self._draw_typing_prompt(font)
        else:
            # Draw completed lines
            self._draw_completed_lines()
            
            # Draw current lines
            self._draw_current_lines()
            
            # Draw robots
            self._draw_robots()
            
            # Show cooperation info
            self._draw_cooperation_info(font)
    
    def _draw_typing_prompt(self, font):
        """Draw typing prompt"""
        prompt_surface = font.render("Enter text and press Enter:", True, self.BLACK_COLOR)
        self.screen.blit(prompt_surface, (50, 20))
        input_surface = font.render(self.user_text, True, self.BLACK_COLOR)
        self.screen.blit(input_surface, (50, 60))
    
    def _draw_completed_lines(self):
        """Draw completed lines for both robots"""
        # Draw completed lines for robot 1 
        for i in range(1, self.robot1_index):
            if i < len(self.robot1_path):
                x1, y1, pen1 = self.robot1_path[i-1]
                x2, y2, pen2 = self.robot1_path[i]
                if pen2:
                    pygame.draw.line(self.screen, self.RED_COLOR, (x1, y1), (x2, y2), DRAWING_WIDTH)
        
        # Draw completed lines for robot 2 
        for i in range(1, self.robot2_index):
            if i < len(self.robot2_path):
                x1, y1, pen1 = self.robot2_path[i-1]
                x2, y2, pen2 = self.robot2_path[i]
                if pen2:
                    pygame.draw.line(self.screen, self.BLUE_COLOR, (x1, y1), (x2, y2), DRAWING_WIDTH)
    
    def _draw_current_lines(self):
        """Draw current lines being drawn"""
        # Draw current line for robot 1
        if self.robot1_index > 0 and self.robot1_index < len(self.robot1_path):
            prev_x, prev_y, _ = self.robot1_path[self.robot1_index-1]
            pygame.draw.line(self.screen, self.RED_COLOR, (prev_x, prev_y), 
                           (self.robot1.x, self.robot1.y), DRAWING_WIDTH)
        
        # Draw current line for robot 2
        if self.robot2_index > 0 and self.robot2_index < len(self.robot2_path):
            prev_x, prev_y, _ = self.robot2_path[self.robot2_index-1]
            pygame.draw.line(self.screen, self.BLUE_COLOR, (prev_x, prev_y), 
                           (self.robot2.x, self.robot2.y), DRAWING_WIDTH)
    
    def _draw_robots(self):
        """Draw both robots"""
        # Robot 1 (Red)
        pygame.draw.circle(self.screen, self.RED_COLOR, (int(self.robot1.x), int(self.robot1.y)), 10)
        pygame.draw.circle(self.screen, self.BLACK_COLOR, (int(self.robot1.x), int(self.robot1.y)), 10, 2)
        
        # Robot 2 (Blue)
        pygame.draw.circle(self.screen, self.BLUE_COLOR, (int(self.robot2.x), int(self.robot2.y)), 10)
        pygame.draw.circle(self.screen, self.BLACK_COLOR, (int(self.robot2.x), int(self.robot2.y)), 10, 2)
    
    def _draw_cooperation_info(self, font):
        """Display cooperation information"""
        status_font = pygame.font.SysFont('Arial', 18)
        
        # Show final result
        result_x, result_y = 50, 150
        title_surface = font.render("Final Result:", True, self.BLACK_COLOR)
        self.screen.blit(title_surface, (result_x, result_y - 40))
        
        text_surface = font.render(self.user_text, True, self.BLACK_COLOR)
        self.screen.blit(text_surface, (result_x, result_y))
        
       
        text_length = len(self.user_text)
        mid_point = text_length // 2
        
    
        if text_length % 2 == 0:
          
            robot1_chars = self.user_text[:mid_point]
            robot2_chars = self.user_text[mid_point:]
        else:
            
            robot1_chars = self.user_text[:mid_point]
            robot2_chars = self.user_text[mid_point:]
        
        robot1_info = f"Robot 1 (Red - First Half): '{robot1_chars}' ({len(robot1_chars)} chars)"
        robot2_info = f"Robot 2 (Blue - Second Half): '{robot2_chars}' ({len(robot2_chars)} chars)"
        
        robot1_surface = status_font.render(robot1_info, True, self.RED_COLOR)
        robot2_surface = status_font.render(robot2_info, True, self.BLUE_COLOR)
        
        self.screen.blit(robot1_surface, (50, HEIGHT - 80))
        self.screen.blit(robot2_surface, (50, HEIGHT - 50))
        
        # Show progress
        total_points = len(self.robot1_path) + len(self.robot2_path)
        completed_points = self.robot1_index + self.robot2_index
        progress = f"Progress: {completed_points}/{total_points} points"
        progress_surface = status_font.render(progress, True, self.BLACK_COLOR)
        self.screen.blit(progress_surface, (50, HEIGHT - 110))
        
        # Show completion percentage
        if total_points > 0:
            percentage = (completed_points / total_points) * 100
            percent_surface = status_font.render(f"Completion: {percentage:.1f}%", True, self.BLACK_COLOR)
            self.screen.blit(percent_surface, (50, HEIGHT - 140))
    
    def _create_cooperative_paths(self):
       
        if not self.user_text:
            return
        
        text_length = len(self.user_text)
        mid_point = text_length // 2
        
        
        robot1_text = self.user_text[:mid_point]
        robot2_text = self.user_text[mid_point:]
        
     
        
        
        available_width = WIDTH - 100  
        section_width = available_width // 2
        
       
        robot1_start_x = 50  
        robot2_start_x = 50 + section_width  
        
        
        self.robot1_path = self.text_engine.build_path(robot1_text, robot1_start_x, 300)
        self.robot2_path = self.text_engine.build_path(robot2_text, robot2_start_x, 300)
        
        # Reset indices
        self.robot1_index = 0
        self.robot2_index = 0
        
        # Set initial robot positions
        if self.robot1_path:
            self.robot1.x, self.robot1.y, _ = self.robot1_path[0]
        if self.robot2_path:
            self.robot2.x, self.robot2.y, _ = self.robot2_path[0]
        
        
    
    def is_complete(self):
        """Check if drawing is complete"""
        return (self.robot1_index >= len(self.robot1_path) and 
                self.robot2_index >= len(self.robot2_path))