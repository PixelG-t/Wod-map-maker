"""
Canvas operations for WoD Map Editor
"""

import pygame
import math
from collections import deque

class CanvasManager:
    """Manages canvas operations"""
    
    def __init__(self, width, height, terrains):
        self.width = width
        self.height = height
        self.terrains = terrains
        self.surface = pygame.Surface((width, height))
        self.surface.fill(terrains[0][1])
        self.undo_stack = deque(maxlen=30)
        self.redo_stack = deque(maxlen=30)

    def save_state(self):
        """Save current state to undo stack"""
        self.undo_stack.append(self.surface.copy())
        self.redo_stack.clear()

    def undo(self):
        """Undo last operation"""
        if self.undo_stack:
            self.redo_stack.append(self.surface.copy())
            self.surface = self.undo_stack.pop()
            return True
        return False

    def redo(self):
        """Redo last undone operation"""
        if self.redo_stack:
            self.undo_stack.append(self.surface.copy())
            self.surface = self.redo_stack.pop()
            return True
        return False

    def paint(self, x, y, brush_size, terrain_idx, smooth=True):
        """Paint on canvas"""
        if 0 <= x < self.width and 0 <= y < self.height:
            color = self.terrains[terrain_idx][1]
            if smooth:
                pygame.draw.circle(self.surface, color, (x, y), brush_size)
            else:
                rect = pygame.Rect(x - brush_size, y - brush_size, brush_size * 2, brush_size * 2)
                pygame.draw.rect(self.surface, color, rect)

    def erase(self, x, y, brush_size):
        """Erase on canvas"""
        if 0 <= x < self.width and 0 <= y < self.height:
            pygame.draw.circle(self.surface, self.terrains[0][1], (x, y), brush_size)

    def flood_fill(self, x, y, new_color):
        """Flood fill algorithm"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return 0

        try:
            target = self.surface.get_at((x, y))[:3]
        except:
            return 0

        if target == new_color:
            return 0

        pixels = [(x, y)]
        filled = set()
        max_px = 100000

        pygame.Surface.lock(self.surface)

        try:
            while pixels and len(filled) < max_px:
                if not pixels:
                    break

                px, py = pixels.pop()

                if (px, py) in filled or not (0 <= px < self.width and 0 <= py < self.height):
                    continue

                try:
                    current_color = self.surface.get_at((px, py))[:3]
                    if current_color != target:
                        continue
                except:
                    continue

                self.surface.set_at((px, py), new_color)
                filled.add((px, py))

                pixels.extend([
                    (px + 1, py), (px - 1, py),
                    (px, py + 1), (px, py - 1)
                ])
        finally:
            pygame.Surface.unlock(self.surface)

        return len(filled)

    def draw_line(self, x1, y1, x2, y2, brush_size, terrain_idx):
        """Draw a line"""
        color = self.terrains[terrain_idx][1]
        dx = x2 - x1
        dy = y2 - y1
        distance = max(abs(dx), abs(dy), 1)

        for i in range(distance + 1):
            t = i / distance
            x = max(0, min(int(x1 + dx * t), self.width - 1))
            y = max(0, min(int(y1 + dy * t), self.height - 1))
            pygame.draw.circle(self.surface, color, (x, y), brush_size)

    def draw_circle(self, cx, cy, radius, brush_size, terrain_idx):
        """Draw a circle"""
        color = self.terrains[terrain_idx][1]
        steps = max(int(2 * math.pi * radius), 36)
        for i in range(steps):
            angle = (2 * math.pi * i) / steps
            x = int(cx + radius * math.cos(angle))
            y = int(cy + radius * math.sin(angle))
            if 0 <= x < self.width and 0 <= y < self.height:
                pygame.draw.circle(self.surface, color, (x, y), brush_size)

    def draw_rectangle(self, x1, y1, x2, y2, terrain_idx):
        """Draw a rectangle"""
        color = self.terrains[terrain_idx][1]
        left = max(0, min(x1, x2))
        top = max(0, min(y1, y2))
        right = min(self.width - 1, max(x1, x2))
        bottom = min(self.height - 1, max(y1, y2))
        width = right - left + 1
        height = bottom - top + 1
        pygame.draw.rect(self.surface, color, (left, top, width, height))

    def pick_color(self, x, y):
        """Pick color from canvas"""
        if 0 <= x < self.width and 0 <= y < self.height:
            try:
                color = self.surface.get_at((x, y))[:3]
                min_dist = float('inf')
                best_idx = 0
                for i, (name, tcolor) in enumerate(self.terrains):
                    dist = sum((a-b)**2 for a, b in zip(color, tcolor))
                    if dist < min_dist:
                        min_dist = dist
                        best_idx = i
                return best_idx, self.terrains[best_idx][0]
            except:
                return None, None
        return None, None

    def resize(self, width, height):
        """Resize canvas"""
        self.width = width
        self.height = height
        old_surface = self.surface
        self.surface = pygame.Surface((width, height))
        self.surface.fill(self.terrains[0][1])
        self.surface.blit(old_surface, (0, 0))
        self.undo_stack.clear()
        self.redo_stack.clear()

    def clear(self):
        """Clear canvas"""
        self.surface.fill(self.terrains[0][1])
        self.undo_stack.clear()
        self.redo_stack.clear()
