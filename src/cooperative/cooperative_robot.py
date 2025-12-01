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
        mode_surface = font.render("Mode: Cooperative Robots", True, BLACK)
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
        prompt_surface = font.render("Enter text and press Enter:", True, BLACK)
        self.screen.blit(prompt_surface, (50, 20))
        input_surface = font.render(self.user_text, True, BLACK)
        self.screen.blit(input_surface, (50, 60))
    
    def _draw_completed_lines(self):
        """Draw completed lines for both robots"""
        # Draw completed lines for robot 1 
        for i in range(1, self.robot1_index):
            if i < len(self.robot1_path):
                x1, y1, pen1 = self.robot1_path[i-1]
                x2, y2, pen2 = self.robot1_path[i]
                if pen2:
                    pygame.draw.line(self.screen, RED, (x1, y1), (x2, y2), DRAWING_WIDTH)
        
        # Draw completed lines for robot 2 
        for i in range(1, self.robot2_index):
            if i < len(self.robot2_path):
                x1, y1, pen1 = self.robot2_path[i-1]
                x2, y2, pen2 = self.robot2_path[i]
                if pen2:
                    pygame.draw.line(self.screen, BLUE, (x1, y1), (x2, y2), DRAWING_WIDTH)
    
    def _draw_current_lines(self):
        """Draw current lines being drawn"""
        # Draw current line for robot 1
        if self.robot1_index > 0 and self.robot1_index < len(self.robot1_path):
            prev_x, prev_y, _ = self.robot1_path[self.robot1_index-1]
            pygame.draw.line(self.screen, RED, (prev_x, prev_y), 
                          (self.robot1.x, self.robot1.y), DRAWING_WIDTH)
        
        # Draw current line for robot 2
        if self.robot2_index > 0 and self.robot2_index < len(self.robot2_path):
            prev_x, prev_y, _ = self.robot2_path[self.robot2_index-1]
            pygame.draw.line(self.screen, BLUE, (prev_x, prev_y), 
                          (self.robot2.x, self.robot2.y), DRAWING_WIDTH)
    
    def _draw_robots(self):
        """Draw both robots"""
        # Robot 1 (Red)
        pygame.draw.circle(self.screen, RED, (int(self.robot1.x), int(self.robot1.y)), 10)
        pygame.draw.circle(self.screen, BLACK, (int(self.robot1.x), int(self.robot1.y)), 10, 2)
        
        # Robot 2 (Blue)
        pygame.draw.circle(self.screen, BLUE, (int(self.robot2.x), int(self.robot2.y)), 10)
        pygame.draw.circle(self.screen, BLACK, (int(self.robot2.x), int(self.robot2.y)), 10, 2)
    
    def _draw_cooperation_info(self, font):
        """Display cooperation information"""
        status_font = pygame.font.SysFont('Arial', 18)
        
        # Show final result
        result_x, result_y = 50, 50
        title_surface = font.render("Final Result:", True, BLACK)
        self.screen.blit(title_surface, (result_x, result_y - 40))
        
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
        
        robot1_surface = status_font.render(robot1_info, True, RED)
        robot2_surface = status_font.render(robot2_info, True, BLUE)
        
        self.screen.blit(robot1_surface, (50, HEIGHT - 80))
        self.screen.blit(robot2_surface, (50, HEIGHT - 50))
        
        # Show progress
        total_points = len(self.robot1_path) + len(self.robot2_path)
        completed_points = self.robot1_index + self.robot2_index
        progress = f"Progress: {completed_points}/{total_points} points"
        progress_surface = status_font.render(progress, True, BLACK)
        self.screen.blit(progress_surface, (50, HEIGHT - 110))
        
        # Show completion percentage
        if total_points > 0:
            percentage = (completed_points / total_points) * 100
            percent_surface = status_font.render(f"Completion: {percentage:.1f}%", True, BLACK)
            self.screen.blit(percent_surface, (50, HEIGHT - 140))
    
    def _create_cooperative_paths(self):
        if not self.user_text:
            return
        
        # Calculate where to split the text (middle character)
        text_length = len(self.user_text)
        mid_point = text_length // 2
        
        robot1_text = self.user_text[:mid_point]
        robot2_text = self.user_text[mid_point:]
        
        # Calculate the actual position where robot2 should start
        # We need to figure out where robot1's text ends (considering line wraps)
        robot2_start_x, robot2_start_y = self._calculate_robot2_start_position(robot1_text)
        
        # Build paths with proper positioning
        robot1_start_x = PAPER_RECT.left + 20
        robot1_start_y = PAPER_RECT.top + 20
        
        self.robot1_path = self.text_engine.build_path_coop_multiline(
            robot1_text, 
            robot1_start_x, 
            robot1_start_y,
            PAPER_RECT,
            LINE_SPACING
        )
        
        self.robot2_path = self.text_engine.build_path_coop_multiline(
            robot2_text, 
            robot2_start_x, 
            robot2_start_y,
            PAPER_RECT,
            LINE_SPACING
        )
        
        # Reset indices
        self.robot1_index = 0
        self.robot2_index = 0
        
        # Set initial robot positions
        if self.robot1_path:
            self.robot1.x, self.robot1.y, _ = self.robot1_path[0]
        if self.robot2_path:
            self.robot2.x, self.robot2.y, _ = self.robot2_path[0]
    
    def _calculate_robot2_start_position(self, robot1_text):
        """Calculate where robot2 should start based on where robot1's text ends"""
        margin_x = 20
        margin_y = 20
        
        start_x = PAPER_RECT.left + margin_x
        start_y = PAPER_RECT.top + margin_y
        max_x = PAPER_RECT.right - margin_x
        
        current_x = start_x
        current_y = start_y
        
        # Simulate drawing robot1's text to find end position
        for char in robot1_text.upper():
            if char == ' ':
                current_x += self.text_engine.spacing * 2
                # Check if space causes line wrap
                if current_x > max_x:
                    current_x = start_x
                    current_y += LINE_SPACING
                continue
            
            char_width = self.text_engine.get_char_width(char)
            
            # Check if character causes line wrap
            if current_x + char_width > max_x:
                current_x = start_x
                current_y += LINE_SPACING
            
            # Draw the character (advance position)
            current_x += char_width + self.text_engine.spacing
        
        # Add a small space between robot1's last char and robot2's first char
        current_x += self.text_engine.spacing
        
        # Check if robot2 needs to start on a new line
        if current_x > max_x:
            current_x = start_x
            current_y += LINE_SPACING
        
        return current_x, current_y
    
    def is_complete(self):
        """Check if drawing is complete"""
        return (self.robot1_index >= len(self.robot1_path) and 
                self.robot2_index >= len(self.robot2_path))