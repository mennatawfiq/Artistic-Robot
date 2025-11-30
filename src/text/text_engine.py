from src.text.letters import LETTER_PATHS
from src.settings import *

class TextEngine:
    def __init__(self, spacing=20, scale=1):
        self.spacing = spacing  # minimum extra space between letters
        self.scale = scale

    def interpolate(self, x1, y1, x2, y2, pen, step=2):
        points = []
        dx = x2 - x1
        dy = y2 - y1
        dist = (dx**2 + dy**2)**0.5
        if dist == 0:
            return [(x1, y1, pen)]
        steps = max(int(dist / step), 1)
        for i in range(1, steps+1):
            xi = x1 + dx * i / steps
            yi = y1 + dy * i / steps
            points.append((xi, yi, pen))
        return points

    def get_char_width(self, char):
        """Helper to get width of a single character."""
        if char in LETTER_PATHS:
            letter_points = LETTER_PATHS[char]
            if letter_points:
                return max(p[0] for p in letter_points) * self.scale
        return 15 * self.scale # Default width for unknown characters (like space)

    def get_word_width(self, word):
        """Calculates total width of a word."""
        width = 0
        for char in word.upper():
            width += self.get_char_width(char) + self.spacing
        return width

    def build_path(self, text, paper_rect, line_spacing=60):
        final_points = []
        
        # Margins inside the paper
        margin_x = 20
        margin_y = 10
        
        start_x = paper_rect.left + margin_x
        start_y = paper_rect.top + margin_y
        
        # Define limits
        max_x = paper_rect.right - margin_x
        max_y = paper_rect.bottom - margin_y
        
        current_x = start_x
        current_y = start_y
        
        words = text.split(' ')
        
        for word in words:
            word_width = self.get_word_width(word)
            
            # --- CHECK IF WORD FITS ---
            if current_x + word_width > max_x:
                # Move to next line
                current_x = start_x
                current_y += line_spacing
            
            # Check Vertical Limit (Stop if we hit bottom)
            if current_y > max_y:
                print("End of page reached. Stopping.")
                break 

            # Draw the word
            for char in word.upper():
                char_width = self.get_char_width(char)
                
                # Check if this specific letter hits the edge
                if current_x + char_width > max_x:
                    current_x = start_x
                    current_y += line_spacing
                    if current_y > max_y: break # Stop if bottom
                
                # Retrieve strokes
                if char in LETTER_PATHS:
                    letter_points = LETTER_PATHS[char]
                    
                    # Move Pen Up to start of letter
                    local_sx, local_sy, _ = letter_points[0]
                    abs_sx = local_sx * self.scale + current_x
                    abs_sy = local_sy * self.scale + current_y
                    final_points.append((abs_sx, abs_sy, 0)) # 0 = Pen Up
                    
                    # Draw strokes
                    for i in range(1, len(letter_points)):
                        p1 = letter_points[i-1]
                        p2 = letter_points[i]
                        
                        x1 = p1[0] * self.scale + current_x
                        y1 = p1[1] * self.scale + current_y
                        x2 = p2[0] * self.scale + current_x
                        y2 = p2[1] * self.scale + current_y
                        
                        final_points.extend(self.interpolate(x1, y1, x2, y2, p2[2]))
                
                # Advance cursor
                current_x += char_width + self.spacing
            
            # Add Space after word
            current_x += self.spacing * 2
            
            # Safety check for space hitting edge
            if current_x > max_x:
                current_x = start_x
                current_y += line_spacing
            
        return final_points
    

    def build_path_coop(self, text, base_x, base_y):
        final_points = []
        offset = 0
        
        for char in text.upper():
            if char == " " or char not in LETTER_PATHS:
                offset += self.spacing  # leave gap for space
                continue
            if char == " " or char not in LETTER_PATHS:
                offset += self.spacing
                continue

            letter_points = LETTER_PATHS[char]

            # Compute letter width
            max_x = max(px for px, py, pen in letter_points) * self.scale

            # Pen-up move to start of letter
            x_start, y_start, _ = letter_points[0]
            x_start = x_start * self.scale + base_x + offset
            y_start = y_start * self.scale + base_y
            final_points.append((x_start, y_start, 0))  # pen up

            # Letter strokes
            for i in range(1, len(letter_points)):
                x1, y1, pen1 = letter_points[i-1]
                x2, y2, pen2 = letter_points[i]

                x1 = x1 * self.scale + base_x + offset
                y1 = y1 * self.scale + base_y
                x2 = x2 * self.scale + base_x + offset
                y2 = y2 * self.scale + base_y

                final_points.extend(self.interpolate(x1, y1, x2, y2, pen2, step=2))

            # Update offset based on letter width + extra spacing
            offset += max_x + self.spacing

        return final_points