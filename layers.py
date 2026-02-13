"""
Layer management for WoD Map Editor
"""

import pygame
import os
from tkinter import filedialog

class OverlayLayer:
    """Multi-layer overlay system"""
    
    def __init__(self, original, name="Layer"):
        self.original = original
        self.image = None
        self.pos = [0, 0]
        self.alpha = 128
        self.scale = 1.0
        self.visible = True
        self.locked = False
        self.name = name
        self.blend_mode = 'normal'
        self.update_image()

    def update_image(self):
        """Update the displayed image with current scale and alpha"""
        w, h = self.original.get_size()
        new_w = max(1, int(w * self.scale))
        new_h = max(1, int(h * self.scale))

        self.image = pygame.transform.smoothscale(self.original, (new_w, new_h))
        self.image.set_alpha(self.alpha)

    def get_bounds(self):
        """Get the bounding rectangle of this layer"""
        if self.image:
            w, h = self.image.get_size()
            return pygame.Rect(self.pos[0], self.pos[1], w, h)
        return pygame.Rect(0, 0, 0, 0)

class LayerManager:
    """Manages all overlay layers"""
    
    def __init__(self):
        self.layers = []
        self.current_idx = 0

    def add_layer(self, image, name="Layer"):
        """Add a new layer"""
        layer = OverlayLayer(image, name)
        self.layers.append(layer)
        self.current_idx = len(self.layers) - 1
        return layer

    def remove_layer(self, idx):
        """Remove a layer by index"""
        if 0 <= idx < len(self.layers):
            self.layers.pop(idx)
            if self.current_idx >= len(self.layers) and self.layers:
                self.current_idx = len(self.layers) - 1

    def get_current_layer(self):
        """Get the currently selected layer"""
        if 0 <= self.current_idx < len(self.layers):
            return self.layers[self.current_idx]
        return None

    def load_overlay_image(self, canvas_w, canvas_h):
        """Load an overlay image as a new layer"""
        filename = filedialog.askopenfilename(
            title="Load Overlay Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
            ]
        )

        if not filename:
            return None, None

        try:
            loaded = pygame.image.load(filename)
            original = loaded.convert_alpha()

            img_w, img_h = original.get_size()

            layer_name = f"Layer {len(self.layers) + 1}: {os.path.basename(filename)[:20]}"
            layer = self.add_layer(original, layer_name)

            layer.pos[0] = (canvas_w - img_w) // 2
            layer.pos[1] = (canvas_h - img_h) // 2

            return layer, (img_w, img_h)
        except Exception as e:
            return None, str(e)

    def apply_layer(self, canvas, idx):
        """Bake layer into canvas"""
        if 0 <= idx < len(self.layers):
            layer = self.layers[idx]
            if layer.visible and layer.image:
                canvas.blit(layer.image, layer.pos)
                layer_name = layer.name
                self.remove_layer(idx)
                return layer_name
        return None

    def toggle_layer_visibility(self, idx):
        """Toggle layer visibility"""
        if 0 <= idx < len(self.layers):
            self.layers[idx].visible = not self.layers[idx].visible
            return self.layers[idx].visible
        return None

    def toggle_all_layers(self):
        """Toggle all layers visibility"""
        if self.layers:
            any_visible = any(layer.visible for layer in self.layers)
            new_state = not any_visible
            for layer in self.layers:
                layer.visible = new_state
            return new_state
        return None
