# War of Dots Map Editor

A powerful map editor with multi-layer overlay support, modern UI design, and hidden surprises!

![Version](https://img.shields.io/badge/version-2.5-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Easter Eggs](https://img.shields.io/badge/easter_eggs-21-purple.svg)

## 🆕 What's New in v2.5 - "The Fun Update"

- **🎯 Draggable Layer Manager** - Move the layer panel anywhere to see your work!
- **✨ Animated Welcome Screen** - 25% chance for a special rainbow edition
- **🥚 21 Hidden Easter Eggs** - Discover secret features and visual effects!
- **🎬 Enhanced Animations** - Smoother, more engaging UI throughout

[**See WHATS_NEW.md for full details!**](WHATS_NEW.md) | [**Easter Egg Guide →**](EASTER_EGGS.md)

## Features

### Core Features
- **Modern Gradient UI** with smooth animations
- **Draggable Layer Manager** - position it anywhere on screen!
- **Multi-layer overlay system** for precise map building
- **Minimap** for easy navigation when zoomed in
- **8 terrain types** with instant hotkey access
- **7 drawing tools**: Brush, Eraser, Fill, Rectangle, Line, Circle, Color Picker
- **Unlimited undo/redo** (configurable limit)
- **Auto-save** with crash recovery
- **Zoom and pan** with smooth controls
- **Grid overlay** with snap-to-grid option
- **21 Secret Easter Eggs** - find them all for special effects!

### Advanced Features
- **Layer Management**
  - **Draggable layer panel** - move it out of the way!
  - Multiple overlay layers with independent controls
  - Opacity and scale adjustments per layer
  - Layer visibility toggles (Ctrl+Shift+1-9)
  - Drag and position layers precisely
  - Apply layers to canvas or remove them

- **Professional UI**
  - Dark and light theme support
  - Smooth animations and transitions
  - Context-aware tooltips
  - Real-time notifications
  - Keyboard shortcut hints

## Installation

### Requirements
- Python 3.7 or higher
- pygame 2.0+

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/wod-map-editor.git
cd wod-map-editor

# Install dependencies
pip install -r requirements.txt

# Run the editor
python main.py
```

## Usage

### Quick Start
1. Launch the application: `python main.py`
2. Select a canvas size or load an existing map
3. Use the terrain palette to select terrains
4. Draw with the brush tool or use shape tools
5. Save your map with Ctrl+S

### Keyboard Shortcuts

#### Drawing Tools
- `B` - Brush
- `E` - Eraser  
- `F` - Fill bucket
- `R` - Rectangle
- `L` - Line
- `C` - Circle
- `P` - Color picker

#### Layers
- `Ctrl+Shift+1-9` - Toggle overlay layers 1-9
- `V` - Toggle current layer visibility
- `Ctrl+A` - Toggle all layers
- `Ctrl+O` - Open layer manager

#### Canvas
- `1-8` - Select terrain type
- `[` / `]` - Decrease/increase brush size
- `Space+Drag` - Pan canvas
- `Mouse wheel` - Zoom in/out
- `0` - Reset zoom to 100%

#### File Operations
- `Ctrl+S` - Save map
- `Ctrl+N` - New canvas
- `Ctrl+Z` - Undo
- `Ctrl+Y` or `Ctrl+Shift+Z` - Redo
- `H` - Show help/shortcuts
- `Esc` - Close dialogs/exit

### Layer System

The multi-layer overlay system allows you to:
1. Load reference images or artwork
2. Adjust transparency to trace or blend
3. Scale images to fit your canvas
4. Position layers precisely with drag or arrow keys
5. Apply layers to permanently merge with canvas

**Layer Controls:**
- **Add Layer** - Load a new overlay image
- **Toggle** - Show/hide current layer
- **Apply** - Merge layer into canvas
- **Remove** - Delete current layer
- **Opacity slider** - Adjust transparency
- **Scale slider** - Resize the layer

## Terrain Types

1. **Plains** (Green) - Basic terrain
2. **Forest** (Dark Green) - Dense forests
3. **Desert** (Sand) - Desert terrain
4. **Mountain** (Gray) - Rocky mountains
5. **Snow** (White) - Snowy areas
6. **Mud** (Brown) - Muddy ground
7. **Water** (Blue) - Lakes and rivers
8. **Dark Gray** - Special terrain

## Settings

Access settings by clicking the Settings button:
- **Dark Theme** - Toggle between dark and light mode
- **Show Grid** - Display alignment grid
- **Show Minimap** - Show navigation minimap when zoomed
- **Smooth Brush** - Anti-aliased drawing
- **Show Coordinates** - Display mouse position

## File Format

Maps are saved as PNG images:
- Lossless quality preservation
- Compatible with any image viewer
- Can be loaded back into the editor
- Standard format for game engines

## Project Structure

```
wod_map_editor/
├── main.py           # Application entry point
├── config.py         # Settings and constants
├── canvas.py         # Canvas operations
├── layers.py         # Layer management
├── ui.py             # UI rendering
├── utils.py          # Utility functions
├── animation.py      # Animation system
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Tips & Tricks

1. **Use layers for reference** - Load artwork and trace over it
2. **Right-click to pick colors** - Quick color selection from canvas
3. **Hold Space to pan** - Easy navigation while working
4. **Use grid for alignment** - Enable grid and snap-to-grid for precise placement
5. **Adjust brush size quickly** - Use [ and ] keys for fast adjustments
6. **Keyboard terrain selection** - Numbers 1-8 for instant terrain switching

## Auto-Save & Recovery

The editor automatically saves your work:
- Auto-save every 2 minutes (configurable)
- Crash recovery on restart
- Manual save with Ctrl+S clears recovery file

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

MIT License - feel free to use in your projects!

## Author

**wowthat**

## Changelog

### Version 2.5 - "The Fun Update"
- **Draggable layer manager panel** - finally!
- **Animated welcome screen** with 25% special edition variant
- **21 hidden Easter eggs** with special visual effects
- Enhanced animations throughout the UI
- Party mode, disco mode, rainbow brush, matrix rain, inverted colors, screen shake, and sparkles!
- Easter egg progress tracker
- Complete Easter egg guide with hints (EASTER_EGGS.md)
- Improved user experience and engagement
- Better workflow for layer positioning

### Version 2.0
- Added multi-layer overlay system
- New modern gradient UI
- Minimap navigation
- Improved notification system
- Better color schemes
- Enhanced keyboard shortcuts
- Layer hotkeys (Ctrl+Shift+1-9)

### Version 1.0
- Initial release
- Basic drawing tools
- Terrain system
- Save/load functionality

## Support

For issues or questions:
- Open an issue on GitHub
- Check the help dialog in-app (press H)

---

**Enjoy creating awesome maps!** 🗺️
