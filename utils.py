"""
Utility functions for WoD Map Editor
"""

import pygame
import json
import os
from tkinter import filedialog
from collections import deque
from config import RECOVERY_FILE, RECOVERY_INFO_FILE

class UIState:
    """UI state management"""
    
    def __init__(self):
        self.panel_scroll = 0
        self.layer_panel_scroll = 0
        self.hover_terrain = -1
        self.hover_tool = None
        self.hover_layer = -1
        self.notification_queue = deque(maxlen=5)

    def add_notification(self, text, color='success', duration=2000):
        """Add a notification to the queue"""
        self.notification_queue.append({
            'text': text,
            'color': color,
            'time': pygame.time.get_ticks() + duration,
            'alpha': 255
        })

def save_recovery_file(canvas, canvas_w, canvas_h, last_save_path):
    """Save current canvas to recovery file"""
    try:
        pygame.image.save(canvas, RECOVERY_FILE)
        recovery_info = {
            'timestamp': pygame.time.get_ticks(),
            'canvas_size': [canvas_w, canvas_h],
            'last_save_path': last_save_path
        }
        with open(RECOVERY_INFO_FILE, 'w') as f:
            json.dump(recovery_info, f)
        return True
    except:
        return False

def load_recovery_file():
    """Load canvas from recovery file"""
    try:
        if os.path.exists(RECOVERY_FILE) and os.path.exists(RECOVERY_INFO_FILE):
            with open(RECOVERY_INFO_FILE, 'r') as f:
                recovery_info = json.load(f)

            loaded = pygame.image.load(RECOVERY_FILE)
            canvas_w, canvas_h = loaded.get_size()
            
            return loaded, canvas_w, canvas_h, recovery_info
    except:
        pass
    return None, None, None, None

def delete_recovery_files():
    """Delete recovery files after successful save"""
    try:
        if os.path.exists(RECOVERY_FILE):
            os.remove(RECOVERY_FILE)
        if os.path.exists(RECOVERY_INFO_FILE):
            os.remove(RECOVERY_INFO_FILE)
    except:
        pass

def check_for_recovery():
    """Check if recovery file exists"""
    return os.path.exists(RECOVERY_FILE) and os.path.exists(RECOVERY_INFO_FILE)

def save_map(canvas, last_save_path=None):
    """Save map to file"""
    filename = filedialog.asksaveasfilename(
        title="Save Map",
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        initialfile=last_save_path or 'my_map.png'
    )

    if not filename:
        return None

    try:
        if not filename.lower().endswith('.png'):
            filename += '.png'

        pygame.image.save(canvas, filename)
        delete_recovery_files()
        return filename
    except Exception as e:
        return False

def load_map():
    """Load map from file"""
    filename = filedialog.askopenfilename(
        title="Load Map",
        filetypes=[("PNG files", "*.png")]
    )

    if not filename:
        return None, None, None

    try:
        loaded = pygame.image.load(filename)
        canvas_w, canvas_h = loaded.get_size()
        return loaded, canvas_w, canvas_h
    except Exception as e:
        return None, None, str(e)

def screen_to_canvas(mx, my, base_x, base_y, zoom_offset_x, zoom_offset_y, zoom_level, snap_to_grid=False, grid_size=32):
    """Convert screen coordinates to canvas coordinates"""
    canvas_x = base_x + zoom_offset_x
    canvas_y = base_y + zoom_offset_y
    x = int((mx - canvas_x) / zoom_level)
    y = int((my - canvas_y) / zoom_level)

    if snap_to_grid:
        x = (x // grid_size) * grid_size
        y = (y // grid_size) * grid_size

    return x, y

def zoom_at_mouse(mx, my, factor, base_x, base_y, zoom_level, zoom_offset_x, zoom_offset_y, min_zoom, max_zoom):
    """Zoom at mouse position"""
    canvas_x = base_x + zoom_offset_x
    canvas_y = base_y + zoom_offset_y

    mouse_canvas_x = (mx - canvas_x) / zoom_level
    mouse_canvas_y = (my - canvas_y) / zoom_level

    new_zoom = max(min_zoom, min(max_zoom, zoom_level * factor))

    new_canvas_x = mx - mouse_canvas_x * new_zoom
    new_canvas_y = my - mouse_canvas_y * new_zoom

    new_offset_x = new_canvas_x - base_x
    new_offset_y = new_canvas_y - base_y

    return new_zoom, new_offset_x, new_offset_y
