from src.text.letters import LETTER_PATHS

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

    def build_path(self, text, base_x, base_y):
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
