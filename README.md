Welcome, and first and foremost: if you're on mac os, don't use python3.9. Tkinter no likey. So go ahead and route your interpreter to a homebrew 3.10 & >.

For instance:

```bash
brew install python@3.10
# Then run:
/usr/local/bin/python3.10 main.py
```

(Adjust the exact path as needed, depending on your brew prefix. Some folks may be on /opt/homebrew.)
<br/>
Table of Contents

    About the Program
    Major Features
    Installation & Requirements
    Running the Program
    Tool Summary
    Keyboard Shortcuts
    Pixel Editor (TileEditorWithTools)
    Detailed Walkthrough
    Potential Improvements & Ideas
    Known Caveats & Final Thoughts

<br/>
1. About the Program

This Python/Tkinter application is a Game Boy–style tile generator and map editor. It can:

    Generate 16×16 pixel tiles from a dictionary of 150+ world-building words (like ice, gold, desert, ocean, etc.).
    Apply patterns (e.g., solid, stripes, checkerboard, etc.) and color shifts (hue, saturation, value).
    Store recently generated tiles and let you select or re-select them for painting.
    Provide a map (composed of multiple 16×16 tiles) that you can paint, erase, shape-draw (line, rectangle, circle), or fill with a “bucket” tool.
    Let you sampler-pick (eyedropper) a tile from the map or from within a tile, adding it to your recents.
    Offer an advanced pixel-level editor for any single 16×16 tile, with the same suite of tools (paint, erase, bucket, shapes, sampler, etc.).
    Let you “Gameboy-ize” the entire map (convert all pixels to a simplified or transparent color set).
    Provide Undo/Redo (Cmd+Z, Cmd+Shift+Z on mac) for map editing (and a simpler local undo stack in the pixel editor).

A typical usage scenario:

    Generate new tiles with interesting color patterns from the “Tile Generation” panel.
    Use them to paint onto a map.
    Possibly open the “Pixel Editor” to refine or customize any tile.
    Save or export as needed.

<br/>
2. Major Features

    Massive Dictionary (150+ entries) of terrain/thematic words → color palettes.
    Pattern-based Generation: choose from a variety of pattern functions (solid, stripes, checkerboard, etc.) to fill a tile.
    Hue/Sat/Val sliders: quickly tweak the final tile’s colors.
    Recent Tiles panel: up to 10 tiles stored with hotkeys (1–9, 0).
    Map Editor: paint, erase, select multiple tiles, shape-draw, bucket fill, sampler tool.
    Arrow keys: quickly cycle through dictionary words in word_var.
    Gameboy-ize: recolor all tiles to a classic GB color set, special cases black/white → transparent (#65ff00).
    Undo/Redo: at the map level, storing snapshot states of the entire map_data.
    Pixel-Level Editor: open a dedicated tile editor window, featuring the same suite of tools on a single 16×16 tile.

<br/>
3. Installation & Requirements

    Python 3.10+ is strongly recommended (especially on macOS, as Tkinter can break on older or system Pythons).
    Tkinter must be present (usually standard for most Python distributions).
    Pillow (pip install pillow) for image manipulations.
    If you want to use the “color chooser” in the pixel editor, that’s part of standard Tkinter (colorchooser).

<br/>
4. Running the Program

    Clone or download this repo.
    Ensure main.py and patterns.py plus your large dictionary are present in the same directory.
    In a terminal:

python3 main.py

(Or your homebrew Python 3.10 path.)

    The GUI will open.

<br/>
5. Tool Summary

Within both the main Map Editor and the Pixel Editor, you’ll see these tools (some differences in labeling between the two windows):

    🖌️ Paint
        Use a selected tile for painting onto the map or onto each pixel (in the editor).
        Has a “stroke width” setting that can paint a small block or radius.

    Eraser
        Removes (map context) or sets the pixel to white (tile editor context).

    Select
        (Map) allows multi-cell selection. SHIFT+Select can drag multiple selected.
        (Tile Editor) might let you highlight single pixels, though it is mostly minimal.

    🪣 Bucket
        Fills contiguous area of the same tile (map) or the same color (tile editor).

    📏 Line

    ▭ Rect

    ⚪ Circle
        In the map, these draw the shape on the map (applying the selected tile with a certain stroke).
        In the tile editor, they draw lines/pixels in the local 16×16 tile.

    👁️ Sampler
        Eyedropper: pick a tile from the map (or pixel color in the tile editor) and add it to recents or set your paint color.
        In the main map, it picks entire 16×16 tiles. In the tile editor, it picks single-pixel colors.

<br/>
6. Keyboard Shortcuts

    Enter: Generate a new tile from the current word/pattern/slider settings.
    Arrow Left/Right/Up/Down: Cycle word_var among dictionary words. Right/Left = ±1, Up/Down = ±10.
    1..9,0: Select a recent tile (0 = 10th slot).
    Delete: Erase selected tile(s) in the map.
    Cmd+Z: Undo the last action in the map.
    Cmd+Shift+Z: Redo.
    e: Edit the selected tile in “Recent Tiles” with the pixel-level editor.

<br/>
7. Pixel Editor (TileEditorWithTools)

When you press “Edit Selected Tile” in the main window or double-click a tile in “Recent Tiles,” the Pixel Editor appears:

    A 16×16 grid of squares, each representing one pixel of the tile.
    Tools mirrored from the main map (paint, erase, bucket, shapes, sampler).
    You can paint continuously by holding the mouse down and dragging, same as in the main map.
    A small, floating “cursor ghost” appears in Paint mode to indicate where you’re about to paint.
    The “Sampler” picks a pixel’s color.
    A “stroke width” for shapes/painting.
    Undo/Redo just for that single tile (cmd+z / cmd+shift+z).
    “Pick Color” button: opens a color chooser to let you pick a custom color to paint with.
    Press “Save” to apply changes back to the main app’s selected tile. Press “Cancel” or close to discard.

<br/>
8. Detailed Walkthrough

    Generating Tiles
        In the left panel: Type a word in the “Word” field or cycle with arrow keys.
        Adjust “Pattern” from the drop-down, tweak Hue/Sat/Val, then press “Generate” (or press Enter).
        A new 16×16 tile preview appears.
        This tile is also added to the “Recent Tiles” row, up to 10 slots, with hotkeys 1–9,0.

    Selecting a Tile
        Click a tile in the “Recent Tiles” row. The code highlights it in red and sets it as your “selected tile.”
        If your last tool was “Select,” the program automatically changes your tool to “Paint.”

    Map Editing
        Tools are at the bottom-left or middle-left. For example, choose 🖌️ “Paint,” then click or drag on the map to paint your selected tile.
        SHIFT+Select: drag multiple selected tiles around.
        Bucket: fill contiguous tiles on the map with your selected tile.
        Shapes: line, rect, circle (with “stroke width”).
        Sampler (👁️): pick a tile from the map and add it to recents.

    Gameboy-ize
        Press the “Gameboy-ize Map” button.
        Each tile is scanned pixel by pixel, mapping it to a limited color set or special transparent color for black/white.

    Undo/Redo
        On the main map, each paint/erase/bucket/shape places a new snapshot in the undo stack. Press Cmd+Z to revert, Cmd+Shift+Z to go forward.

    Editing a Recent Tile
        Either press “Edit Selected Tile” or double-click the tile’s thumbnail in recents.
        The Pixel Editor (TileEditorWithTools) opens. Tools appear at the top, a 16×16 grid in the center, and “Pick Color,” “Save,” “Cancel” at the bottom.
        Paint, erase, shapes, sampler, etc., all on a per-pixel basis.
        “Save” updates the tile in recents. “Cancel” discards changes.

<br/>
9. Potential Improvements & Ideas

    Layering: In the main map, you could introduce separate layers for collision or meta info.
    Bigger map: The current code handles a map up to ~500×500 tiles, but storing large undo snapshots can be memory-heavy. One might adopt a more delta-based approach.
    Additional tile transformations: rotation, flipping, random noise, fractal patterns.
    Multi-tile shapes: e.g., polygon fills, text overlays, stamp patterns.
    Advanced “Gameboy-ize”: let the user define a custom color set or add dithering.
    Export entire tile dictionary: generate a sprite sheet from all 150 dictionary words.
    Saving/Loading map**: store the entire layout in JSON or a custom format for reloading.
    Pixel Editor advanced: multi-layer editing, infinite undo, color indexing, alpha channel, etc.

<br/>
10. Known Caveats & Final Thoughts

    Memory usage: Undo snapshots store the entire map_data. A large map with many steps might become memory-intensive.
    Tkinter coordinate extremes: for extremely big map sizes, scrolling might slow down.
    No concurrency: everything is single-threaded; painting large shapes or gameboy-izing huge maps can block the UI briefly.
    Pixel Editor is single-tile only (16×16). For larger custom images, you’d need a more robust editor or the main map approach.

That said, this app is a powerful example of bridging procedural tile generation with interactive map painting plus a mini pixel-level editor. We hope you enjoy hacking on it to produce a wide variety of 2D “Game Boy–style” assets for your game or creative projects!
<br/>

Thanks for taking a peek, and remember: if you’re on macOS, route your Python to 3.10 or above. Enjoy the tile generation, map building, shape drawing, pixel editing, and all the other creative possibilities. Have fun!
