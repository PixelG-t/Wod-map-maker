"""
Configuration and constants for WoD Map Editor
"""

import json
import os

# Settings
SETTINGS_FILE = "wod_editor_settings.json"
RECOVERY_FILE = "wod_editor_recovery.png"
RECOVERY_INFO_FILE = "wod_editor_recovery_info.json"

DEFAULT_SETTINGS = {
    'last_save_path': 'my_map.png',
    'canvas_width': 960,
    'canvas_height': 540,
    'dark_theme': True,
    'show_grid': False,
    'grid_size': 32,
    'auto_save': True,
    'snap_to_grid': False,
    'show_coordinates': True,
    'smooth_brush': True,
    'undo_limit': 30,
    'auto_save_interval': 120,
    'ui_animations': True,
    'show_minimap': True,
    'panel_opacity': 95,
}

# Constants
FPS = 60
MIN_BRUSH = 1
MAX_BRUSH = 100
MAX_UNDO = 30
MIN_ZOOM = 0.1
MAX_ZOOM = 8.0

# Terrains
TERRAINS = [
    ("Plains", (160, 194, 69)),
    ("Forest", (57, 131, 54)),
    ("Desert", (237, 228, 176)),
    ("Mountain", (136, 139, 135)),
    ("Snow", (228, 242, 242)),
    ("Mud", (121, 75, 35)),
    ("Water", (39, 155, 255)),
    ("Dark Gray", (110, 107, 112)),
]

# Canvas presets
PRESETS = [
    ("Game Size", 960, 540),
    ("Small", 640, 360),
    ("Medium", 1280, 720),
    ("Large", 1920, 1080),
    ("HD", 1600, 900),
    ("4K", 3840, 2160),
]

def load_settings():
    """Load settings from file"""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                return {**DEFAULT_SETTINGS, **json.load(f)}
    except:
        pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """Save settings to file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
    except:
        pass

def get_colors(dark_theme=True):
    """Get color scheme based on theme"""
    if dark_theme:
        return {
            'bg': (18, 18, 22),
            'bg_alt': (25, 25, 30),
            'panel': (30, 30, 36),
            'panel_light': (40, 40, 46),
            'border': (60, 60, 70),
            'border_light': (80, 80, 90),
            'text': (230, 230, 235),
            'text_dim': (150, 150, 160),
            'accent': (88, 166, 255),
            'accent_hover': (108, 186, 255),
            'accent_dim': (68, 146, 235),
            'success': (80, 200, 120),
            'success_hover': (100, 220, 140),
            'warning': (255, 180, 80),
            'error': (255, 100, 100),
            'layer_accent': (160, 100, 255),
            'layer_hover': (180, 120, 255),
            'grid': (40, 40, 50),
        }
    return {
        'bg': (245, 245, 248),
        'bg_alt': (235, 235, 240),
        'panel': (250, 250, 252),
        'panel_light': (255, 255, 255),
        'border': (200, 200, 210),
        'border_light': (220, 220, 230),
        'text': (30, 30, 35),
        'text_dim': (100, 100, 110),
        'accent': (30, 120, 220),
        'accent_hover': (50, 140, 240),
        'accent_dim': (70, 160, 255),
        'success': (40, 160, 80),
        'success_hover': (60, 180, 100),
        'warning': (220, 140, 40),
        'error': (220, 60, 60),
        'layer_accent': (140, 60, 220),
        'layer_hover': (160, 80, 240),
        'grid': (220, 220, 230),
    }
