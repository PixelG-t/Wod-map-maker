"""
UI rendering for WoD Map Editor
"""

import pygame
import math

def draw_rounded_rect(surface, color, rect, radius=8, border=0, border_color=None):
    """Draw a rounded rectangle with optional border"""
    if border > 0 and border_color:
        pygame.draw.rect(surface, border_color, rect, border_radius=radius)
        inner = rect.inflate(-border*2, -border*2)
        pygame.draw.rect(surface, color, inner, border_radius=max(0, radius-border))
    else:
        pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_gradient_rect(surface, color1, color2, rect, vertical=True):
    """Draw a gradient rectangle"""
    if vertical:
        for i in range(rect.height):
            t = i / rect.height
            color = tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))
            pygame.draw.line(surface, color, (rect.x, rect.y + i), (rect.x + rect.width, rect.y + i))
    else:
        for i in range(rect.width):
            t = i / rect.width
            color = tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))
            pygame.draw.line(surface, color, (rect.x + i, rect.y), (rect.x + i, rect.y + rect.height))

def draw_shadow(surface, rect, offset=4, alpha=30):
    """Draw a soft shadow"""
    shadow = pygame.Surface((rect.width + offset*2, rect.height + offset*2), pygame.SRCALPHA)
    for i in range(offset):
        a = int(alpha * (1 - i/offset))
        shadow_rect = pygame.Rect(i, i, rect.width + (offset-i)*2, rect.height + (offset-i)*2)
        pygame.draw.rect(shadow, (0, 0, 0, a), shadow_rect, border_radius=12)
    surface.blit(shadow, (rect.x - offset, rect.y - offset))

def draw_canvas_select(screen, width, height, colors, presets, font_large, font, small_font, tiny_font):
    """Enhanced canvas selection screen"""
    screen.fill(colors['bg'])

    # Title
    title_y = 80
    title = font_large.render("CREATE NEW CANVAS", True, colors['text'])
    title_rect = title.get_rect(center=(width // 2, title_y))
    screen.blit(title, title_rect)

    subtitle = small_font.render("Choose a preset size or create custom dimensions", True, colors['text_dim'])
    subtitle_rect = subtitle.get_rect(center=(width // 2, title_y + 35))
    screen.blit(subtitle, subtitle_rect)

    # Decorative line
    line_y = title_y + 60
    pygame.draw.line(screen, colors['accent'], (width//2 - 200, line_y), (width//2 + 200, line_y), 2)

    mx, my = pygame.mouse.get_pos()
    rects = []

    # Calculate grid layout
    start_y = 180
    cols = 3
    card_w = 280
    card_h = 100
    spacing_x = 30
    spacing_y = 30

    total_width = cols * card_w + (cols - 1) * spacing_x
    start_x = (width - total_width) // 2

    for i, (name, w, h) in enumerate(presets):
        col = i % cols
        row = i // cols

        x = start_x + col * (card_w + spacing_x)
        y = start_y + row * (card_h + spacing_y)

        rect = pygame.Rect(x, y, card_w, card_h)
        hover = rect.collidepoint(mx, my)

        # Card shadow
        if hover:
            draw_shadow(screen, rect, offset=6, alpha=40)
        else:
            draw_shadow(screen, rect, offset=3, alpha=20)

        # Card background
        if i == 0:  # Highlight recommended
            card_color = colors['accent_dim'] if not hover else colors['accent']
        else:
            card_color = colors['panel_light'] if not hover else colors['panel']

        draw_rounded_rect(screen, card_color, rect, radius=12)

        if i == 0:
            pygame.draw.rect(screen, colors['accent'], rect, 3, border_radius=12)
        else:
            pygame.draw.rect(screen, colors['border_light'] if hover else colors['border'], rect, 2, border_radius=12)

        # Name
        name_color = (255, 255, 255) if i == 0 else colors['text']
        name_text = font.render(name, True, name_color)
        name_rect = name_text.get_rect(center=(rect.centerx, rect.y + 35))
        screen.blit(name_text, name_rect)

        # Dimensions
        dim_color = (240, 240, 255) if i == 0 else colors['text_dim']
        dim_text = small_font.render(f"{w} x {h} px", True, dim_color)
        dim_rect = dim_text.get_rect(center=(rect.centerx, rect.y + 65))
        screen.blit(dim_text, dim_rect)

        # Recommended badge
        if i == 0:
            badge_text = tiny_font.render("RECOMMENDED", True, (255, 255, 255))
            badge_rect = badge_text.get_rect(center=(rect.centerx, rect.y + 85))
            badge_bg = badge_rect.inflate(12, 6)
            draw_rounded_rect(screen, colors['accent_hover'], badge_bg, radius=4)
            screen.blit(badge_text, badge_rect)

        rects.append((rect, w, h, 'preset'))

    # Load existing button
    load_y = start_y + ((len(presets) - 1) // cols + 1) * (card_h + spacing_y) + 20
    load_btn = pygame.Rect(width // 2 - 150, load_y, 300, 50)
    load_hover = load_btn.collidepoint(mx, my)

    draw_rounded_rect(screen, colors['success_hover' if load_hover else 'success'], load_btn, radius=10)
    pygame.draw.rect(screen, colors['border'], load_btn, 2, border_radius=10)

    load_text = font.render("Load Existing Map", True, (255, 255, 255))
    load_rect = load_text.get_rect(center=load_btn.center)
    screen.blit(load_text, load_rect)

    rects.append((load_btn, 0, 0, 'load'))

    return rects

def draw_toolbar(screen, width, canvas_w, canvas_h, layer_count, colors, font_large, small_font):
    """Enhanced toolbar"""
    toolbar_h = 90

    # Gradient background
    toolbar_surf = pygame.Surface((width, toolbar_h))
    draw_gradient_rect(toolbar_surf, colors['panel'], colors['panel_light'], pygame.Rect(0, 0, width, toolbar_h))

    # Shadow
    pygame.draw.line(toolbar_surf, colors['border'], (0, toolbar_h-1), (width, toolbar_h-1), 2)

    screen.blit(toolbar_surf, (0, 0))

    # Title
    title_text = font_large.render("WOD MAP MAKER", True, colors['text'])
    screen.blit(title_text, (25, 20))

    # Canvas info
    info_text = small_font.render(f"{canvas_w}x{canvas_h}px | {layer_count} layers", True, colors['text_dim'])
    screen.blit(info_text, (25, 52))

    # Buttons
    mx, my = pygame.mouse.get_pos()
    btn_rects = []

    btn_data = [
        ("Save", colors['success'], "Save map (Ctrl+S)"),
        ("Load", colors['accent'], "Load map"),
        ("New", colors['border'], "New canvas (Ctrl+N)"),
        ("Layers", colors['layer_accent'], "Manage layers (Ctrl+O)"),
        ("Settings", colors['border'], "Settings"),
        ("Help", colors['warning'], "Keyboard shortcuts"),
    ]

    btn_x = width - 650
    btn_y = 20
    btn_w = 90
    btn_h = 50
    btn_spacing = 10

    for label, color, tooltip in btn_data:
        btn = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        hover = btn.collidepoint(mx, my)

        # Button background
        if hover:
            lighter = tuple(min(255, c + 30) for c in color)
            draw_rounded_rect(screen, lighter, btn, radius=8)
            pygame.draw.rect(screen, colors['border_light'], btn, 2, border_radius=8)
        else:
            draw_rounded_rect(screen, color, btn, radius=8)
            pygame.draw.rect(screen, colors['border'], btn, 1, border_radius=8)

        # Label
        label_text = small_font.render(label, True, (255, 255, 255))
        label_rect = label_text.get_rect(center=btn.center)
        screen.blit(label_text, label_rect)

        btn_rects.append((btn, label))
        btn_x += btn_w + btn_spacing

    return btn_rects

def draw_side_panel(screen, width, height, selected_terrain, tool, brush_size, terrains, colors, font, small_font, tiny_font, min_brush, max_brush):
    """Enhanced side panel with terrains and tools"""
    panel_w = 340
    panel_x = width - panel_w
    panel_h = height - 90

    # Panel background
    panel_surf = pygame.Surface((panel_w, panel_h))
    draw_gradient_rect(panel_surf, colors['panel'], colors['panel_light'], pygame.Rect(0, 0, panel_w, panel_h), vertical=False)
    screen.blit(panel_surf, (panel_x, 90))

    # Border
    pygame.draw.line(screen, colors['border'], (panel_x, 90), (panel_x, height), 2)

    mx, my = pygame.mouse.get_pos()
    y = 110

    terrain_rects = []
    tool_rects = []

    # TERRAINS SECTION
    section_title = font.render("TERRAIN PALETTE", True, colors['text'])
    screen.blit(section_title, (panel_x + 20, y))
    y += 40

    # Terrain grid (2 columns)
    cols = 2
    terrain_w = (panel_w - 60) // cols
    terrain_h = 44
    spacing = 10

    for i, (name, color) in enumerate(terrains):
        col = i % cols
        row = i // cols

        x = panel_x + 20 + col * (terrain_w + spacing)
        terrain_y = y + row * (terrain_h + spacing)

        rect = pygame.Rect(x, terrain_y, terrain_w, terrain_h)
        hover = rect.collidepoint(mx, my)
        is_selected = i == selected_terrain

        # Terrain card
        if is_selected:
            draw_shadow(screen, rect, offset=3, alpha=40)
            draw_rounded_rect(screen, color, rect, radius=6)
            pygame.draw.rect(screen, colors['accent'], rect, 3, border_radius=6)
        elif hover:
            draw_rounded_rect(screen, color, rect, radius=6)
            pygame.draw.rect(screen, colors['border_light'], rect, 2, border_radius=6)
        else:
            draw_rounded_rect(screen, color, rect, radius=6)
            pygame.draw.rect(screen, colors['border'], rect, 1, border_radius=6)

        # Name and hotkey
        brightness = sum(color) / 3
        text_color = (0, 0, 0) if brightness > 127 else (255, 255, 255)

        name_text = small_font.render(name, True, text_color)
        screen.blit(name_text, (x + 8, terrain_y + 8))

        hotkey_text = tiny_font.render(f"[{i+1}]", True, text_color)
        screen.blit(hotkey_text, (x + 8, terrain_y + 24))

        terrain_rects.append(rect)

    y += ((len(terrains) - 1) // cols + 1) * (terrain_h + spacing) + 25

    # TOOLS SECTION
    pygame.draw.line(screen, colors['border'], (panel_x + 20, y), (panel_x + panel_w - 20, y), 1)
    y += 15

    section_title = font.render("DRAWING TOOLS", True, colors['text'])
    screen.blit(section_title, (panel_x + 20, y))
    y += 35

    tools_data = [
        ("brush", "Brush", "B"),
        ("eraser", "Eraser", "E"),
        ("fill", "Fill", "F"),
        ("rect", "Rectangle", "R"),
        ("line", "Line", "L"),
        ("circle", "Circle", "C"),
        ("picker", "Picker", "P"),
    ]

    for tool_name, label, hotkey in tools_data:
        rect = pygame.Rect(panel_x + 20, y, panel_w - 40, 36)
        hover = rect.collidepoint(mx, my)
        is_active = tool == tool_name

        # Tool button
        if is_active:
            draw_rounded_rect(screen, colors['accent'], rect, radius=6)
            pygame.draw.rect(screen, colors['accent_hover'], rect, 2, border_radius=6)
        elif hover:
            draw_rounded_rect(screen, colors['panel_light'], rect, radius=6)
            pygame.draw.rect(screen, colors['border_light'], rect, 1, border_radius=6)
        else:
            draw_rounded_rect(screen, colors['panel'], rect, radius=6)
            pygame.draw.rect(screen, colors['border'], rect, 1, border_radius=6)

        # Label
        label_color = (255, 255, 255) if is_active else colors['text']
        label_text = small_font.render(label, True, label_color)
        screen.blit(label_text, (rect.x + 15, rect.y + 10))

        # Hotkey
        hotkey_text = tiny_font.render(f"[{hotkey}]", True, label_color)
        screen.blit(hotkey_text, (rect.right - 35, rect.y + 11))

        tool_rects.append((rect, tool_name))
        y += 40

    y += 10

    # BRUSH SIZE SLIDER
    pygame.draw.line(screen, colors['border'], (panel_x + 20, y), (panel_x + panel_w - 20, y), 1)
    y += 15

    brush_label = small_font.render(f"Brush Size: {brush_size}px", True, colors['text'])
    screen.blit(brush_label, (panel_x + 20, y))
    y += 25

    slider_rect = pygame.Rect(panel_x + 20, y, panel_w - 40, 20)

    # Slider track
    draw_rounded_rect(screen, colors['bg'], slider_rect, radius=10)
    pygame.draw.rect(screen, colors['border'], slider_rect, 1, border_radius=10)

    # Slider fill
    fill_percent = (brush_size - min_brush) / (max_brush - min_brush)
    fill_w = int((panel_w - 40) * fill_percent)
    fill_rect = pygame.Rect(panel_x + 20, y, fill_w, 20)
    draw_rounded_rect(screen, colors['accent'], fill_rect, radius=10)

    # Slider handle
    handle_x = panel_x + 20 + fill_w
    handle_y = y + 10
    pygame.draw.circle(screen, (255, 255, 255), (handle_x, handle_y), 12)
    pygame.draw.circle(screen, colors['accent'], (handle_x, handle_y), 10)
    pygame.draw.circle(screen, (255, 255, 255), (handle_x, handle_y), 4)

    return terrain_rects, tool_rects, slider_rect

def draw_status_bar(screen, width, height, mx, my, tool, selected_terrain, brush_size, zoom_level, layer_count, visible_layer_count, unsaved_changes, terrains, colors, tiny_font, canvas_w, canvas_h, screen_to_canvas_func, show_coordinates):
    """Enhanced status bar"""
    status_h = 35
    status_y = height - status_h

    # Gradient background
    status_surf = pygame.Surface((width, status_h))
    draw_gradient_rect(status_surf, colors['panel_light'], colors['panel'], pygame.Rect(0, 0, width, status_h))
    screen.blit(status_surf, (0, status_y))

    # Top border
    pygame.draw.line(screen, colors['border'], (0, status_y), (width, status_y), 2)

    # Left side info
    info_parts = []

    # Coordinates
    if show_coordinates:
        x, y = screen_to_canvas_func(mx, my)
        if 0 <= x < canvas_w and 0 <= y < canvas_h:
            info_parts.append(f"X:{x} Y:{y}")

    # Tool
    info_parts.append(f"{tool.upper()}")

    # Terrain
    terrain_name, _ = terrains[selected_terrain]
    info_parts.append(f"{terrain_name}")

    # Brush size
    info_parts.append(f"Size: {brush_size}px")

    # Zoom
    info_parts.append(f"Zoom: {zoom_level:.1f}x")

    # Layers
    if layer_count > 0:
        info_parts.append(f"{visible_layer_count}/{layer_count} layers")

    # Join and render
    status_text = " | ".join(info_parts)
    text_surf = tiny_font.render(status_text, True, colors['text'])
    screen.blit(text_surf, (15, status_y + 10))

    # Right side - save status
    if unsaved_changes:
        save_text = "Unsaved changes"
        save_color = colors['warning']
    else:
        save_text = "Saved"
        save_color = colors['success']

    save_surf = tiny_font.render(save_text, True, save_color)
    screen.blit(save_surf, (width - save_surf.get_width() - 15, status_y + 10))

def draw_minimap(screen, canvas, canvas_w, canvas_h, width, height, zoom_level, zoom_offset_x, zoom_offset_y, colors, tiny_font, show_minimap):
    """Draw minimap in corner"""
    if not show_minimap or zoom_level <= 1.0:
        return

    minimap_w = 200
    minimap_h = int(minimap_w * canvas_h / canvas_w)
    minimap_x = 20
    minimap_y = height - minimap_h - 60

    # Background
    minimap_bg = pygame.Rect(minimap_x - 5, minimap_y - 5, minimap_w + 10, minimap_h + 10)
    draw_rounded_rect(screen, colors['panel'], minimap_bg, radius=8)
    pygame.draw.rect(screen, colors['border'], minimap_bg, 2, border_radius=8)

    # Scaled canvas
    minimap_canvas = pygame.transform.scale(canvas, (minimap_w, minimap_h))
    screen.blit(minimap_canvas, (minimap_x, minimap_y))

    # Viewport indicator
    viewport_scale = minimap_w / canvas_w
    viewport_w = int(width / zoom_level * viewport_scale)
    viewport_h = int((height - 90) / zoom_level * viewport_scale)
    viewport_x = minimap_x - int(zoom_offset_x / zoom_level * viewport_scale)
    viewport_y = minimap_y - int(zoom_offset_y / zoom_level * viewport_scale)

    viewport_rect = pygame.Rect(viewport_x, viewport_y, viewport_w, viewport_h)
    pygame.draw.rect(screen, colors['accent'], viewport_rect, 2)

    # Label
    label = tiny_font.render("MINIMAP", True, colors['text_dim'])
    screen.blit(label, (minimap_x, minimap_bg.bottom + 3))

def draw_notifications(screen, ui_state, width, colors, small_font):
    """Draw notification queue"""
    y = 110
    to_remove = []
    current_time = pygame.time.get_ticks()

    for i, notif in enumerate(ui_state.notification_queue):
        if current_time > notif['time']:
            to_remove.append(i)
            continue

        # Fade out in last 500ms
        time_left = notif['time'] - current_time
        if time_left < 500:
            notif['alpha'] = int(255 * (time_left / 500))

        # Notification box
        text_surf = small_font.render(notif['text'], True, colors['text'])
        box_w = text_surf.get_width() + 40
        box_h = 40
        box_x = width // 2 - box_w // 2
        box_rect = pygame.Rect(box_x, y, box_w, box_h)

        # Shadow
        draw_shadow(screen, box_rect, offset=3, alpha=20)

        # Background
        color_map = {
            'success': colors['success'],
            'error': colors['error'],
            'warning': colors['warning'],
            'accent': colors['accent'],
        }
        bg_color = color_map.get(notif.get('color', 'success'), colors['success'])

        notif_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        draw_rounded_rect(notif_surf, (*bg_color, notif['alpha']), pygame.Rect(0, 0, box_w, box_h), radius=8)
        screen.blit(notif_surf, (box_x, y))

        # Border
        pygame.draw.rect(screen, (*colors['border_light'], notif['alpha']), box_rect, 2, border_radius=8)

        # Text
        text_surf.set_alpha(notif['alpha'])
        text_rect = text_surf.get_rect(center=box_rect.center)
        screen.blit(text_surf, text_rect)

        y += box_h + 10

    # Remove expired notifications
    for i in reversed(to_remove):
        ui_state.notification_queue.remove(list(ui_state.notification_queue)[i])

def draw_settings_panel(screen, width, height, settings, colors, font_large, font, small_font):
    """Draw settings dialog"""
    panel_w = 500
    panel_h = 400
    panel_x = width // 2 - panel_w // 2
    panel_y = height // 2 - panel_h // 2

    # Dark overlay
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Shadow
    panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
    draw_shadow(screen, panel_rect, offset=8, alpha=50)

    # Background
    draw_rounded_rect(screen, colors['panel'], panel_rect, radius=12)
    pygame.draw.rect(screen, colors['accent'], panel_rect, 3, border_radius=12)

    mx, my = pygame.mouse.get_pos()
    y = panel_y + 20
    rects = []

    # Title
    title = font_large.render("SETTINGS", True, colors['text'])
    screen.blit(title, (panel_x + 20, y))
    y += 50

    # Settings checkboxes
    settings_list = [
        ('dark_theme', "Dark Theme"),
        ('show_grid', "Show Grid"),
        ('show_minimap', "Show Minimap"),
        ('smooth_brush', "Smooth Brush (Anti-aliased)"),
        ('show_coordinates', "Show Coordinates"),
    ]

    for key, label in settings_list:
        checkbox_rect = pygame.Rect(panel_x + 20, y, 30, 30)
        pygame.draw.rect(screen, colors['bg'], checkbox_rect, border_radius=4)
        pygame.draw.rect(screen, colors['border'], checkbox_rect, 2, border_radius=4)
        if settings.get(key, False):
            pygame.draw.circle(screen, colors['accent'], checkbox_rect.center, 10)

        label_text = small_font.render(label, True, colors['text'])
        screen.blit(label_text, (panel_x + 60, y + 5))
        rects.append((key, checkbox_rect))
        y += 45

    y += 15

    # Close button
    close_btn = pygame.Rect(panel_x + 150, panel_y + panel_h - 60, 200, 40)
    close_hover = close_btn.collidepoint(mx, my)
    draw_rounded_rect(screen, colors['accent_hover' if close_hover else 'accent'], close_btn, radius=8)
    pygame.draw.rect(screen, colors['border'], close_btn, 2, border_radius=8)

    close_text = font.render("Close", True, (255, 255, 255))
    screen.blit(close_text, (close_btn.centerx - 25, close_btn.centery - 8))
    rects.append(('close', close_btn))

    return rects

def draw_help_panel(screen, width, height, colors, font_large, font, tiny_font):
    """Draw help dialog with keyboard shortcuts"""
    panel_w = 600
    panel_h = 500
    panel_x = width // 2 - panel_w // 2
    panel_y = height // 2 - panel_h // 2

    # Dark overlay
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Shadow
    panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
    draw_shadow(screen, panel_rect, offset=8, alpha=50)

    # Background
    draw_rounded_rect(screen, colors['panel'], panel_rect, radius=12)
    pygame.draw.rect(screen, colors['warning'], panel_rect, 3, border_radius=12)

    mx, my = pygame.mouse.get_pos()
    y = panel_y + 20

    # Title
    title = font_large.render("KEYBOARD SHORTCUTS", True, colors['text'])
    screen.blit(title, (panel_x + 20, y))
    y += 50

    # Shortcuts list
    shortcuts = [
        ("DRAWING TOOLS", ""),
        ("B", "Brush"),
        ("E", "Eraser"),
        ("F", "Fill bucket"),
        ("R", "Rectangle"),
        ("L", "Line"),
        ("C", "Circle"),
        ("P", "Color picker"),
        ("", ""),
        ("LAYERS", ""),
        ("Ctrl+Shift+1-9", "Toggle overlay layers 1-9"),
        ("V", "Toggle current layer"),
        ("Ctrl+A", "Toggle all layers"),
        ("Ctrl+O", "Open layer manager"),
        ("", ""),
        ("CANVAS", ""),
        ("1-8", "Select terrain"),
        ("[ / ]", "Decrease/increase brush size"),
        ("Space+Drag", "Pan canvas"),
        ("Mouse wheel", "Zoom in/out"),
        ("0", "Reset zoom to 100%"),
        ("", ""),
        ("FILE", ""),
        ("Ctrl+S", "Save map"),
        ("Ctrl+N", "New canvas"),
        ("Ctrl+Z", "Undo"),
        ("Ctrl+Y", "Redo"),
    ]

    for key, desc in shortcuts:
        if not key and not desc:
            y += 10
            continue

        if not desc:  # Section header
            section_text = small_font.render(key, True, colors['accent'])
            screen.blit(section_text, (panel_x + 20, y))
            y += 25
        else:
            key_text = tiny_font.render(key, True, colors['text'])
            desc_text = tiny_font.render(desc, True, colors['text_dim'])
            screen.blit(key_text, (panel_x + 40, y))
            screen.blit(desc_text, (panel_x + 200, y))
            y += 20

    # Close button
    close_btn = pygame.Rect(panel_x + 200, panel_y + panel_h - 60, 200, 40)
    close_hover = close_btn.collidepoint(mx, my)
    draw_rounded_rect(screen, colors['accent_hover' if close_hover else 'accent'], close_btn, radius=8)
    pygame.draw.rect(screen, colors['border'], close_btn, 2, border_radius=8)

    close_text = font.render("Close", True, (255, 255, 255))
    screen.blit(close_text, (close_btn.centerx - 25, close_btn.centery - 8))

    return [('close', close_btn)]

def draw_layer_panel(screen, width, height, layer_manager, colors, settings, font_large, small_font, tiny_font):
    """Enhanced multi-layer panel"""
    if not layer_manager.layers:
        return []

    panel_w = 600
    panel_h = min(500, height - 200)
    panel_x = width // 2 - panel_w // 2
    panel_y = height - panel_h - 60

    # Shadow
    panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
    draw_shadow(screen, panel_rect, offset=8, alpha=50)

    # Background
    panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    panel_surf.fill((*colors['panel'], int(255 * settings.get('panel_opacity', 95) / 100)))
    screen.blit(panel_surf, (panel_x, panel_y))

    # Border
    pygame.draw.rect(screen, colors['layer_accent'], panel_rect, 3, border_radius=12)
    pygame.draw.rect(screen, colors['layer_hover'], panel_rect.inflate(4, 4), 1, border_radius=13)

    mx, my = pygame.mouse.get_pos()
    y = panel_y + 20
    rects = []

    # Title
    title = font_large.render("LAYER MANAGER", True, colors['layer_hover'])
    screen.blit(title, (panel_x + 20, y))
    y += 35

    subtitle = tiny_font.render(f"{len(layer_manager.layers)} layer(s) | Drag to move | Ctrl+Shift+1-9 to toggle", True, colors['text_dim'])
    screen.blit(subtitle, (panel_x + 20, y))
    y += 25

    # Divider
    pygame.draw.line(screen, colors['border'], (panel_x + 20, y), (panel_x + panel_w - 20, y), 1)
    y += 15

    # Layer list
    layer_list_h = 180
    layer_y_start = y

    for i, layer in enumerate(layer_manager.layers):
        is_current = i == layer_manager.current_idx
        layer_rect = pygame.Rect(panel_x + 20, y, panel_w - 40, 38)
        hover = layer_rect.collidepoint(mx, my)

        # Layer card
        if is_current:
            draw_rounded_rect(screen, colors['layer_accent'], layer_rect, radius=6)
            pygame.draw.rect(screen, colors['layer_hover'], layer_rect, 2, border_radius=6)
        elif hover:
            draw_rounded_rect(screen, colors['panel_light'], layer_rect, radius=6)
            pygame.draw.rect(screen, colors['border_light'], layer_rect, 1, border_radius=6)
        else:
            draw_rounded_rect(screen, colors['panel'], layer_rect, radius=6)
            pygame.draw.rect(screen, colors['border'], layer_rect, 1, border_radius=6)

        # Layer number indicator
        num_color = (255, 255, 255) if is_current else colors['text']
        num_text = f"[{i+1}]" if i < 9 else "[*]"
        num_label = tiny_font.render(num_text, True, num_color)
        screen.blit(num_label, (layer_rect.x + 10, layer_rect.y + 12))

        # Visibility indicator
        vis_text = "V" if layer.visible else "H"
        vis_label = tiny_font.render(vis_text, True, num_color)
        screen.blit(vis_label, (layer_rect.x + 45, layer_rect.y + 12))

        # Lock indicator
        if layer.locked:
            lock_label = tiny_font.render("[L]", True, num_color)
            screen.blit(lock_label, (layer_rect.x + 70, layer_rect.y + 12))

        # Layer name
        name_text = tiny_font.render(layer.name[:40], True, num_color)
        screen.blit(name_text, (layer_rect.x + (95 if layer.locked else 70), layer_rect.y + 12))

        # Layer info
        img_w, img_h = layer.original.get_size()
        info_text = tiny_font.render(f"{img_w}x{img_h} | {int(layer.alpha/255*100)}% | {layer.scale:.2f}x", True, num_color)
        screen.blit(info_text, (layer_rect.right - info_text.get_width() - 10, layer_rect.y + 12))

        rects.append(('layer_select', layer_rect, i))
        y += 42

    y = layer_y_start + max(layer_list_h, len(layer_manager.layers) * 42 + 10)

    # Divider
    pygame.draw.line(screen, colors['border'], (panel_x + 20, y), (panel_x + panel_w - 20, y), 1)
    y += 15

    # Current layer controls
    layer = layer_manager.get_current_layer()
    if layer:
        # Opacity slider
        opacity_label = small_font.render("Opacity", True, colors['text'])
        screen.blit(opacity_label, (panel_x + 20, y))

        opacity_val = small_font.render(f"{int(layer.alpha/255*100)}%", True, colors['layer_hover'])
        screen.blit(opacity_val, (panel_x + panel_w - 60, y))
        y += 25

        slider_w = panel_w - 40
        alpha_slider = pygame.Rect(panel_x + 20, y, slider_w, 22)

        # Track
        draw_rounded_rect(screen, colors['bg'], alpha_slider, radius=11)
        pygame.draw.rect(screen, colors['border'], alpha_slider, 1, border_radius=11)

        # Fill
        fill_percent = layer.alpha / 255
        fill_w = int(slider_w * fill_percent)
        fill_rect = pygame.Rect(panel_x + 20, y, fill_w, 22)

        if fill_w > 0:
            fill_surf = pygame.Surface((fill_w, 22))
            draw_gradient_rect(fill_surf, colors['layer_accent'], colors['layer_hover'], pygame.Rect(0, 0, fill_w, 22), vertical=False)
            screen.blit(fill_surf, (panel_x + 20, y))
            pygame.draw.rect(screen, colors['layer_hover'], fill_rect, border_radius=11)

        # Handle
        handle_x = panel_x + 20 + fill_w
        handle_y = y + 11
        pygame.draw.circle(screen, (255, 255, 255), (handle_x, handle_y), 14)
        pygame.draw.circle(screen, colors['layer_hover'], (handle_x, handle_y), 12)
        pygame.draw.circle(screen, (255, 255, 255), (handle_x, handle_y), 5)

        rects.append(('alpha_slider', alpha_slider))
        y += 35

        # Scale slider
        scale_label = small_font.render("Scale", True, colors['text'])
        screen.blit(scale_label, (panel_x + 20, y))

        scale_val = small_font.render(f"{layer.scale:.2f}x", True, colors['layer_hover'])
        screen.blit(scale_val, (panel_x + panel_w - 60, y))
        y += 25

        scale_slider = pygame.Rect(panel_x + 20, y, slider_w, 22)

        # Track
        draw_rounded_rect(screen, colors['bg'], scale_slider, radius=11)
        pygame.draw.rect(screen, colors['border'], scale_slider, 1, border_radius=11)

        # Fill
        fill_percent = (layer.scale - 0.1) / (3.0 - 0.1)
        fill_w = int(slider_w * fill_percent)
        fill_rect = pygame.Rect(panel_x + 20, y, fill_w, 22)

        if fill_w > 0:
            draw_rounded_rect(screen, colors['success'], fill_rect, radius=11)

        # Handle
        handle_x = panel_x + 20 + fill_w
        handle_y = y + 11
        pygame.draw.circle(screen, (255, 255, 255), (handle_x, handle_y), 14)
        pygame.draw.circle(screen, colors['success'], (handle_x, handle_y), 12)
        pygame.draw.circle(screen, (255, 255, 255), (handle_x, handle_y), 5)

        rects.append(('scale_slider', scale_slider))
        y += 40

    # Divider
    pygame.draw.line(screen, colors['border'], (panel_x + 20, y), (panel_x + panel_w - 20, y), 1)
    y += 12

    # Action buttons
    btn_data = [
        ('Add', colors['success'], 'add_layer'),
        ('Toggle', colors['accent'], 'toggle'),
        ('Apply', colors['success_hover'], 'apply'),
        ('Remove', colors['error'], 'clear'),
        ('Close', colors['border'], 'close'),
    ]

    btn_count = len(btn_data)
    btn_w = (panel_w - 40 - 10 * (btn_count - 1)) // btn_count
    btn_h = 44
    btn_x = panel_x + 20

    for label, color, action in btn_data:
        btn_rect = pygame.Rect(btn_x, y, btn_w, btn_h)
        hover = btn_rect.collidepoint(mx, my)

        # Button
        if hover:
            lighter = tuple(min(255, c + 30) for c in color)
            draw_rounded_rect(screen, lighter, btn_rect, radius=8)
            pygame.draw.rect(screen, colors['border_light'], btn_rect, 2, border_radius=8)
        else:
            draw_rounded_rect(screen, color, btn_rect, radius=8)
            pygame.draw.rect(screen, colors['border'], btn_rect, 1, border_radius=8)

        # Label
        label_text = small_font.render(label, True, (255, 255, 255))
        label_rect = label_text.get_rect(center=btn_rect.center)
        screen.blit(label_text, label_rect)

        rects.append((action, btn_rect))
        btn_x += btn_w + 10

    return rects
