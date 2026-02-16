"""
Easter Eggs for WoD Map Editor
Hidden surprises for users to discover!
"""

import pygame
import random
import math

class EasterEggManager:
    """Manages all Easter eggs in the application - 21 total!"""

    def __init__(self):
        self.discovered = set()
        self.konami_sequence = []
        self.konami_code = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN,
                           pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT,
                           pygame.K_b, pygame.K_a]
        self.click_count = {}
        self.secret_brush_unlocked = False
        self.disco_mode = False
        self.disco_timer = 0
        self.rainbow_mode = False
        self.party_mode = False
        self.party_timer = 0
        self.matrix_mode = False
        self.matrix_drops = []
        self.inverted_mode = False
        self.inverted_timer = 0
        self.shake_mode = False
        self.shake_timer = 0
        self.sparkle_mode = False
        self.sparkle_timer = 0
        self.sparkles = []
        self.zoom_spam_count = 0
        self.last_zoom_time = 0
        self.tool_switches = []
        self.last_save_time = 0
        self.save_spam_count = 0

    def check_konami_code(self, key):
        """Easter Egg #1: Konami Code - activates party mode"""
        self.konami_sequence.append(key)
        if len(self.konami_sequence) > len(self.konami_code):
            self.konami_sequence.pop(0)

        if self.konami_sequence == self.konami_code:
            if 'konami' not in self.discovered:
                self.discovered.add('konami')
                self.party_mode = True
                self.party_timer = pygame.time.get_ticks()
                return "🎉 KONAMI CODE ACTIVATED! Party mode enabled!"
        return None

    def check_canvas_corner_clicks(self, click_pos, canvas_rect):
        """Easter Egg #2: Click all 4 corners of canvas in order"""
        corners = [
            ('tl', pygame.Rect(canvas_rect.left, canvas_rect.top, 50, 50)),
            ('tr', pygame.Rect(canvas_rect.right - 50, canvas_rect.top, 50, 50)),
            ('br', pygame.Rect(canvas_rect.right - 50, canvas_rect.bottom - 50, 50, 50)),
            ('bl', pygame.Rect(canvas_rect.left, canvas_rect.bottom - 50, 50, 50))
        ]

        key = 'corner_sequence'
        if key not in self.click_count:
            self.click_count[key] = {'sequence': [], 'time': pygame.time.get_ticks()}

        # Check if clicked in a corner
        for corner_name, corner_rect in corners:
            if corner_rect.collidepoint(click_pos):
                if pygame.time.get_ticks() - self.click_count[key]['time'] < 10000:  # 10 second window
                    self.click_count[key]['sequence'].append(corner_name)
                    self.click_count[key]['time'] = pygame.time.get_ticks()

                    # Check for complete sequence
                    if len(self.click_count[key]['sequence']) >= 4:
                        if self.click_count[key]['sequence'][-4:] == ['tl', 'tr', 'br', 'bl']:
                            if 'corners' not in self.discovered:
                                self.discovered.add('corners')
                                self.disco_mode = True
                                self.disco_timer = pygame.time.get_ticks()
                                return "🕺 CORNER MASTER! Disco mode activated!"
                else:
                    self.click_count[key] = {'sequence': [corner_name], 'time': pygame.time.get_ticks()}
                break

        return None

    def check_brush_size_egg(self, brush_size):
        """Easter Egg #3: Set brush size to exactly 42"""
        if brush_size == 42 and 'answer' not in self.discovered:
            self.discovered.add('answer')
            return "🌌 You found the Answer to Life, the Universe, and Everything!"
        return None

    def check_terrain_sequence(self, terrain_history):
        """Easter Egg #4: Select terrains in rainbow order"""
        rainbow_sequence = [6, 0, 3, 1]  # Water, Plains, Mountain, Forest
        if len(terrain_history) >= 4:
            if terrain_history[-4:] == rainbow_sequence:
                if 'rainbow' not in self.discovered:
                    self.discovered.add('rainbow')
                    self.rainbow_mode = True
                    return "🌈 RAINBOW MODE UNLOCKED! Your brush is magical!"
        return None

    def check_zoom_level(self, zoom_level):
        """Easter Egg #5: Zoom to exactly 3.14 (pi)"""
        if abs(zoom_level - 3.14) < 0.01 and 'pi' not in self.discovered:
            self.discovered.add('pi')
            return "🥧 Pi detected! You're a mathematical artist!"
        return None

    def check_coordinates(self, x, y):
        """Easter Egg #6: Click at coordinates (69, 420)"""
        if x == 69 and y == 420 and 'coords' not in self.discovered:
            self.discovered.add('coords')
            return "😎 Nice coordinates, nice!"
        return None

    def check_undo_spam(self, undo_count):
        """Easter Egg #7: Undo 10 times rapidly"""
        if undo_count >= 10 and 'undo_spam' not in self.discovered:
            self.discovered.add('undo_spam')
            return "⏪ Undo master! Are you sure about that?"
        return None

    def check_layer_count(self, layer_count):
        """Easter Egg #8: Have exactly 7 layers"""
        if layer_count == 7 and 'lucky7' not in self.discovered:
            self.discovered.add('lucky7')
            return "🍀 Lucky 7 layers! You're a layer legend!"
        return None

    def check_paint_time(self, painting_time):
        """Easter Egg #9: Paint continuously for 30 seconds"""
        if painting_time >= 30000 and 'dedication' not in self.discovered:
            self.discovered.add('dedication')
            return "🎨 30 seconds of continuous painting! True dedication!"
        return None

    def check_middle_click(self, canvas_w, canvas_h, click_x, click_y):
        """Easter Egg #10: Middle click exactly in the center of canvas"""
        center_x = canvas_w // 2
        center_y = canvas_h // 2
        if abs(click_x - center_x) <= 2 and abs(click_y - center_y) <= 2:
            if 'center' not in self.discovered:
                self.discovered.add('center')
                self.matrix_mode = True
                self.init_matrix_drops(canvas_w, canvas_h)
                return "🟢 You found the center! Matrix mode activated!"
        return None

    def init_matrix_drops(self, canvas_w, canvas_h):
        """Initialize matrix rain effect"""
        self.matrix_drops = []
        for i in range(0, canvas_w, 20):
            self.matrix_drops.append({
                'x': i,
                'y': random.randint(-canvas_h, 0),
                'speed': random.uniform(2, 8),
                'chars': [random.randint(0, 1) for _ in range(20)]
            })

    def update_disco_mode(self):
        """Update disco mode state"""
        if self.disco_mode:
            if pygame.time.get_ticks() - self.disco_timer > 10000:  # 10 seconds
                self.disco_mode = False

    def update_party_mode(self):
        """Update party mode state"""
        if self.party_mode:
            if pygame.time.get_ticks() - self.party_timer > 15000:  # 15 seconds
                self.party_mode = False

    def update_all_modes(self):
        """Update all timed modes"""
        self.update_disco_mode()
        self.update_party_mode()
        self.update_inverted_mode()
        self.update_shake_mode()
        self.update_sparkle_mode()

    def get_disco_color(self, base_color):
        """Get disco mode color transformation"""
        if not self.disco_mode:
            return base_color
        t = pygame.time.get_ticks() / 500
        r = int(127 + 127 * math.sin(t))
        g = int(127 + 127 * math.sin(t + 2))
        b = int(127 + 127 * math.sin(t + 4))
        return (r, g, b)

    def get_rainbow_color(self, index):
        """Get rainbow brush color"""
        if not self.rainbow_mode:
            return None
        t = pygame.time.get_ticks() / 1000 + index
        r = int(127 + 127 * math.sin(t))
        g = int(127 + 127 * math.sin(t + 2.094))
        b = int(127 + 127 * math.sin(t + 4.189))
        return (r, g, b)

    def draw_party_effects(self, screen, width, height):
        """Draw party mode effects"""
        if not self.party_mode:
            return

        # Draw random confetti
        for _ in range(10):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(3, 8)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pygame.draw.circle(screen, color, (x, y), size)

    def draw_matrix_effect(self, screen, tiny_font, canvas_rect):
        """Draw matrix rain effect"""
        if not self.matrix_mode or not self.matrix_drops:
            return

        for drop in self.matrix_drops:
            drop['y'] += drop['speed']
            if drop['y'] > canvas_rect.bottom:
                drop['y'] = canvas_rect.top - 20

            # Draw the drop
            for i, char in enumerate(drop['chars']):
                y_pos = int(drop['y'] + i * 15)
                if canvas_rect.top <= y_pos <= canvas_rect.bottom:
                    alpha = max(0, min(255, 255 - i * 20))
                    char_surface = tiny_font.render(str(char), True, (0, 255, 0))
                    char_surface.set_alpha(alpha)
                    screen.blit(char_surface, (drop['x'], y_pos))

    def get_discovered_count(self):
        """Get number of discovered Easter eggs"""
        return len(self.discovered)

    def check_fibonacci_brush(self, brush_size):
        """Easter Egg #11: Set brush to Fibonacci number"""
        fibonacci = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        if brush_size in fibonacci and brush_size > 8:
            if f'fib_{brush_size}' not in self.discovered:
                self.discovered.add(f'fib_{brush_size}')
                return f"🌀 Fibonacci brush ({brush_size})! Nature's perfect spiral!"
        return None

    def check_perfect_square_canvas(self, width, height):
        """Easter Egg #12: Create a perfect square canvas"""
        if width == height and width > 0:
            if 'square' not in self.discovered:
                self.discovered.add('square')
                return f"⬛ Perfect square canvas ({width}x{height})! So symmetrical!"
        return None

    def check_tool_cycler(self, current_tool):
        """Easter Egg #13: Cycle through all tools in 10 seconds"""
        current_time = pygame.time.get_ticks()

        if not hasattr(self, 'tool_switches'):
            self.tool_switches = []

        # Add current tool to history
        if not self.tool_switches or self.tool_switches[-1] != current_tool:
            self.tool_switches.append(current_tool)

        # Keep only recent switches (10 seconds)
        self.tool_switches = [(tool) for tool in self.tool_switches]
        if len(self.tool_switches) > 20:
            self.tool_switches = self.tool_switches[-20:]

        # Check if all tools used
        all_tools = {'brush', 'eraser', 'fill', 'rect', 'line', 'circle', 'picker'}
        if len(self.tool_switches) >= 7 and set(self.tool_switches[-7:]) == all_tools:
            if 'toolmaster' not in self.discovered:
                self.discovered.add('toolmaster')
                self.sparkle_mode = True
                self.sparkle_timer = pygame.time.get_ticks()
                return "✨ TOOL MASTER! You've used all tools! Sparkle mode!"
        return None

    def check_spam_zoom(self):
        """Easter Egg #14: Zoom in/out rapidly 15 times"""
        current_time = pygame.time.get_ticks()

        if current_time - self.last_zoom_time < 300:
            self.zoom_spam_count += 1
        else:
            self.zoom_spam_count = 1

        self.last_zoom_time = current_time

        if self.zoom_spam_count >= 15 and 'zoomspam' not in self.discovered:
            self.discovered.add('zoomspam')
            self.shake_mode = True
            self.shake_timer = pygame.time.get_ticks()
            return "🔍 ZOOM MANIAC! Screen shake activated!"
        return None

    def check_666_coordinates(self, x, y):
        """Easter Egg #15: Click at (666, 666)"""
        if x == 666 and y == 666:
            if 'devil' not in self.discovered:
                self.discovered.add('devil')
                self.inverted_mode = True
                self.inverted_timer = pygame.time.get_ticks()
                return "😈 Devil's coordinates! Inverted colors activated!"
        return None

    def check_1337_coordinates(self, x, y):
        """Easter Egg #16: Click at coordinates containing 1337 (leet speak)"""
        if (x == 1337 or y == 1337) or (x == 13 and y == 37) or (x == 133 and y == 7):
            if 'leet' not in self.discovered:
                self.discovered.add('leet')
                return "😎 1337 H4X0R! You speak the ancient tongue!"
        return None

    def check_binary_brush(self, brush_size):
        """Easter Egg #17: Set brush to power of 2"""
        powers_of_2 = [2, 4, 8, 16, 32, 64]
        if brush_size in powers_of_2 and brush_size >= 16:
            if f'binary_{brush_size}' not in self.discovered:
                self.discovered.add(f'binary_{brush_size}')
                return f"💾 Binary brush ({brush_size})! Computer-perfect!"
        return None

    def check_rapid_save(self):
        """Easter Egg #18: Save 5 times in 10 seconds"""
        current_time = pygame.time.get_ticks()

        if current_time - self.last_save_time < 2000:
            self.save_spam_count += 1
        else:
            self.save_spam_count = 1

        self.last_save_time = current_time

        if self.save_spam_count >= 5 and 'savespam' not in self.discovered:
            self.discovered.add('savespam')
            return "💾 SAVE MASTER! Better safe than sorry!"
        return None

    def check_golden_ratio_zoom(self, zoom_level):
        """Easter Egg #19: Zoom to golden ratio (1.618)"""
        if abs(zoom_level - 1.618) < 0.01:
            if 'golden' not in self.discovered:
                self.discovered.add('golden')
                return "✨ GOLDEN RATIO! Phi-nomenal!"
        return None

    def check_420_69_canvas(self, width, height):
        """Easter Egg #20: Create canvas with 420 or 69 in dimensions"""
        if (width == 420 or height == 420 or width == 69 or height == 69):
            if 'meme_canvas' not in self.discovered:
                self.discovered.add('meme_canvas')
                return "😂 MEME CANVAS DETECTED! Nice dimensions!"
        return None

    def check_all_terrain_paint(self, terrain_usage):
        """Easter Egg #21: Paint with all 8 terrain types in one session"""
        if len(terrain_usage) >= 8 and 'rainbow_painter' not in self.discovered:
            self.discovered.add('rainbow_painter')
            return "🎨 RAINBOW PAINTER! You've used all terrain types!"
        return None

    def check_palindrome_coordinates(self, x, y):
        """Easter Egg #22: Click palindrome coordinates like (121, 121)"""
        def is_palindrome(n):
            s = str(n)
            return s == s[::-1] and len(s) >= 2

        if is_palindrome(x) and is_palindrome(y) and x == y:
            if f'palindrome_{x}' not in self.discovered:
                self.discovered.add(f'palindrome_{x}')
                return f"🔄 PALINDROME COORDINATES ({x},{y})! Perfect symmetry!"
        return None

    def update_inverted_mode(self):
        """Update inverted mode state"""
        if self.inverted_mode:
            if pygame.time.get_ticks() - self.inverted_timer > 8000:  # 8 seconds
                self.inverted_mode = False

    def update_shake_mode(self):
        """Update shake mode state"""
        if self.shake_mode:
            if pygame.time.get_ticks() - self.shake_timer > 5000:  # 5 seconds
                self.shake_mode = False

    def update_sparkle_mode(self):
        """Update sparkle mode state"""
        if self.sparkle_mode:
            if pygame.time.get_ticks() - self.sparkle_timer > 10000:  # 10 seconds
                self.sparkle_mode = False

    def get_shake_offset(self):
        """Get screen shake offset"""
        if not self.shake_mode:
            return (0, 0)
        intensity = 5
        return (random.randint(-intensity, intensity), random.randint(-intensity, intensity))

    def draw_sparkles(self, screen, width, height):
        """Draw sparkle effects"""
        if not self.sparkle_mode:
            return

        # Generate new sparkles
        if random.random() < 0.3:
            self.sparkles.append({
                'x': random.randint(0, width),
                'y': random.randint(0, height),
                'size': random.randint(2, 6),
                'life': 255,
                'color': random.choice([
                    (255, 255, 100), (100, 255, 255), (255, 100, 255),
                    (255, 255, 255), (255, 200, 100)
                ])
            })

        # Update and draw sparkles
        for sparkle in self.sparkles[:]:
            sparkle['life'] -= 5
            if sparkle['life'] <= 0:
                self.sparkles.remove(sparkle)
            else:
                alpha = sparkle['life']
                color = sparkle['color']
                size = int(sparkle['size'] * (sparkle['life'] / 255))
                if size > 0:
                    # Draw sparkle as a star
                    pygame.draw.circle(screen, color, (int(sparkle['x']), int(sparkle['y'])), size)

    def get_inverted_color(self, color):
        """Get inverted color for inverted mode"""
        if not self.inverted_mode:
            return color
        return (255 - color[0], 255 - color[1], 255 - color[2])

    def get_progress_message(self):
        """Get progress message"""
        count = len(self.discovered)
        if count == 0:
            return ""
        elif count < 7:
            return f"🥚 {count}/21 Easter eggs found!"
        elif count < 14:
            return f"🐰 {count}/21 Easter eggs found! Keep going!"
        elif count < 21:
            return f"🔥 {count}/21 Easter eggs found! So close!"
        else:
            return f"🏆 ALL {count} EASTER EGGS FOUND! You're a LEGEND!"
