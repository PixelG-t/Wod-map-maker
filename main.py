"""
War of Dots Map Editor - Enhanced Edition
A map editor with multi layer overlay and modern UI

Author: wowthat
"""

import pygame
from pygame.locals import *
import sys
import math
import random
from tkinter import Tk
import os

# Import modules
from config import *
from animation import AnimationManager
from layers import LayerManager
from canvas import CanvasManager
from utils import *
from ui import *
from easter_eggs import EasterEggManager

def main():
    # Initialize
    root = Tk()
    root.withdraw()
    pygame.init()

    # Screen setup
    info = pygame.display.Info()
    SCREEN_W, SCREEN_H = info.current_w, info.current_h
    WIDTH, HEIGHT = 1600, 900
    screen = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
    pygame.display.set_caption("WoD Map Editor - Enhanced Edition")

    # Load settings
    settings = load_settings()
    COLORS = get_colors(settings['dark_theme'])

    # Fonts
    try:
        font_large = pygame.font.SysFont("Segoe UI", 24, bold=True)
        font = pygame.font.SysFont("Segoe UI", 18)
        small_font = pygame.font.SysFont("Segoe UI", 14)
        tiny_font = pygame.font.SysFont("Segoe UI", 12)
    except:
        font_large = pygame.font.Font(None, 24)
        font = pygame.font.Font(None, 18)
        small_font = pygame.font.Font(None, 14)
        tiny_font = pygame.font.Font(None, 12)

    # Easter egg: 25% chance for alternate welcome screen
    use_alternate_welcome = random.random() < 0.25

    # State
    current_screen = "welcome" if use_alternate_welcome or random.random() < 0.5 else "canvas_select"
    canvas_manager = None
    layer_manager = LayerManager()
    anim_manager = AnimationManager()
    ui_state = UIState()
    easter_egg_manager = EasterEggManager()

    # Easter egg tracking
    terrain_selection_history = []
    terrain_usage = set()  # Track which terrains have been used
    undo_counter = 0
    last_undo_time = 0
    paint_start_time = None
    continuous_paint_time = 0
    
    selected_terrain = 0
    brush_size = 8
    tool = "brush"
    painting = False
    panning = False
    pan_start = None
    last_paint_pos = None
    shape_start = None
    unsaved_changes = False
    dragging_slider = False
    show_exit_confirm = False
    show_settings = False
    show_help = False
    show_overlay_controls = False
    dragging_overlay = False
    overlay_drag_start = None
    dragging_alpha_slider = False
    dragging_scale_slider = False
    last_auto_save = 0
    dragging_layer_panel = False
    layer_panel_drag_offset = None
    layer_panel_pos = None

    # Zoom
    zoom_level = 1.0
    zoom_offset_x = 0
    zoom_offset_y = 0

    base_canvas_x = 0
    base_canvas_y = 100

    # Print startup info
    print("WoD Map Editor - Enhanced Edition")
    print("=" * 50)
    print("New features:")
    print("  - Modern gradient UI with smooth animations")
    print("  - Enhanced multi-layer system")
    print("  - Minimap for easy navigation")
    print("  - Improved notifications")
    print("  - Better color scheme")
    print("  - Ctrl+Shift+1-9 for overlay layer control")
    print("\nPress H for help")
    print("Press Ctrl+O for multi-layer overlay")
    print("Auto-save: ON (every {}s)".format(settings.get('auto_save_interval', 120)))
    print("=" * 50)

    clock = pygame.time.Clock()
    running = True
    last_auto_save = pygame.time.get_ticks()
    auto_save_interval = settings.get('auto_save_interval', 120) * 1000

    def get_screen_to_canvas():
        """Create screen_to_canvas function with current state"""
        return lambda mx, my: screen_to_canvas(
            mx, my, base_canvas_x, base_canvas_y,
            zoom_offset_x, zoom_offset_y, zoom_level,
            settings.get('snap_to_grid', False),
            settings.get('grid_size', 32)
        )

    while running:
        dt = clock.tick(FPS)
        anim_manager.update()

        mx, my = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()

        # Auto-save
        if settings['auto_save'] and current_screen == "editor" and canvas_manager:
            if current_time - last_auto_save > auto_save_interval:
                if unsaved_changes:
                    save_recovery_file(canvas_manager.surface, canvas_manager.width, 
                                     canvas_manager.height, settings['last_save_path'])
                    last_auto_save = current_time

        for event in pygame.event.get():
            if event.type == QUIT:
                if settings['auto_save'] and unsaved_changes and canvas_manager:
                    save_recovery_file(canvas_manager.surface, canvas_manager.width,
                                     canvas_manager.height, settings['last_save_path'])
                running = False

            elif event.type == VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                if canvas_manager:
                    base_canvas_x = (WIDTH - canvas_manager.width) // 2
                    base_canvas_y = 100

            elif event.type == MOUSEWHEEL:
                if current_screen == "editor":
                    zoom_level, zoom_offset_x, zoom_offset_y = zoom_at_mouse(
                        mx, my, 1.1 if event.y > 0 else 1/1.1,
                        base_canvas_x, base_canvas_y, zoom_level,
                        zoom_offset_x, zoom_offset_y, MIN_ZOOM, MAX_ZOOM
                    )

            elif event.type == KEYDOWN:
                # Easter egg: Check Konami code
                egg_msg = easter_egg_manager.check_konami_code(event.key)
                if egg_msg:
                    ui_state.add_notification(egg_msg, 'success', 5000)

                if event.key == K_ESCAPE:
                    if show_overlay_controls:
                        show_overlay_controls = False
                    elif show_settings:
                        show_settings = False
                    elif show_help:
                        show_help = False
                    else:
                        running = False

                elif current_screen == "editor":
                    layer = layer_manager.get_current_layer()

                    # Layer controls
                    if layer and show_overlay_controls:
                        if event.key == K_UP:
                            layer.pos[1] -= 1
                        elif event.key == K_DOWN:
                            layer.pos[1] += 1
                        elif event.key == K_LEFT:
                            layer.pos[0] -= 1
                        elif event.key == K_RIGHT:
                            layer.pos[0] += 1

                    # Ctrl+Shift+1-9 for overlay layer control
                    mods = pygame.key.get_mods()
                    if (mods & KMOD_CTRL) and (mods & KMOD_SHIFT):
                        layer_keys = {
                            K_1: 0, K_2: 1, K_3: 2, K_4: 3, K_5: 4,
                            K_6: 5, K_7: 6, K_8: 7, K_9: 8
                        }

                        if event.key in layer_keys:
                            layer_idx = layer_keys[event.key]
                            result = layer_manager.toggle_layer_visibility(layer_idx)
                            if result is not None:
                                ui_state.add_notification(
                                    f"Overlay {layer_idx + 1}: {'visible' if result else 'hidden'}",
                                    'layer_hover'
                                )
                            continue

                    # V toggles current selected layer
                    if event.key == K_v and layer_manager.layers:
                        layer = layer_manager.get_current_layer()
                        if layer:
                            layer.visible = not layer.visible
                            ui_state.add_notification(
                                f"Current layer: {'visible' if layer.visible else 'hidden'}",
                                'accent'
                            )

                    # Ctrl+A toggles all layers
                    elif event.key == K_a and pygame.key.get_mods() & KMOD_CTRL:
                        result = layer_manager.toggle_all_layers()
                        if result is not None:
                            ui_state.add_notification(
                                f"All layers: {'visible' if result else 'hidden'}",
                                'accent'
                            )

                    # Terrain selection
                    elif K_1 <= event.key <= K_9:
                        idx = event.key - K_1
                        if idx < len(TERRAINS):
                            selected_terrain = idx
                            terrain_selection_history.append(idx)
                            if len(terrain_selection_history) > 10:
                                terrain_selection_history.pop(0)

                            # Easter egg: Check rainbow sequence
                            egg_msg = easter_egg_manager.check_terrain_sequence(terrain_selection_history)
                            if egg_msg:
                                ui_state.add_notification(egg_msg, 'success', 5000)

                    # Tools
                    elif event.key == K_b:
                        tool = "brush"
                        egg_msg = easter_egg_manager.check_tool_cycler(tool)
                        if egg_msg:
                            ui_state.add_notification(egg_msg, 'success', 5000)
                    elif event.key == K_e:
                        tool = "eraser"
                        egg_msg = easter_egg_manager.check_tool_cycler(tool)
                        if egg_msg:
                            ui_state.add_notification(egg_msg, 'success', 5000)
                    elif event.key == K_f:
                        tool = "fill"
                        egg_msg = easter_egg_manager.check_tool_cycler(tool)
                        if egg_msg:
                            ui_state.add_notification(egg_msg, 'success', 5000)
                    elif event.key == K_r:
                        tool = "rect"
                        egg_msg = easter_egg_manager.check_tool_cycler(tool)
                        if egg_msg:
                            ui_state.add_notification(egg_msg, 'success', 5000)
                    elif event.key == K_l:
                        tool = "line"
                        egg_msg = easter_egg_manager.check_tool_cycler(tool)
                        if egg_msg:
                            ui_state.add_notification(egg_msg, 'success', 5000)
                    elif event.key == K_c:
                        tool = "circle"
                        egg_msg = easter_egg_manager.check_tool_cycler(tool)
                        if egg_msg:
                            ui_state.add_notification(egg_msg, 'success', 5000)
                    elif event.key == K_p:
                        tool = "picker"
                        egg_msg = easter_egg_manager.check_tool_cycler(tool)
                        if egg_msg:
                            ui_state.add_notification(egg_msg, 'success', 5000)
                    elif event.key == K_o and pygame.key.get_mods() & KMOD_CTRL:
                        if layer_manager.layers:
                            show_overlay_controls = not show_overlay_controls
                        else:
                            result, size = layer_manager.load_overlay_image(
                                canvas_manager.width, canvas_manager.height
                            )
                            if result:
                                show_overlay_controls = True
                                img_w, img_h = size
                                if img_w > canvas_manager.width or img_h > canvas_manager.height:
                                    ui_state.add_notification(
                                        f"Layer added ({img_w}x{img_h}) - use Scale slider!",
                                        'warning', 4000
                                    )
                                else:
                                    ui_state.add_notification(
                                        f"Layer added: {result.name}",
                                        'success', 3000
                                    )
                    elif event.key == K_h:
                        show_help = True

                    # Brush size
                    elif event.key == K_LEFTBRACKET:
                        brush_size = max(MIN_BRUSH, brush_size - 2)
                        # Check multiple Easter eggs
                        for check in [easter_egg_manager.check_brush_size_egg,
                                     easter_egg_manager.check_fibonacci_brush,
                                     easter_egg_manager.check_binary_brush]:
                            egg_msg = check(brush_size)
                            if egg_msg:
                                ui_state.add_notification(egg_msg, 'success', 5000)
                    elif event.key == K_RIGHTBRACKET:
                        brush_size = min(MAX_BRUSH, brush_size + 2)
                        # Check multiple Easter eggs
                        for check in [easter_egg_manager.check_brush_size_egg,
                                     easter_egg_manager.check_fibonacci_brush,
                                     easter_egg_manager.check_binary_brush]:
                            egg_msg = check(brush_size)
                            if egg_msg:
                                ui_state.add_notification(egg_msg, 'success', 5000)

                    # Undo/Redo
                    elif event.key == K_z and pygame.key.get_mods() & KMOD_CTRL:
                        if pygame.key.get_mods() & KMOD_SHIFT:
                            if canvas_manager.redo():
                                ui_state.add_notification("Redo", 'accent')
                        else:
                            if canvas_manager.undo():
                                unsaved_changes = True
                                ui_state.add_notification("Undo", 'accent')

                                # Easter egg: Track undo spam
                                current_time = pygame.time.get_ticks()
                                if current_time - last_undo_time < 500:
                                    undo_counter += 1
                                else:
                                    undo_counter = 1
                                last_undo_time = current_time

                                egg_msg = easter_egg_manager.check_undo_spam(undo_counter)
                                if egg_msg:
                                    ui_state.add_notification(egg_msg, 'success', 5000)
                    elif event.key == K_y and pygame.key.get_mods() & KMOD_CTRL:
                        if canvas_manager.redo():
                            ui_state.add_notification("Redo", 'accent')

                    # Save/Load
                    elif event.key == K_s and pygame.key.get_mods() & KMOD_CTRL:
                        result = save_map(canvas_manager.surface, settings['last_save_path'])
                        if result:
                            settings['last_save_path'] = result
                            save_settings(settings)
                            unsaved_changes = False
                            delete_recovery_files()
                            ui_state.add_notification(f"Saved: {os.path.basename(result)}", 'success')

                            # Easter egg: Check rapid save
                            egg_msg = easter_egg_manager.check_rapid_save()
                            if egg_msg:
                                ui_state.add_notification(egg_msg, 'success', 5000)
                        elif result is False:
                            ui_state.add_notification("Save failed", 'error')
                    elif event.key == K_n and pygame.key.get_mods() & KMOD_CTRL:
                        current_screen = "canvas_select"

                    # Zoom
                    elif event.key == K_0:
                        zoom_level = 1.0
                        zoom_offset_x = 0
                        zoom_offset_y = 0
                        ui_state.add_notification("Zoom reset", 'accent')
                    elif event.key == K_EQUALS or event.key == K_PLUS:
                        zoom_level, zoom_offset_x, zoom_offset_y = zoom_at_mouse(
                            mx, my, 1.25, base_canvas_x, base_canvas_y,
                            zoom_level, zoom_offset_x, zoom_offset_y,
                            MIN_ZOOM, MAX_ZOOM
                        )
                        # Check zoom Easter eggs
                        egg_msg = easter_egg_manager.check_zoom_level(zoom_level)
                        if egg_msg:
                            ui_state.add_notification(egg_msg, 'success', 5000)
                        egg_msg = easter_egg_manager.check_golden_ratio_zoom(zoom_level)
                        if egg_msg:
                            ui_state.add_notification(egg_msg, 'success', 5000)
                        egg_msg = easter_egg_manager.check_spam_zoom()
                        if egg_msg:
                            ui_state.add_notification(egg_msg, 'success', 5000)
                    elif event.key == K_MINUS:
                        zoom_level, zoom_offset_x, zoom_offset_y = zoom_at_mouse(
                            mx, my, 1/1.25, base_canvas_x, base_canvas_y,
                            zoom_level, zoom_offset_x, zoom_offset_y,
                            MIN_ZOOM, MAX_ZOOM
                        )
                        # Check zoom Easter eggs
                        egg_msg = easter_egg_manager.check_zoom_level(zoom_level)
                        if egg_msg:
                            ui_state.add_notification(egg_msg, 'success', 5000)
                        egg_msg = easter_egg_manager.check_golden_ratio_zoom(zoom_level)
                        if egg_msg:
                            ui_state.add_notification(egg_msg, 'success', 5000)
                        egg_msg = easter_egg_manager.check_spam_zoom()
                        if egg_msg:
                            ui_state.add_notification(egg_msg, 'success', 5000)

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Handle settings panel
                if show_settings:
                    settings_rects = draw_settings_panel(screen, WIDTH, HEIGHT, settings,
                                                        COLORS, font_large, font, small_font)
                    for item in settings_rects:
                        name, rect = item
                        if rect.collidepoint(mx, my):
                            if name == 'close':
                                show_settings = False
                            elif name == 'dark_theme':
                                settings['dark_theme'] = not settings['dark_theme']
                                COLORS = get_colors(settings['dark_theme'])
                                save_settings(settings)
                            elif name in settings:
                                settings[name] = not settings[name]
                                save_settings(settings)
                            break

                # Handle help panel
                elif show_help:
                    help_rects = draw_help_panel(screen, WIDTH, HEIGHT, COLORS,
                                                 font_large, font, tiny_font)
                    for name, rect in help_rects:
                        if rect.collidepoint(mx, my) and name == 'close':
                            show_help = False
                            break

                elif show_overlay_controls and layer_manager.layers:
                    layer_rects, panel_rect = draw_layer_panel(screen, WIDTH, HEIGHT, layer_manager,
                                                   COLORS, settings, font_large, small_font, tiny_font, layer_panel_pos)
                    handled = False

                    for item in layer_rects:
                        if len(item) == 3:
                            name, rect, idx = item
                            if name == 'layer_select' and rect.collidepoint(mx, my):
                                layer_manager.current_idx = idx
                                handled = True
                                break
                            elif name == 'drag_handle' and rect.collidepoint(mx, my):
                                dragging_layer_panel = True
                                layer_panel_drag_offset = (mx - panel_rect.x, my - panel_rect.y)
                                handled = True
                                break
                        else:
                            name, rect = item
                            if rect.collidepoint(mx, my):
                                if name == 'alpha_slider':
                                    dragging_alpha_slider = True
                                elif name == 'scale_slider':
                                    dragging_scale_slider = True
                                elif name == 'toggle':
                                    layer = layer_manager.get_current_layer()
                                    if layer:
                                        layer.visible = not layer.visible
                                        ui_state.add_notification(
                                            f"Layer {'visible' if layer.visible else 'hidden'}",
                                            'accent'
                                        )
                                elif name == 'apply':
                                    layer_name = layer_manager.apply_layer(
                                        canvas_manager.surface,
                                        layer_manager.current_idx
                                    )
                                    if layer_name:
                                        unsaved_changes = True
                                        ui_state.add_notification(
                                            f"{layer_name} applied to canvas!",
                                            'success'
                                        )
                                        if not layer_manager.layers:
                                            show_overlay_controls = False
                                elif name == 'clear':
                                    if layer_manager.layers:
                                        layer_name = layer_manager.layers[layer_manager.current_idx].name
                                        layer_manager.remove_layer(layer_manager.current_idx)
                                        ui_state.add_notification(f"{layer_name} removed", 'success')
                                        if not layer_manager.layers:
                                            show_overlay_controls = False
                                elif name == 'close':
                                    show_overlay_controls = False
                                    layer_panel_pos = None
                                elif name == 'add_layer':
                                    result, size = layer_manager.load_overlay_image(
                                        canvas_manager.width, canvas_manager.height
                                    )
                                    if result:
                                        img_w, img_h = size
                                        if img_w > canvas_manager.width or img_h > canvas_manager.height:
                                            ui_state.add_notification(
                                                f"Layer added ({img_w}x{img_h}) - use Scale slider!",
                                                'warning', 4000
                                            )
                                        else:
                                            ui_state.add_notification(
                                                f"Layer added",
                                                'success', 3000
                                            )

                                        # Easter egg: Check layer count
                                        egg_msg = easter_egg_manager.check_layer_count(len(layer_manager.layers))
                                        if egg_msg:
                                            ui_state.add_notification(egg_msg, 'success', 5000)
                                handled = True
                                break

                    if not handled:
                        # Check overlay dragging
                        layer = layer_manager.get_current_layer()
                        if layer and not layer.locked:
                            canvas_x = base_canvas_x + zoom_offset_x
                            canvas_y = base_canvas_y + zoom_offset_y
                            overlay_x = int(canvas_x + layer.pos[0] * zoom_level)
                            overlay_y = int(canvas_y + layer.pos[1] * zoom_level)
                            ow, oh = layer.image.get_size()
                            overlay_rect = pygame.Rect(overlay_x, overlay_y,
                                                      int(ow * zoom_level), int(oh * zoom_level))

                            if overlay_rect.collidepoint(mx, my):
                                dragging_overlay = True
                                overlay_drag_start = (mx - layer.pos[0] * zoom_level,
                                                    my - layer.pos[1] * zoom_level)

                elif current_screen == "welcome":
                    start_btn, title_rect = draw_welcome_screen(screen, WIDTH, HEIGHT, COLORS,
                                                                font_large, font, small_font, tiny_font,
                                                                use_alternate_welcome)
                    if start_btn.collidepoint(mx, my):
                        current_screen = "canvas_select"
                        ui_state.add_notification("Welcome to WoD Map Maker!", 'accent', 2000)

                elif current_screen == "canvas_select":
                    rects = draw_canvas_select(screen, WIDTH, HEIGHT, COLORS, PRESETS,
                                              font_large, font, small_font, tiny_font)
                    for rect, w, h, btn_type in rects:
                        if rect.collidepoint(mx, my):
                            if btn_type == 'load':
                                loaded, canvas_w, canvas_h = load_map()
                                if loaded:
                                    canvas_manager = CanvasManager(canvas_w, canvas_h, TERRAINS)
                                    canvas_manager.surface = loaded
                                    base_canvas_x = (WIDTH - canvas_w) // 2
                                    base_canvas_y = 100
                                    unsaved_changes = False
                                    ui_state.add_notification(f"Loaded: {canvas_w}x{canvas_h}", 'success')
                                    current_screen = "editor"
                                elif canvas_h:
                                    ui_state.add_notification(f"Load failed: {canvas_h}", 'error')
                            else:
                                canvas_manager = CanvasManager(w, h, TERRAINS)
                                base_canvas_x = (WIDTH - w) // 2
                                base_canvas_y = 100
                                settings['canvas_width'] = w
                                settings['canvas_height'] = h
                                save_settings(settings)
                                ui_state.add_notification(f"Canvas created: {w}x{h}", 'success')
                                current_screen = "editor"

                                # Easter eggs: Check canvas dimensions
                                egg_msg = easter_egg_manager.check_perfect_square_canvas(w, h)
                                if egg_msg:
                                    ui_state.add_notification(egg_msg, 'success', 5000)

                                egg_msg = easter_egg_manager.check_420_69_canvas(w, h)
                                if egg_msg:
                                    ui_state.add_notification(egg_msg, 'success', 5000)
                            break

                elif current_screen == "editor":
                    # Get UI elements
                    screen_to_canvas_func = get_screen_to_canvas()
                    
                    btn_rects = draw_toolbar(screen, WIDTH, canvas_manager.width,
                                           canvas_manager.height, len(layer_manager.layers),
                                           COLORS, font_large, small_font)
                    terrain_rects, tool_rects, slider_rect = draw_side_panel(
                        screen, WIDTH, HEIGHT, selected_terrain, tool, brush_size,
                        TERRAINS, COLORS, font, small_font, tiny_font, MIN_BRUSH, MAX_BRUSH
                    )

                    # Check slider
                    if slider_rect.collidepoint(mx, my):
                        dragging_slider = True
                        percent = (mx - slider_rect.x) / slider_rect.width
                        brush_size = int(MIN_BRUSH + percent * (MAX_BRUSH - MIN_BRUSH))

                    # Check buttons
                    else:
                        clicked = False
                        for btn, label in btn_rects:
                            if btn.collidepoint(mx, my):
                                if label == "Save":
                                    result = save_map(canvas_manager.surface, settings['last_save_path'])
                                    if result:
                                        settings['last_save_path'] = result
                                        save_settings(settings)
                                        unsaved_changes = False
                                        delete_recovery_files()
                                        ui_state.add_notification(f"Saved: {os.path.basename(result)}", 'success')
                                    elif result is False:
                                        ui_state.add_notification("Save failed", 'error')
                                elif label == "Load":
                                    loaded, canvas_w, canvas_h = load_map()
                                    if loaded:
                                        canvas_manager = CanvasManager(canvas_w, canvas_h, TERRAINS)
                                        canvas_manager.surface = loaded
                                        base_canvas_x = (WIDTH - canvas_w) // 2
                                        unsaved_changes = False
                                        ui_state.add_notification(f"Loaded: {canvas_w}x{canvas_h}", 'success')
                                elif label == "New":
                                    current_screen = "canvas_select"
                                elif label == "Layers":
                                    if layer_manager.layers:
                                        show_overlay_controls = not show_overlay_controls
                                    else:
                                        result, size = layer_manager.load_overlay_image(
                                            canvas_manager.width, canvas_manager.height
                                        )
                                        if result:
                                            show_overlay_controls = True
                                            img_w, img_h = size
                                            if img_w > canvas_manager.width or img_h > canvas_manager.height:
                                                ui_state.add_notification(
                                                    f"Layer added ({img_w}x{img_h}) - use Scale slider!",
                                                    'warning', 4000
                                                )
                                            else:
                                                ui_state.add_notification("Layer added", 'success', 3000)
                                elif label == "Settings":
                                    show_settings = True
                                elif label == "Help":
                                    show_help = True
                                clicked = True
                                break

                        # Check terrains
                        if not clicked:
                            for i, rect in enumerate(terrain_rects):
                                if rect.collidepoint(mx, my):
                                    selected_terrain = i
                                    clicked = True
                                    break

                        # Check tools
                        if not clicked:
                            for rect, tool_name in tool_rects:
                                if rect.collidepoint(mx, my):
                                    tool = tool_name
                                    clicked = True
                                    break

                        # Canvas interaction
                        if not clicked:
                            x, y = screen_to_canvas_func(mx, my)

                            # Easter egg: Check canvas corner clicks
                            canvas_rect = pygame.Rect(base_canvas_x + zoom_offset_x, base_canvas_y + zoom_offset_y,
                                                     int(canvas_manager.width * zoom_level), int(canvas_manager.height * zoom_level))
                            egg_msg = easter_egg_manager.check_canvas_corner_clicks((mx, my), canvas_rect)
                            if egg_msg:
                                ui_state.add_notification(egg_msg, 'success', 5000)

                            if 0 <= x < canvas_manager.width and 0 <= y < canvas_manager.height:
                                if pygame.key.get_pressed()[K_SPACE]:
                                    panning = True
                                    pan_start = (mx, my)
                                elif tool == "fill":
                                    canvas_manager.save_state()
                                    filled = canvas_manager.flood_fill(x, y, TERRAINS[selected_terrain][1])
                                    if filled > 0:
                                        unsaved_changes = True
                                        ui_state.add_notification(f"Filled {filled} pixels", 'success')
                                    else:
                                        ui_state.add_notification("Nothing to fill", 'warning')
                                elif tool == "picker":
                                    idx, name = canvas_manager.pick_color(x, y)
                                    if idx is not None:
                                        selected_terrain = idx
                                        ui_state.add_notification(f"Picked: {name}", 'accent')
                                elif tool in ["rect", "line", "circle"]:
                                    shape_start = (mx, my)
                                elif tool == "brush":
                                    painting = True
                                    paint_start_time = pygame.time.get_ticks()
                                    canvas_manager.save_state()
                                    last_paint_pos = (mx, my)
                                    canvas_manager.paint(x, y, brush_size, selected_terrain,
                                                       settings.get('smooth_brush', True))
                                    unsaved_changes = True

                                    # Track terrain usage
                                    terrain_usage.add(selected_terrain)
                                    egg_msg = easter_egg_manager.check_all_terrain_paint(terrain_usage)
                                    if egg_msg:
                                        ui_state.add_notification(egg_msg, 'success', 5000)
                                elif tool == "eraser":
                                    painting = True
                                    canvas_manager.save_state()
                                    last_paint_pos = (mx, my)
                                    canvas_manager.erase(x, y, brush_size)
                                    unsaved_changes = True

            elif event.type == MOUSEBUTTONDOWN and event.button == 2:
                # Middle mouse button - Easter egg check
                if current_screen == "editor" and canvas_manager:
                    screen_to_canvas_func = get_screen_to_canvas()
                    x, y = screen_to_canvas_func(mx, my)
                    egg_msg = easter_egg_manager.check_middle_click(
                        canvas_manager.width, canvas_manager.height, x, y
                    )
                    if egg_msg:
                        ui_state.add_notification(egg_msg, 'success', 5000)

            elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                if current_screen == "editor":
                    screen_to_canvas_func = get_screen_to_canvas()
                    x, y = screen_to_canvas_func(mx, my)

                    # Easter eggs: Check various coordinate Easter eggs
                    for check in [easter_egg_manager.check_coordinates,
                                 easter_egg_manager.check_666_coordinates,
                                 easter_egg_manager.check_1337_coordinates,
                                 easter_egg_manager.check_palindrome_coordinates]:
                        egg_msg = check(x, y)
                        if egg_msg:
                            ui_state.add_notification(egg_msg, 'success', 5000)

                    idx, name = canvas_manager.pick_color(x, y)
                    if idx is not None:
                        selected_terrain = idx
                        ui_state.add_notification(f"Picked: {name}", 'accent')

            elif event.type == MOUSEBUTTONUP and event.button == 1:
                if dragging_layer_panel:
                    dragging_layer_panel = False
                    layer_panel_drag_offset = None
                elif dragging_alpha_slider:
                    dragging_alpha_slider = False
                elif dragging_scale_slider:
                    dragging_scale_slider = False
                elif dragging_overlay:
                    dragging_overlay = False
                    overlay_drag_start = None
                elif current_screen == "editor":
                    if dragging_slider:
                        dragging_slider = False
                    elif panning:
                        panning = False
                        pan_start = None
                    elif shape_start and tool in ["rect", "line", "circle"]:
                        screen_to_canvas_func = get_screen_to_canvas()
                        x1, y1 = screen_to_canvas_func(shape_start[0], shape_start[1])
                        x2, y2 = screen_to_canvas_func(mx, my)

                        canvas_manager.save_state()
                        if tool == "rect":
                            canvas_manager.draw_rectangle(x1, y1, x2, y2, selected_terrain)
                        elif tool == "line":
                            canvas_manager.draw_line(x1, y1, x2, y2, brush_size, selected_terrain)
                        elif tool == "circle":
                            radius = int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
                            canvas_manager.draw_circle(x1, y1, radius, brush_size, selected_terrain)

                        shape_start = None
                        unsaved_changes = True

                    painting = False
                    last_paint_pos = None

        # Continuous interactions
        if dragging_layer_panel and layer_panel_drag_offset:
            layer_panel_pos = (mx - layer_panel_drag_offset[0], my - layer_panel_drag_offset[1])

        if dragging_slider and current_screen == "editor":
            terrain_rects, tool_rects, slider_rect = draw_side_panel(
                screen, WIDTH, HEIGHT, selected_terrain, tool, brush_size,
                TERRAINS, COLORS, font, small_font, tiny_font, MIN_BRUSH, MAX_BRUSH
            )
            percent = max(0, min(1, (mx - slider_rect.x) / slider_rect.width))
            brush_size = int(MIN_BRUSH + percent * (MAX_BRUSH - MIN_BRUSH))

        if dragging_alpha_slider:
            layer = layer_manager.get_current_layer()
            if layer:
                layer_rects, panel_rect = draw_layer_panel(screen, WIDTH, HEIGHT, layer_manager,
                                               COLORS, settings, font_large, small_font, tiny_font, layer_panel_pos)
                for item in layer_rects:
                    if len(item) == 2:
                        name, rect = item
                        if name == 'alpha_slider':
                            percent = max(0, min(1, (mx - rect.x) / rect.width))
                            layer.alpha = int(255 * percent)
                            layer.update_image()
                            break

        if dragging_scale_slider:
            layer = layer_manager.get_current_layer()
            if layer:
                layer_rects, panel_rect = draw_layer_panel(screen, WIDTH, HEIGHT, layer_manager,
                                               COLORS, settings, font_large, small_font, tiny_font, layer_panel_pos)
                for item in layer_rects:
                    if len(item) == 2:
                        name, rect = item
                        if name == 'scale_slider':
                            percent = max(0, min(1, (mx - rect.x) / rect.width))
                            layer.scale = 0.1 + percent * (3.0 - 0.1)
                            layer.update_image()
                            break

        if dragging_overlay and overlay_drag_start:
            layer = layer_manager.get_current_layer()
            if layer:
                canvas_x = base_canvas_x + zoom_offset_x
                canvas_y = base_canvas_y + zoom_offset_y
                layer.pos[0] = int((mx - overlay_drag_start[0]) / zoom_level)
                layer.pos[1] = int((my - overlay_drag_start[1]) / zoom_level)

        if panning and pan_start:
            dx = mx - pan_start[0]
            dy = my - pan_start[1]
            zoom_offset_x += dx
            zoom_offset_y += dy
            pan_start = (mx, my)

        if painting and tool in ["brush", "eraser"] and current_screen == "editor":
            # Easter egg: Track continuous painting
            if paint_start_time:
                continuous_paint_time = pygame.time.get_ticks() - paint_start_time
                egg_msg = easter_egg_manager.check_paint_time(continuous_paint_time)
                if egg_msg:
                    ui_state.add_notification(egg_msg, 'success', 5000)

            screen_to_canvas_func = get_screen_to_canvas()
            x, y = screen_to_canvas_func(mx, my)

            if tool == "brush":
                canvas_manager.paint(x, y, brush_size, selected_terrain,
                                   settings.get('smooth_brush', True))
            else:
                canvas_manager.erase(x, y, brush_size)

            if last_paint_pos:
                lx, ly = last_paint_pos
                steps = max(abs(mx - lx), abs(my - ly), 1)
                for i in range(steps):
                    t = i / steps
                    ix = int(lx + (mx - lx) * t)
                    iy = int(ly + (my - ly) * t)
                    x, y = screen_to_canvas_func(ix, iy)
                    if tool == "brush":
                        canvas_manager.paint(x, y, brush_size, selected_terrain,
                                           settings.get('smooth_brush', True))
                    else:
                        canvas_manager.erase(x, y, brush_size)
            last_paint_pos = (mx, my)
        else:
            paint_start_time = None

        # Update Easter egg states
        easter_egg_manager.update_all_modes()

        # Draw
        if current_screen == "welcome":
            draw_welcome_screen(screen, WIDTH, HEIGHT, COLORS,
                              font_large, font, small_font, tiny_font, use_alternate_welcome)
        elif current_screen == "canvas_select":
            draw_canvas_select(screen, WIDTH, HEIGHT, COLORS, PRESETS,
                             font_large, font, small_font, tiny_font)
        else:
            # Draw editor
            # Apply shake offset if shake mode is active
            shake_x, shake_y = easter_egg_manager.get_shake_offset()

            # Apply inverted colors if inverted mode is active
            bg_color = easter_egg_manager.get_inverted_color(COLORS['bg'])
            screen.fill(bg_color)

            # Canvas rendering
            canvas_x = base_canvas_x + zoom_offset_x + shake_x
            canvas_y = base_canvas_y + zoom_offset_y + shake_y

            zoomed_w = int(canvas_manager.width * zoom_level)
            zoomed_h = int(canvas_manager.height * zoom_level)

            # Checkerboard background
            checker_size = 16
            for x in range(0, zoomed_w, checker_size):
                for y in range(0, zoomed_h, checker_size):
                    if (x // checker_size + y // checker_size) % 2 == 0:
                        color = (200, 200, 200) if settings['dark_theme'] else (240, 240, 240)
                    else:
                        color = (180, 180, 180) if settings['dark_theme'] else (220, 220, 220)
                    pygame.draw.rect(screen, color,
                                   (canvas_x + x, canvas_y + y,
                                    min(checker_size, zoomed_w - x),
                                    min(checker_size, zoomed_h - y)))

            # Scale canvas
            if abs(zoom_level - 1.0) > 0.01:
                zoomed_canvas = pygame.transform.smoothscale(canvas_manager.surface,
                                                            (zoomed_w, zoomed_h))
            else:
                zoomed_canvas = canvas_manager.surface
                canvas_x = base_canvas_x
                canvas_y = base_canvas_y

            screen.blit(zoomed_canvas, (canvas_x, canvas_y))

            # Draw all visible overlay layers
            for layer in layer_manager.layers:
                if layer.visible and layer.image:
                    overlay_x = int(canvas_x + layer.pos[0] * zoom_level)
                    overlay_y = int(canvas_y + layer.pos[1] * zoom_level)

                    if abs(zoom_level - 1.0) > 0.01:
                        ow, oh = layer.image.get_size()
                        zoomed_overlay = pygame.transform.smoothscale(
                            layer.image,
                            (int(ow * zoom_level), int(oh * zoom_level))
                        )
                        screen.blit(zoomed_overlay, (overlay_x, overlay_y))
                    else:
                        screen.blit(layer.image, (overlay_x, overlay_y))

            # Canvas border
            pygame.draw.rect(screen, COLORS['border_light'],
                           (canvas_x - 2, canvas_y - 2, zoomed_w + 4, zoomed_h + 4), 2)

            # Grid overlay
            if settings['show_grid'] and zoom_level >= 0.3:
                grid_size = int(settings['grid_size'] * zoom_level)
                grid_color = COLORS['grid']

                for x in range(0, zoomed_w, grid_size):
                    pygame.draw.line(screen, grid_color,
                                   (canvas_x + x, canvas_y),
                                   (canvas_x + x, canvas_y + zoomed_h), 1)
                for y in range(0, zoomed_h, grid_size):
                    pygame.draw.line(screen, grid_color,
                                   (canvas_x, canvas_y + y),
                                   (canvas_x + zoomed_w, canvas_y + y), 1)

            # Shape preview
            if shape_start and tool in ["rect", "line", "circle"]:
                screen_to_canvas_func = get_screen_to_canvas()
                x1, y1 = screen_to_canvas_func(shape_start[0], shape_start[1])
                x2, y2 = screen_to_canvas_func(mx, my)

                if tool == "rect":
                    left = int(min(x1, x2) * zoom_level) + canvas_x
                    top = int(min(y1, y2) * zoom_level) + canvas_y
                    w = int(abs(x2 - x1) * zoom_level)
                    h = int(abs(y2 - y1) * zoom_level)
                    pygame.draw.rect(screen, COLORS['accent_hover'], (left, top, w, h), 3)
                elif tool == "line":
                    sx1 = int(x1 * zoom_level) + canvas_x
                    sy1 = int(y1 * zoom_level) + canvas_y
                    sx2 = int(x2 * zoom_level) + canvas_x
                    sy2 = int(y2 * zoom_level) + canvas_y
                    pygame.draw.line(screen, COLORS['accent_hover'], (sx1, sy1), (sx2, sy2), 3)
                elif tool == "circle":
                    cx = int(x1 * zoom_level) + canvas_x
                    cy = int(y1 * zoom_level) + canvas_y
                    r = int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * zoom_level)
                    if r > 0:
                        pygame.draw.circle(screen, COLORS['accent_hover'], (cx, cy), r, 3)

            # UI elements
            draw_toolbar(screen, WIDTH, canvas_manager.width, canvas_manager.height,
                        len(layer_manager.layers), COLORS, font_large, small_font)
            draw_side_panel(screen, WIDTH, HEIGHT, selected_terrain, tool, brush_size,
                          TERRAINS, COLORS, font, small_font, tiny_font, MIN_BRUSH, MAX_BRUSH)
            
            draw_minimap(screen, canvas_manager.surface, canvas_manager.width,
                        canvas_manager.height, WIDTH, HEIGHT, zoom_level,
                        zoom_offset_x, zoom_offset_y, COLORS, tiny_font,
                        settings.get('show_minimap', True))
            
            screen_to_canvas_func = get_screen_to_canvas()
            visible_layers = sum(1 for layer in layer_manager.layers if layer.visible)
            draw_status_bar(screen, WIDTH, HEIGHT, mx, my, tool, selected_terrain,
                          brush_size, zoom_level, len(layer_manager.layers),
                          visible_layers, unsaved_changes, TERRAINS, COLORS, tiny_font,
                          canvas_manager.width, canvas_manager.height,
                          screen_to_canvas_func, settings.get('show_coordinates', True))
            
            draw_notifications(screen, ui_state, WIDTH, COLORS, small_font)

            # Layer panel
            if show_overlay_controls and layer_manager.layers:
                draw_layer_panel(screen, WIDTH, HEIGHT, layer_manager,
                               COLORS, settings, font_large, small_font, tiny_font, layer_panel_pos)

            # Settings panel
            if show_settings:
                draw_settings_panel(screen, WIDTH, HEIGHT, settings,
                                  COLORS, font_large, font, small_font)

            # Help panel
            if show_help:
                draw_help_panel(screen, WIDTH, HEIGHT, COLORS,
                              font_large, font, tiny_font)

            # Easter egg visual effects
            easter_egg_manager.draw_party_effects(screen, WIDTH, HEIGHT)
            easter_egg_manager.draw_sparkles(screen, WIDTH, HEIGHT)

            canvas_rect = pygame.Rect(canvas_x, canvas_y, zoomed_w, zoomed_h)
            easter_egg_manager.draw_matrix_effect(screen, tiny_font, canvas_rect)

            # Easter egg progress indicator
            if easter_egg_manager.get_discovered_count() > 0:
                progress_msg = easter_egg_manager.get_progress_message()
                progress_color = easter_egg_manager.get_inverted_color(COLORS['accent_hover'])
                progress_surf = tiny_font.render(progress_msg, True, progress_color)
                screen.blit(progress_surf, (WIDTH - progress_surf.get_width() - 20, 95))

        pygame.display.flip()

    # Cleanup
    if settings['auto_save'] and unsaved_changes and canvas_manager:
        save_recovery_file(canvas_manager.surface, canvas_manager.width,
                         canvas_manager.height, settings['last_save_path'])
        print("Work auto-saved to recovery file")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
