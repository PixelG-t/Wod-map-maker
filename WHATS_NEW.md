# What's New in WoD Map Maker v2.5! 🎉

## Major Updates

### 1. ✨ Draggable Layer Manager Panel
**The #1 requested feature is here!**

- **Drag and move** the layer manager window anywhere on screen
- Look for the "⬍ DRAG TO MOVE ⬍" handle at the top of the panel
- Now you can position layers while seeing the full canvas behind them
- No more blocking the view while managing your layers!
- Panel position resets when you close and reopen it

**How to use:**
1. Open Layer Manager (Ctrl+O or click "Layers" button)
2. Click and hold the drag handle at the top
3. Move the panel anywhere you want
4. Continue managing your layers without obstruction!

### 2. 🌟 Animated Welcome Screen
**First impressions matter!**

- Beautiful animated welcome screen greets you on startup
- **25% chance** to see a special Rainbow Edition welcome screen!
- Smooth animations and glowing effects
- Quick feature overview before you start creating

### 3. 🥚 21 Hidden Easter Eggs!
**Can you find them all?** Secret surprises await dedicated users!

[**Full Easter Egg Guide with hints →** See EASTER_EGGS.md](EASTER_EGGS.md)

#### 🎮 Classic & Mouse Challenges (7 eggs)
- **Konami Code** - Party mode with confetti!
- **Corner Master** - Click all 4 canvas corners in order → Disco mode!
- **Nice Coordinates** - (69, 420)
- **The Center** - Middle-click canvas center → Matrix mode!
- **Devil's Coordinates** - (666, 666) → Inverted colors!
- **1337 H4X0R** - Various 1337 coordinates
- **Palindrome** - Matching palindrome coords like (121, 121)

#### 🖌️ Brush Size Secrets (3 eggs)
- **The Answer (42)** - Brush size 42
- **Fibonacci** - Brush sizes 13, 21, 34, 55, 89
- **Binary** - Power of 2 sizes: 16, 32, 64

#### 🎨 Terrain & Painting (3 eggs)
- **Rainbow Sequence** - Water→Plains→Mountain→Forest
- **True Dedication** - Paint for 30 seconds straight
- **Rainbow Painter** - Use all 8 terrain types

#### ⚙️ Tool & Interface (1 egg)
- **Tool Master** - Use all 7 tools → Sparkle mode!

#### 🔍 Zoom Mastery (3 eggs)
- **Pi Precision** - Zoom to 3.14x
- **Zoom Maniac** - Spam zoom 15 times → Screen shake!
- **Golden Ratio** - Zoom to 1.618x (phi)

#### ⏪ Productivity (2 eggs)
- **Undo Master** - Undo 10 times rapidly
- **Save Master** - Save 5 times in 10 seconds

#### 🗺️ Canvas Creation (3 eggs)
- **Lucky 7 Layers** - Have exactly 7 layers
- **Perfect Square** - Create square canvas
- **Meme Canvas** - 420 or 69 in dimensions

**Progress Tracker:** Your Easter egg count appears in the top-right corner!

### 4. 🎬 Enhanced Animations
- Smooth button hover effects
- Animated welcome screen elements
- Glowing title effects
- Particle systems for Easter eggs
- More responsive UI feedback

## Improvements

### Layer Management
- Draggable panel eliminates workflow interruption
- Clear visual feedback when dragging
- Maintains all previous layer functionality
- Easier to position layers precisely

### Visual Polish
- Rainbow effects in special welcome screen
- Confetti particle system
- Matrix rain effect
- Disco mode color cycling
- Smoother transitions throughout

### User Experience
- Welcome screen reduces initial overwhelm
- Easter eggs reward exploration
- More engaging and fun to use
- Professional yet playful

## Tips & Tricks

### Layer Management Workflow
1. Load your reference image (Ctrl+O)
2. Drag the layer panel to the side
3. Adjust opacity to see through the layer
4. Position your reference perfectly
5. Trace or draw with full visibility!

### Easter Egg Hunting
- Check coordinates in the status bar
- Use the zoom display to hit 3.14x exactly
- Use [ and ] keys to fine-tune brush size to 42
- Be creative and explore all features!

### Welcome Screen
- 1 in 4 startups shows the special rainbow edition
- Restart the app to try for the special version
- Triple-click the title for an instant reward!

## Technical Details

### New Files
- `easter_eggs.py` - Easter egg detection and visual effects system (21 eggs!)
- `EASTER_EGGS.md` - Complete Easter egg guide with hints
- `WHATS_NEW.md` - This file!

### Modified Files
- `main.py` - Easter egg integration, welcome screen, draggable panels
- `ui.py` - Welcome screen function, draggable layer panel support
- `layers.py` - (unchanged, ready for future layer history)

### Performance
- Easter egg checks are lightweight
- Visual effects only render when active
- No impact on normal editing performance
- Particle systems use efficient rendering

## Known Issues & Future Ideas

### Coming Soon
- **Layer History/Undo**: Ability to undo layer applications (complex feature, needs more work)
- **More Easter Eggs**: Always room for more surprises!
- **Custom Welcome Messages**: Personalized greetings
- **Achievement System**: Track your artistic journey

### Compatibility
- Requires Pygame 2.0+
- Python 3.7+
- All previous features fully compatible
- Settings files carry forward

## How to Update

If you have a previous version:
1. Backup your existing maps
2. Replace old files with new ones
3. Settings will be preserved
4. Start exploring new features!

## Feedback

Found a bug? Have an idea? Want to share your Easter egg discoveries?
- Open an issue on GitHub
- Share your discoveries with the community!
- Suggest new Easter eggs for future versions

---

**Enjoy the new features!** 🎨✨

Remember: Art is supposed to be fun. That's why we added easter eggs and animations to make your creative process more enjoyable!

**Version 2.5** - "The Fun Update"
Created with ❤️ by wowthat
