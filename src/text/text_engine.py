import pygame
from src.settings import * 
from src.text.letters import LETTER_PATHS

class TextEngine:
    def __init__(self, spacing=20, scale=1):
        self.spacing = spacing 
        self.scale = scale

    def interpolate(self, x1, y1, x2, y2, pen, step=4):
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
        if char in LETTER_PATHS:
            letter_points = LETTER_PATHS[char]
            if letter_points:
                return max(p[0] for p in letter_points) * self.scale
        return 15 * self.scale

    def get_word_width(self, word):
        width = 0
        for char in word.upper():
            width += self.get_char_width(char) + self.spacing
        return width
    
    def check_collision_global(self, x, y, radius, env):
        local_x = x - PAPER_RECT.left
        local_y = y - PAPER_RECT.top
        return env.obstacles.collides(local_x, local_y, radius)

    def is_area_safe(self, x, y, w, h, env):
        if not env: return True
        cx = x + w / 2
        cy = y + h / 2
        
        if self.check_collision_global(cx, cy, min(w, h)/2, env): return False
        if self.check_collision_global(x, y, 5, env): return False
        if self.check_collision_global(x + w, y + h, 5, env): return False
        return True

    def build_path(self, text, paper_rect, line_spacing=60, env=None):
        final_points = []
        
        margin_x = 20
        start_x = paper_rect.left + margin_x
        max_x = paper_rect.right - margin_x
        
        start_y = paper_rect.top + 10
        max_y = paper_rect.bottom - 10
        
        current_x = start_x
        current_y = start_y
        
        words = text.split(' ')
        line_height = 40 * self.scale 
        
        for word in words:
            word_width = self.get_word_width(word)
            
            # Check if this is a "Mega Word" (Wider than the page itself)
            is_mega_word = word_width > (max_x - start_x)

            # --- PLACEMENT STRATEGY ---
            if not is_mega_word:
                # NORMAL WORD: Try to find a spot for the WHOLE word
                placed = False
                safety_counter = 0 
                
                while not placed:
                    safety_counter += 1
                    if safety_counter > 500: break # Avoid freeze

                    # 1. Border Check
                    if current_x + word_width > max_x:
                        current_x = start_x
                        current_y += line_spacing
                        safety_counter = 0 
                        continue 

                    # 2. Page End Check
                    if current_y > max_y: return final_points

                    # 3. Obstacle Check
                    if env and not self.is_area_safe(current_x, current_y, word_width, line_height, env):
                        current_x += 20 
                    else:
                        placed = True
                
                if not placed: continue # Skip if truly no space for normal word
            else:
                # MEGA WORD: Just ensure we start on a new line if not already there
                # We will handle wrapping character-by-character below.
                if current_x > start_x + 50: # If we aren't near the start
                    current_x = start_x
                    current_y += line_spacing

            # --- DRAWING ---
            for char in word.upper():
                char_width = self.get_char_width(char)
                
                # --- CHARACTER WRAPPING (For Mega Words) ---
                if current_x + char_width > max_x:
                    current_x = start_x
                    current_y += line_spacing
                
                if current_y > max_y: return final_points

                # --- OBSTACLE DODGING (Per Character) ---
                # Check if this specific letter hits a rock
                # If so, scoot right until safe OR we hit the edge again
                if env:
                    char_safe = False
                    sub_attempts = 0
                    while not char_safe and sub_attempts < 20:
                        sub_attempts += 1
                        if self.is_area_safe(current_x, current_y, char_width, line_height, env):
                            char_safe = True
                        else:
                            current_x += 15
                            # If scooting pushes us over edge, wrap line
                            if current_x + char_width > max_x:
                                current_x = start_x
                                current_y += line_spacing
                
                # Retrieve strokes
                if char in LETTER_PATHS:
                    letter_points = LETTER_PATHS[char]
                    
                    local_sx, local_sy, _ = letter_points[0]
                    abs_sx = local_sx * self.scale + current_x
                    abs_sy = local_sy * self.scale + current_y
                    
                    final_points.append((abs_sx, abs_sy, 0)) 
                    
                    for i in range(1, len(letter_points)):
                        p1 = letter_points[i-1]
                        p2 = letter_points[i]
                        
                        x1 = p1[0] * self.scale + current_x
                        y1 = p1[1] * self.scale + current_y
                        x2 = p2[0] * self.scale + current_x
                        y2 = p2[1] * self.scale + current_y
                        
                        stroke_points = self.interpolate(x1, y1, x2, y2, p2[2])
                        
                        # Stroke Eraser (Final Safety)
                        if env:
                            for j in range(len(stroke_points)):
                                px, py, p_pen = stroke_points[j]
                                if self.check_collision_global(px, py, 0, env):
                                    stroke_points[j] = (px, py, 0)
                        
                        final_points.extend(stroke_points)
                
                current_x += char_width + self.spacing
            
            current_x += self.spacing * 2
            
        return final_points