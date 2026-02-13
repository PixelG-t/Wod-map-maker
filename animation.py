"""
Animation system for WoD Map Editor
"""

import pygame

class AnimationManager:
    """Manages smooth UI animations"""
    
    def __init__(self):
        self.animations = []

    def add(self, target_obj, property_name, target_value, duration=300, easing='ease_out'):
        """Add a new animation"""
        anim = {
            'obj': target_obj,
            'prop': property_name,
            'start': getattr(target_obj, property_name, 0),
            'target': target_value,
            'duration': duration,
            'start_time': pygame.time.get_ticks(),
            'easing': easing
        }
        self.animations.append(anim)

    def update(self):
        """Update all animations"""
        current_time = pygame.time.get_ticks()
        completed = []

        for i, anim in enumerate(self.animations):
            elapsed = current_time - anim['start_time']
            progress = min(1.0, elapsed / anim['duration'])

            # Easing functions
            if anim['easing'] == 'ease_out':
                progress = 1 - (1 - progress) ** 3
            elif anim['easing'] == 'ease_in':
                progress = progress ** 3
            elif anim['easing'] == 'ease_in_out':
                if progress < 0.5:
                    progress = 4 * progress ** 3
                else:
                    progress = 1 - (-2 * progress + 2) ** 3 / 2

            # Interpolate value
            current = anim['start'] + (anim['target'] - anim['start']) * progress
            setattr(anim['obj'], anim['prop'], current)

            if progress >= 1.0:
                completed.append(i)

        # Remove completed animations
        for i in reversed(completed):
            self.animations.pop(i)
