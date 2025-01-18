#!/opt/homebrew/bin/python3.10

"""
Author: 10x Senior Architect Megalord Oversigma Gigachad Engineer
Description:
  This script generates 16x16 tiles based on a word entered (e.g., 'grass', 'rock', 'ocean').
  It uses a large dictionary (150+ entries) of world-building words mapped to color palettes.
  A user can preview the tile in a Tkinter GUI, tweak color palettes using basic sliders,
  and export the tile as a .png. Perfect for Game Boy Color-style 2D world map building.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
from PIL import Image, ImageTk, ImageDraw
from patterns import PATTERN_GENERATORS
import copy

TK_SILENCE_DEPRECATION = 1

# -----------------------------------------------------------------------------
# 1) Massive World-Building Dictionary with 150+ Entries
#    Each key is a terrain or thematic word, mapped to a list of sample RGB color tuples.
# -----------------------------------------------------------------------------

TILE_COLOR_DICTIONARY = {
    "grass":        [(34,139,34), (50,205,50), (0,128,0), (124,252,0)],
    "rock":         [(112,128,144), (119,136,153), (105,105,105), (128,128,128)],
    "ocean":        [(0,105,148), (0,128,255), (28,107,160), (25,25,112)],
    "desert":       [(237,201,175), (210,180,140), (244,164,96), (222,184,135)],
    "forest":       [(34,139,34), (0,100,0), (27,94,32), (46,139,87)],
    "mountain":     [(139,137,137), (205,201,201), (169,169,169), (188,184,177)],
    "hills":        [(85,107,47), (107,142,35), (143,188,143), (154,205,50)],
    "stone":        [(120,120,120), (140,140,140), (110,110,110), (90,90,90)],
    "gravel":       [(128,128,128), (153,153,153), (102,102,102), (77,77,77)],
    "mud":          [(70,50,30), (60,40,20), (80,60,40), (100,80,60)],
    "snow":         [(255,250,250), (240,248,255), (245,245,245), (230,230,230)],
    "ice":          [(176,224,230), (173,216,230), (224,255,255), (240,255,255)],
    "glass":        [(180,180,255), (200,200,255), (220,220,255), (240,240,255)],
    "lava":         [(255,69,0), (255,140,0), (255,0,0), (139,0,0)],
    "sand":         [(194,178,128), (238,214,175), (244,164,96), (210,180,140)],
    "cliff":        [(139,137,137), (160,160,160), (190,190,190), (211,211,211)],
    "snowy":        [(248,248,255), (240,255,255), (245,245,245), (230,230,230)],
    "volcano":      [(139,0,0), (205,38,38), (255,69,0), (105,105,105)],
    "river":        [(0,191,255), (30,144,255), (70,130,180), (25,25,112)],
    "riverbank":    [(34,139,34), (50,205,50), (139,69,19), (210,180,140)],
    "basalt":       [(70,70,70), (90,90,90), (50,50,50), (30,30,30)],
    "marble":       [(220,220,220), (255,250,250), (245,245,245), (230,230,230)],
    "metal":        [(192,192,192), (169,169,169), (128,128,128), (255,215,0)],
    "iron":         [(188,188,188), (183,183,183), (160,160,160), (130,130,130)],
    "gold":         [(255,215,0), (238,201,0), (218,165,32), (184,134,11)],
    "silver":       [(192,192,192), (211,211,211), (169,169,169), (128,128,128)],
    "lapis":        [(38,97,156), (25,25,112), (0,0,139), (0,0,205)],
    "emerald":      [(0,201,87), (0,139,69), (0,255,127), (46,139,87)],
    "diamond":      [(185,242,255), (224,255,255), (175,238,238), (176,224,230)],
    "obsidian":     [(53,56,57), (35,38,39), (27,29,30), (70,70,90)],
    "netherrack":   [(96,35,35), (125,45,45), (74,22,22), (50,10,10)],
    "endstone":     [(218,210,158), (232,224,174), (211,203,146), (190,182,122)],
    "pebble":       [(139,137,137), (160,160,160), (120,120,120), (105,105,105)],
    "coral":        [(255,127,80), (255,160,122), (240,128,128), (233,150,122)],
    "sponge":       [(255,255,128), (255,255,153), (240,230,140), (238,232,170)],
    "kelp":         [(34,139,34), (0,128,0), (85,107,47), (46,139,87)],
    "seaweed":      [(46,139,87), (0,100,0), (0,128,0), (60,179,113)],
    "fossil":       [(210,180,140), (205,133,63), (222,184,135), (139,69,19)],
    "boulder":      [(128,128,128), (105,105,105), (119,136,153), (112,128,144)],
    "slate":        [(112,128,144), (47,79,79), (69,90,100), (70,70,70)],
    "clay":         [(221,221,221), (205,201,201), (196,196,196), (169,169,169)],
    "terra":        [(139,69,19), (160,82,45), (210,105,30), (188,143,143)],
    "cobblestone":  [(120,120,120), (90,90,90), (100,100,100), (130,130,130)],
    "brick":        [(178,34,34), (165,42,42), (139,0,0), (150,40,40)],
    "roof":         [(139,69,19), (105,105,105), (165,42,42), (128,128,128)],
    "wood":         [(139,69,19), (160,82,45), (205,133,63), (222,184,135)],
    "plank":        [(181,101,29), (210,105,30), (153,76,0), (139,69,19)],
    "tree":         [(34,139,34), (0,128,0), (139,69,19), (160,82,45)],
    "leaves":       [(0,100,0), (34,139,34), (50,205,50), (107,142,35)],
    "cactus":       [(0,100,0), (34,139,34), (60,179,113), (107,142,35)],
    "mushroom":     [(139,69,19), (222,184,135), (255,0,0), (240,230,140)],
    "fire":         [(255,0,0), (255,69,0), (255,140,0), (255,215,0)],
    "magma":        [(255,69,0), (255,140,0), (220,20,60), (178,34,34)],
    "acid":         [(173,255,47), (127,255,0), (202,255,112), (143,188,143)],
    "poison":       [(127,255,0), (110,139,61), (50,205,50), (154,205,50)],
    "toxic":        [(0,255,127), (46,139,87), (173,255,47), (127,255,0)],
    "radioactive":  [(0,250,154), (0,255,127), (127,255,0), (189,183,107)],
    "plague":       [(128,0,0), (139,0,0), (165,42,42), (178,34,34)],
    "light":        [(255,255,224), (255,255,240), (250,250,210), (255,250,205)],
    "dark":         [(25,25,25), (50,50,50), (75,75,75), (0,0,0)],
    "shadow":       [(40,40,40), (60,60,60), (80,80,80), (0,0,0)],
    "portal":       [(138,43,226), (75,0,130), (148,0,211), (153,50,204)],
    "magic":        [(186,85,211), (218,112,214), (147,112,219), (138,43,226)],
    "arcane":       [(72,61,139), (106,90,205), (123,104,238), (147,112,219)],
    "rune":         [(225,225,255), (200,200,255), (175,175,230), (150,150,205)],
    "glyph":        [(255,228,225), (255,240,245), (238,221,130), (218,112,214)],
    "enchanted":    [(128,0,128), (186,85,211), (216,191,216), (199,21,133)],
    "fairy":        [(255,182,193), (255,192,203), (255,228,225), (255,240,245)],
    "pixie":        [(255,228,225), (255,182,193), (255,105,180), (255,20,147)],
    "sprite":       [(173,216,230), (135,206,250), (135,206,235), (176,196,222)],
    "spirit":       [(211,211,255), (170,170,255), (192,192,192), (224,255,255)],
    "ghost":        [(245,245,245), (230,230,230), (211,211,211), (192,192,192)],
    "grave":        [(60,60,60), (45,45,45), (30,30,30), (90,90,90)],
    "tomb":         [(70,70,70), (100,100,100), (130,130,130), (153,153,153)],
    "crypt":        [(50,50,50), (70,70,70), (90,90,90), (100,100,100)],
    "bone":         [(245,245,220), (255,228,196), (255,239,213), (240,230,140)],
    "skull":        [(215,215,215), (192,192,192), (169,169,169), (245,245,245)],
    "flesh":        [(255,160,122), (255,127,80), (255,99,71), (250,128,114)],
    "blood":        [(139,0,0), (178,34,34), (220,20,60), (255,0,0)],
    "carrion":      [(128,0,0), (139,0,0), (165,42,42), (178,34,34)],
    "sandstone":    [(216,179,140), (237,201,175), (255,228,196), (210,180,140)],
    "limestone":    [(230,230,220), (224,224,214), (211,211,185), (200,200,175)],
    "granite":      [(143,143,143), (155,155,155), (165,168,170), (175,175,175)],
    "meteor":       [(105,105,105), (119,136,153), (128,128,128), (178,34,34)],
    "asteroid":     [(70,70,70), (90,90,90), (110,110,110), (130,130,130)],
    "cosmic":       [(72,61,139), (75,0,130), (106,90,205), (123,104,238)],
    "star":         [(255,255,224), (255,250,205), (240,230,140), (255,215,0)],
    "nebula":       [(147,112,219), (138,43,226), (186,85,211), (218,112,214)],
    "galaxy":       [(25,25,112), (72,61,139), (106,90,205), (138,43,226)],
    "planet":       [(154,205,50), (233,150,122), (210,105,30), (160,82,45)],
    "grassland":    [(124,252,0), (127,255,0), (0,250,154), (50,205,50)],
    "savanna":      [(210,180,140), (222,184,135), (238,232,170), (189,183,107)],
    "jungle":       [(0,100,0), (34,139,34), (85,107,47), (46,139,87)],
    "rainforest":   [(34,139,34), (0,128,0), (60,179,113), (123,153,34)],
    "wetland":      [(107,142,35), (154,205,50), (0,191,255), (70,130,180)],
    "swamp":        [(47,79,79), (85,107,47), (50,205,50), (0,100,0)],
    "bog":          [(80,100,60), (70,80,50), (85,107,47), (65,80,45)],
    "marsh":        [(100,120,70), (90,110,60), (107,142,35), (154,205,50)],
    "tundra":       [(230,230,250), (240,255,255), (245,245,245), (220,220,220)],
    "iceberg":      [(173,216,230), (224,255,255), (240,255,255), (176,224,230)],
    "frozen":       [(176,224,230), (173,216,230), (224,255,255), (220,220,255)],
    "arctic":       [(245,245,255), (240,255,255), (230,230,250), (255,250,250)],
    "underwater":   [(0,105,148), (0,128,255), (70,130,180), (25,25,112)],
    "deepsea":      [(25,25,112), (0,0,128), (0,0,139), (0,100,160)],
    "reef":         [(255,160,122), (255,127,80), (46,139,87), (0,128,128)],
    "shore":        [(210,180,140), (238,214,175), (70,130,180), (25,25,112)],
    "beach":        [(238,214,175), (222,184,135), (240,230,140), (70,130,180)],
    "volcanic":     [(105,105,105), (139,0,0), (205,38,38), (70,70,70)],
    "ash":          [(80,80,80), (100,100,100), (120,120,120), (140,140,140)],
    "charred":      [(60,60,60), (80,80,80), (100,100,100), (120,120,120)],
    "burnt":        [(139,69,19), (160,82,45), (105,105,105), (70,70,70)],
    "crystal":      [(224,255,255), (175,238,238), (176,224,230), (173,216,230)],
    "ruby":         [(224,17,95), (227,11,93), (178,34,34), (139,0,0)],
    "sapphire":     [(15,82,186), (0,0,139), (25,25,112), (0,0,205)],
    "amethyst":     [(153,102,204), (138,43,226), (186,85,211), (123,104,238)],
    "quartz":       [(255,255,255), (245,245,245), (240,240,240), (230,230,230)],
    "opal":         [(168,195,188), (178,223,238), (224,255,255), (152,251,152)],
    "pearl":        [(234,224,200), (255,239,219), (255,245,238), (245,245,245)],
    "enigma":       [(75,0,130), (106,90,205), (72,61,139), (128,0,128)],
    "mystic":       [(138,43,226), (148,0,211), (186,85,211), (153,50,204)],
    "mythic":       [(199,21,133), (218,112,214), (255,105,180), (219,112,147)],
    "legend":       [(255,215,0), (238,221,130), (189,183,107), (218,165,32)],
    "relic":        [(184,134,11), (218,165,32), (205,133,63), (139,69,19)],
    "artifact":     [(220,220,220), (245,245,245), (192,192,192), (255,250,240)],
    "ancient":      [(205,133,63), (160,82,45), (139,69,19), (110,40,19)],
    "future":       [(192,192,192), (211,211,211), (60,60,60), (128,128,128)],
    "cyber":        [(0,255,255), (0,250,154), (127,255,212), (0,255,127)],
    "tech":         [(105,105,105), (128,128,128), (192,192,192), (220,220,220)],
    "robotic":      [(200,200,200), (169,169,169), (105,105,105), (255,215,0)],
    "mechanical":   [(139,137,137), (160,160,160), (190,190,190), (218,165,32)],
    "steam":        [(169,169,169), (211,211,211), (192,192,192), (205,201,201)],
    "clockwork":    [(205,201,201), (192,192,192), (218,165,32), (184,134,11)],
    "brass":        [(181,166,66), (205,127,50), (184,134,11), (218,165,32)],
    "ironwork":     [(188,188,188), (169,169,169), (192,192,192), (128,128,128)],
    "wire":         [(90,90,90), (130,130,130), (160,160,160), (192,192,192)],
    "circuit":      [(0,255,127), (127,255,0), (46,139,87), (60,179,113)],
    "chip":         [(192,192,192), (128,128,128), (72,61,139), (255,255,224)],
    "binary":       [(0,0,0), (255,255,255), (32,32,32), (224,224,224)],
    "digital":      [(0,255,255), (127,255,212), (255,255,0), (124,252,0)],
    "virtual":      [(186,85,211), (147,112,219), (0,255,255), (173,216,230)],
    "hologram":     [(102,205,170), (0,255,255), (127,255,212), (0,206,209)],
    "mirror":       [(245,245,245), (224,224,224), (211,211,211), (192,192,192)],
    "glassland":    [(180,180,255), (200,200,255), (220,220,255), (240,240,255)],
    "translucent":  [(255,255,255), (240,248,255), (224,255,255), (248,248,255)],
    "phantom":      [(119,136,153), (105,105,105), (40,40,40), (70,70,70)],
    "ethereal":     [(224,255,255), (255,250,240), (250,240,230), (230,230,250)],
    "celestial":    [(135,206,235), (176,196,222), (220,220,255), (192,192,255)],
    "astral":       [(123,104,238), (106,90,205), (72,61,139), (138,43,226)],
    "heaven":       [(240,255,255), (224,255,255), (255,255,240), (255,250,250)],
    "hell":         [(139,0,0), (178,34,34), (255,0,0), (70,70,70)],
    "demon":        [(178,34,34), (139,0,0), (70,70,70), (40,40,40)],
    "angel":        [(255,255,224), (255,250,205), (245,245,245), (224,255,255)],
    "seraph":       [(255,245,238), (255,250,250), (230,230,250), (255,250,205)],
    "dragon":       [(139,0,0), (205,38,38), (85,107,47), (46,139,87)],
    "wyvern":       [(46,139,87), (0,128,128), (60,179,113), (34,139,34)],
    "drake":        [(128,0,0), (178,34,34), (50,50,50), (60,60,60)],
    "hydra":        [(0,100,0), (0,139,139), (60,179,113), (107,142,35)],
    "serpent":      [(0,128,128), (0,100,0), (85,107,47), (128,0,0)],
    "worm":         [(160,82,45), (139,69,19), (128,0,0), (184,134,11)],
    "golem":        [(100,100,100), (130,130,130), (160,160,160), (70,70,70)],
    "construct":    [(139,137,137), (120,120,120), (90,90,90), (180,180,180)],
    "automaton":    [(192,192,192), (169,169,169), (128,128,128), (105,105,105)],
    "puppet":       [(210,180,140), (139,69,19), (160,82,45), (100,80,60)],
    "homunculus":   [(255,160,122), (205,133,63), (139,69,19), (178,34,34)],
    "borg":         [(128,128,128), (192,192,192), (0,255,0), (0,128,0)],
    "biomech":      [(139,69,19), (160,82,45), (192,192,192), (128,128,128)],
    "biotech":      [(107,142,35), (0,128,0), (127,255,0), (60,179,113)],
    "gene":         [(144,238,144), (152,251,152), (124,252,0), (0,255,127)],
    "DNA":          [(255,0,255), (186,85,211), (147,112,219), (138,43,226)],
    "virus":        [(128,0,0), (178,34,34), (220,20,60), (255,69,0)],
    "bacteria":     [(189,183,107), (143,188,143), (127,255,0), (173,255,47)],
    "fungus":       [(139,69,19), (222,184,135), (154,205,50), (107,142,35)],
    "algae":        [(0,128,128), (0,100,0), (34,139,34), (46,139,87)],
    "lichen":       [(107,142,35), (143,188,143), (154,205,50), (85,107,47)],
    "mold":         [(96,128,56), (85,107,47), (110,139,61), (34,139,34)],
    "yeast":        [(255,255,224), (255,250,205), (255,245,238), (253,245,230)],
    "petri":        [(211,211,211), (255,255,224), (127,255,212), (127,255,0)],
    "lab":          [(192,192,192), (211,211,211), (220,220,220), (240,248,255)],
    "science":      [(173,216,230), (176,196,222), (224,255,255), (0,255,255)],
    "alchemy":      [(238,221,130), (218,165,32), (184,134,11), (245,245,220)],
    "potion":       [(255,20,147), (218,112,214), (186,85,211), (147,112,219)],
    "tonic":        [(0,255,127), (60,179,113), (127,255,212), (255,105,180)],
    "elixir":       [(255,69,0), (255,140,0), (0,255,255), (173,216,230)],
    "brew":         [(139,69,19), (160,82,45), (222,184,135), (210,105,30)],
    "mix":          [(255,192,203), (219,112,147), (186,85,211), (0,255,127)],
    "amalgam":      [(255,215,0), (255,140,0), (220,20,60), (138,43,226)]
}

# -----------------------------------------------------------------------------
# 2) Utility Functions
# -----------------------------------------------------------------------------

import math
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw
import copy

# from patterns import PATTERN_GENERATORS
# from your_dictionary_module import TILE_COLOR_DICTIONARY
#   (We assume the big dictionary is defined above.)

def get_color_palette(word: str):
    """
    Return 4-color palette for a word or default to 'grass' if not found.
    """
    return TILE_COLOR_DICTIONARY.get(word.lower(), TILE_COLOR_DICTIONARY["grass"])

def generate_16x16_tile_with_pattern(palette,
                                     pattern_name="solid",
                                     hue_shift=0.0,
                                     sat_mult=1.0,
                                     val_mult=1.0):
    """
    Generate a 16x16 Pillow Image using the specified pattern & adjusted palette.
    """
    from colorsys import rgb_to_hsv, hsv_to_rgb

    tile = Image.new("RGB", (16,16))
    draw = ImageDraw.Draw(tile)

    adjusted = []
    for (r,g,b) in palette:
        h,s,v = rgb_to_hsv(r/255,g/255,b/255)
        h=(h+hue_shift)%1.0
        s=min(max(s*sat_mult,0),1)
        v=min(max(v*val_mult,0),1)
        nr,ng,nb = hsv_to_rgb(h,s,v)
        adjusted.append((int(nr*255),int(ng*255),int(nb*255)))

    from patterns import PATTERN_GENERATORS
    pattern_func = PATTERN_GENERATORS.get(pattern_name.lower(), PATTERN_GENERATORS["solid"])
    pattern_func(draw, adjusted)
    return tile


# -----------------------------------------------------------------------------
# Pixel Editor with Full Tools
# -----------------------------------------------------------------------------

class TileEditorWithTools(tk.Toplevel):
    """
    A 'mini map editor' for a single 16×16 tile:
      - Tools: paint, erase, select, bucket, line, rect, circle, sampler
      - Continuous paint
      - Floating tile cursor for paint (optionally not for sampler, to match your design)
      - Double-click or 'enter' to finalize? We'll do a separate "Save" button.
    """

    TOOL_PAINT   = "🖌️"
    TOOL_ERASE   = "Eraser"
    TOOL_SELECT  = "Select"
    TOOL_BUCKET  = "🪣"
    TOOL_LINE    = "📏"
    TOOL_RECT    = "▭"
    TOOL_CIRCLE  = "⚪"
    TOOL_SAMPLER = "👁️"

    def __init__(self, parent, tile_pil, on_save_callback):
        """
        parent: main window
        tile_pil: 16x16 PIL Image (RGB)
        on_save_callback: function(new_pil) -> saves result
        """
        super().__init__(parent)
        self.title("Tile Editor - Full Tools")
        self.resizable(False, False)

        # Keep a local 16x16 "map_data" approach?
        # We can store each pixel as a (r,g,b). For simplicity, store just a PIL Image.
        self.tile_pil = tile_pil.convert("RGB").copy()
        self.on_save_callback = on_save_callback

        # We'll have an internal canvas 16*16 "pixel_size" => let's do 20 px per pixel
        self.pixel_size = 20
        self.width_px = 16
        self.height_px = 16

        # Tools
        self.current_tool = tk.StringVar(value=self.TOOL_PAINT)
        self.stroke_width_var = tk.IntVar(value=1)
        # We can do "select" or "sampler" if we like, but let's keep them minimal or replicate.

        self.selected_color = (255,0,0)  # default painting color
        self.cursor_ghost_id = None
        self.dragging = False
        self.last_cell = None
        self.shape_start_cell = None
        self.selected_cells = set()
        self.shift_down = False  # if user wants line from last click, etc. we can do advanced?

        # We'll store an internal "undo_stack" for the tile. Or keep it simpler?
        self.undo_stack = []
        self.redo_stack = []

        # Build UI
        self.create_widgets()
        self.load_tile_into_canvas()

        # Keybind
        self.setup_keybindings()

        # record initial state
        self.record_undo()

    def create_widgets(self):
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # Tools bar
        tk.Label(top_frame, text="Tool:").pack(side=tk.LEFT)
        for t in [self.TOOL_PAINT, self.TOOL_ERASE, self.TOOL_SELECT,
                  self.TOOL_BUCKET, self.TOOL_LINE, self.TOOL_RECT,
                  self.TOOL_CIRCLE, self.TOOL_SAMPLER]:
            tk.Radiobutton(top_frame, text=t, variable=self.current_tool,
                           value=t).pack(side=tk.LEFT, padx=2)

        # stroke
        tk.Label(top_frame, text="Stroke:").pack(side=tk.LEFT)
        tk.Spinbox(top_frame, from_=1, to=10, textvariable=self.stroke_width_var, width=3).pack(side=tk.LEFT)

        # color pick
        tk.Button(top_frame, text="Pick Color", command=self.pick_color).pack(side=tk.LEFT, padx=5)

        # Canvas
        self.canvas = tk.Canvas(self, width=self.width_px*self.pixel_size,
                                     height=self.height_px*self.pixel_size,
                                     bg="white")
        self.canvas.pack()

        # Buttons: Save / Cancel
        bot_frame = tk.Frame(self)
        bot_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        tk.Button(bot_frame, text="Save", command=self.save_and_close).pack(side=tk.RIGHT, padx=5)
        tk.Button(bot_frame, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=5)

        # Bind mouse
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Motion>", self.on_canvas_motion)
        # Possibly handle double-click for shapes?

    def setup_keybindings(self):
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Command-z>", self.on_undo)
        self.bind("<Command-Shift-z>", self.on_redo)
        self.bind("<Command-Z>", self.on_undo)
        self.bind("<Command-Shift-Z>", self.on_redo)
        self.bind("<Return>", lambda e: self.save_and_close())

    def pick_color(self):
        c = colorchooser.askcolor(color=self._rgb_to_hex(self.selected_color), title="Pick a Color")
        if c and c[0]:
            self.selected_color = (int(c[0][0]), int(c[0][1]), int(c[0][2]))

    def load_tile_into_canvas(self):
        """
        Draw each pixel as a small rectangle.
        """
        self.canvas.delete("all")
        pix = self.tile_pil.load()
        for y in range(16):
            for x in range(16):
                color = pix[x,y]
                x0 = x*self.pixel_size
                y0 = y*self.pixel_size
                x1 = x0+self.pixel_size
                y1 = y0+self.pixel_size
                self.canvas.create_rectangle(x0,y0,x1,y1,
                                             fill=self._rgb_to_hex(color),
                                             outline="", tags="pixel")

    def _update_pixel(self, x, y, color):
        """
        Set pixel x,y to color in self.tile_pil, update canvas.
        """
        if x<0 or x>=16 or y<0 or y>=16: return
        self.tile_pil.putpixel((x,y), color)
        x0 = x*self.pixel_size
        y0 = y*self.pixel_size
        x1 = x0+self.pixel_size
        y1 = y0+self.pixel_size
        self.canvas.create_rectangle(x0,y0,x1,y1, fill=self._rgb_to_hex(color), outline="")

    def on_canvas_click(self, event):
        px,py = event.x, event.y
        cx, cy = px//self.pixel_size, py//self.pixel_size
        tool = self.current_tool.get()

        if tool==self.TOOL_LINE or tool==self.TOOL_RECT or tool==self.TOOL_CIRCLE:
            self.shape_start_cell=(cx,cy)
            return

        if not (0<=cx<16 and 0<=cy<16):
            return

        if tool==self.TOOL_PAINT:
            self._do_paint_pixel(cx,cy)
            self.record_undo()
        elif tool==self.TOOL_ERASE:
            self._do_erase_pixel(cx,cy)
            self.record_undo()
        elif tool==self.TOOL_SELECT:
            # not super meaningful in a single tile context,
            # but we can store selected pixel in a set.
            self.selected_cells.clear()
            self.selected_cells.add((cx,cy))
        elif tool==self.TOOL_BUCKET:
            self._do_bucket(cx,cy)
            self.record_undo()
        elif tool==self.TOOL_SAMPLER:
            c = self.tile_pil.getpixel((cx,cy))
            self.selected_color = c
        self.last_cell=(cx,cy)

    def on_canvas_drag(self,event):
        px,py = event.x, event.y
        cx,cy = px//self.pixel_size, py//self.pixel_size
        tool=self.current_tool.get()

        if tool in (self.TOOL_LINE,self.TOOL_RECT,self.TOOL_CIRCLE):
            return

        if 0<=cx<16 and 0<=cy<16 and (cx,cy)!=self.last_cell:
            if tool==self.TOOL_PAINT:
                self._do_paint_pixel(cx,cy)
            elif tool==self.TOOL_ERASE:
                self._do_erase_pixel(cx,cy)
            elif tool==self.TOOL_BUCKET:
                # Typically, bucket is single-click
                pass
            elif tool==self.TOOL_SAMPLER:
                pass
            self.last_cell=(cx,cy)

    def on_canvas_release(self,event):
        tool = self.current_tool.get()
        if tool in (self.TOOL_LINE,self.TOOL_RECT,self.TOOL_CIRCLE):
            if self.shape_start_cell:
                px,py = event.x, event.y
                cx,cy = px//self.pixel_size, py//self.pixel_size
                sx,sy = self.shape_start_cell
                self._do_shape(tool, sx,sy, cx,cy)
                self.record_undo()
            self.shape_start_cell=None
        self.last_cell=None

    def on_canvas_motion(self,event):
        """
        Show a floating 'cursor ghost' if tool==paint (and maybe sampler).
        We'll skip sampler if you want no ghost.
        """
        tool=self.current_tool.get()
        if tool==self.TOOL_PAINT:
            px,py = event.x, event.y
            if not self.cursor_ghost_id:
                # create
                ghost = self.canvas.create_rectangle(px-5,py-5,px+5,py+5,
                                                     outline="red", width=1,
                                                     tags="cursor_ghost")
                self.cursor_ghost_id=ghost
            else:
                # move
                self.canvas.coords(self.cursor_ghost_id, px-5,py-5,px+5,py+5)
        else:
            if self.cursor_ghost_id:
                self.canvas.delete(self.cursor_ghost_id)
                self.cursor_ghost_id=None

    # -------------------------------------------------------------------------
    # Paint / Erase / Bucket / shape
    # -------------------------------------------------------------------------
    def _do_paint_pixel(self,x,y):
        stroke = self.stroke_width_var.get()
        rad = (stroke-1)//2
        for dy in range(-rad,rad+1):
            for dx in range(-rad,rad+1):
                nx, ny = x+dx, y+dy
                if 0<=nx<16 and 0<=ny<16:
                    self._update_pixel(nx,ny,self.selected_color)

    def _do_erase_pixel(self,x,y):
        stroke=self.stroke_width_var.get()
        rad=(stroke-1)//2
        for dy in range(-rad,rad+1):
            for dx in range(-rad,rad+1):
                nx, ny = x+dx,y+dy
                if 0<=nx<16 and 0<=ny<16:
                    self._update_pixel(nx,ny,(255,255,255))  # "erasing" => set to white?

    def _do_bucket(self,cx,cy):
        orig = self.tile_pil.getpixel((cx,cy))
        if orig==self.selected_color:
            return
        w,h=16,16
        st=[(cx,cy)]
        visited=set()
        while st:
            x,y=st.pop()
            if (x,y) in visited: continue
            visited.add((x,y))
            if 0<=x<w and 0<=y<h:
                c = self.tile_pil.getpixel((x,y))
                if c==orig:
                    self._update_pixel(x,y,self.selected_color)
                    st.append((x-1,y))
                    st.append((x+1,y))
                    st.append((x,y-1))
                    st.append((x,y+1))

    def _do_shape(self, tool, sx,sy, ex,ey):
        stroke=self.stroke_width_var.get()
        if tool==self.TOOL_LINE:
            self._draw_line(sx,sy,ex,ey,stroke)
        elif tool==self.TOOL_RECT:
            self._draw_rect(sx,sy,ex,ey,stroke)
        elif tool==self.TOOL_CIRCLE:
            self._draw_circle(sx,sy,ex,ey,stroke)

    def _draw_line(self,sx,sy,ex,ey,stroke):
        dx=abs(ex-sx)
        dy=abs(ey-sy)
        x,y=sx,sy
        sxn=1 if ex>sx else -1
        syn=1 if ey>sy else -1
        err=dx-dy
        rad=(stroke-1)//2
        while True:
            for rdy in range(-rad,rad+1):
                for rdx in range(-rad,rad+1):
                    nx=x+rdx
                    ny=y+rdy
                    if 0<=nx<16 and 0<=ny<16:
                        self._update_pixel(nx,ny,self.selected_color)
            if x==ex and y==ey:
                break
            e2=2*err
            if e2> -dy:
                err-=dy
                x+=sxn
            if e2< dx:
                err+=dx
                y+=syn

    def _draw_rect(self,sx,sy,ex,ey,stroke):
        x1,y1=min(sx,ex), min(sy,ey)
        x2,y2=max(sx,ex), max(sy,ey)
        rad=(stroke-1)//2
        def paint_cell(cx,cy):
            if 0<=cx<16 and 0<=cy<16:
                self._update_pixel(cx,cy,self.selected_color)
        for cx in range(x1,x2+1):
            for thick in range(-rad,rad+1):
                paint_cell(cx,y1+thick)
                paint_cell(cx,y2+thick)
        for cy in range(y1,y2+1):
            for thick in range(-rad,rad+1):
                paint_cell(x1+thick,cy)
                paint_cell(x2+thick,cy)

    def _draw_circle(self,sx,sy,ex,ey,stroke):
        x1,y1=min(sx,ex),min(sy,ey)
        x2,y2=max(sx,ex),max(sy,ey)
        w=x2-x1
        h=y2-y1
        cx=(x1+x2)/2
        cy=(y1+y2)/2
        rx=w/2
        ry=h/2
        rad=(stroke-1)//2
        steps=int(360*max(w,h))
        for step in range(steps+1):
            if steps==0: break
            theta=2*math.pi*step/steps
            fx=cx+rx*math.cos(theta)
            fy=cy+ry*math.sin(theta)
            tx,ty=int(round(fx)),int(round(fy))
            for rdy in range(-rad,rad+1):
                for rdx in range(-rad,rad+1):
                    nx=tx+rdx
                    ny=ty+rdy
                    if 0<=nx<16 and 0<=ny<16:
                        self._update_pixel(nx,ny,self.selected_color)

    # -------------------------------------------------------------------------
    # Undo/Redo
    # -------------------------------------------------------------------------
    def record_undo(self):
        st = self.tile_pil.copy()
        self.undo_stack.append(st)
        self.redo_stack.clear()

    def on_undo(self,e=None):
        if len(self.undo_stack)>1:
            self.redo_stack.append(self.undo_stack.pop())
            top = self.undo_stack[-1]
            self.tile_pil=top.copy()
            self.load_tile_into_canvas()
        else:
            messagebox.showinfo("Undo","No more steps.")

    def on_redo(self,e=None):
        if self.redo_stack:
            st = self.redo_stack.pop()
            self.undo_stack.append(self.tile_pil.copy())
            self.tile_pil=st.copy()
            self.load_tile_into_canvas()
        else:
            messagebox.showinfo("Redo","No redo steps available.")

    # -------------------------------------------------------------------------
    # Save / Cancel
    # -------------------------------------------------------------------------
    def save_and_close(self):
        if self.on_save_callback:
            self.on_save_callback(self.tile_pil)
        self.destroy()

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    def _rgb_to_hex(self, rgb):
        return "#%02x%02x%02x"%(rgb[0],rgb[1],rgb[2])


# -----------------------------------------------------------------------------
# 3) Main Application
# -----------------------------------------------------------------------------

class TileGeneratorApp(tk.Tk):
    """
    Updated features:
    - Tools: Paint(🖌️), Eraser(Eraser), Select("Select"), Bucket(🪣), Line(📏), Rect(▭), Circle(⚪), Sampler(👁️).
    - No tile preview cursor for Sampler (👁️).
    - Press Enter => generate tile immediately.
    - Arrow keys => cycle dictionary words (word_var).
    - Undo/Redo with Cmd+Z/Cmd+Shift+Z.
    - "Gameboy-ize" button.
    - "Edit Selected Tile" button in Recent Tiles => opens PixelEditor for 16x16 edit.
    """

    def __init__(self):
        super().__init__()
        self.title("16x16 Tile Generator - Extended Features")
        self.resizable(True, True)

        # Tools
        self.TOOL_PAINT   = "🖌️"
        self.TOOL_ERASE   = "Eraser"
        self.TOOL_SELECT  = "Select"   # spelled out
        self.TOOL_BUCKET  = "🪣"
        self.TOOL_LINE    = "📏"
        self.TOOL_RECT    = "▭"
        self.TOOL_CIRCLE  = "⚪"
        self.TOOL_SAMPLER = "👁️"

        self.current_tool = tk.StringVar(value=self.TOOL_PAINT)
        self.current_tool.trace_add("write", self.on_tool_changed)

        self.word_var = tk.StringVar(value="grass")
        self.pattern_var = tk.StringVar(value="solid")
        self.hue_shift_var = tk.DoubleVar(value=0.0)
        self.sat_var = tk.DoubleVar(value=1.0)
        self.val_var = tk.DoubleVar(value=1.0)

        self.generated_tile_pil = None

        self.recent_tiles = []
        self.selected_recent_tile_index = None
        self.selected_tile_image = None

        # Build dictionary key list for arrow cycling
        self.dict_keys = sorted(TILE_COLOR_DICTIONARY.keys())
        self.dict_index = self.dict_keys.index("grass") if "grass" in self.dict_keys else 0

        self.tile_size = 16
        self.map_width = 16
        self.map_height = 16
        self.map_data = [[None for _ in range(self.map_width)] for _ in range(self.map_height)]

        self.shift_down = False
        self.ctrl_down = False
        self.selected_cells = set()

        self.dragging_multi = False
        self.drag_origin_cell = None
        self.drag_ghost_ids = []
        self.multi_offsets = []
        self.last_cell = None
        self.shape_start_cell = None
        self.stroke_width_var = tk.IntVar(value=1)

        # Cursor ghost
        self.cursor_ghost_id = None

        # Undo/Redo
        self.undo_stack = []
        self.redo_stack = []

        self.create_widgets()
        self.setup_keybindings()

        self.record_undo_state()  # initial state in undo stack

    # -------------------------------------------------------------------------
    # UI
    # -------------------------------------------------------------------------
    def create_widgets(self):
        container = tk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(container, borderwidth=2, relief=tk.RAISED)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        right_frame = tk.Frame(container)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.build_tile_generator_ui(left_frame)
        self.build_recent_tiles_ui(left_frame)
        self.build_map_controls_ui(left_frame)
        self.build_scrollable_map(right_frame)

    def build_tile_generator_ui(self, parent):
        frame = tk.LabelFrame(parent, text="Tile Generation", padx=5, pady=5)
        frame.pack(fill=tk.X, pady=5)

        # Word
        tk.Label(frame, text="Word:").grid(row=0, column=0, sticky="e")
        word_entry = tk.Entry(frame, textvariable=self.word_var, width=12)
        word_entry.grid(row=0, column=1, padx=5, pady=2)

        from patterns import PATTERN_GENERATORS
        patterns = sorted(PATTERN_GENERATORS.keys())

        # Pattern
        tk.Label(frame, text="Pattern:").grid(row=1, column=0, sticky="e")
        cb = ttk.Combobox(frame, textvariable=self.pattern_var,
                          values=patterns, state="readonly", width=10)
        cb.grid(row=1, column=1, padx=5, pady=2)

        # Hue, Sat, Val
        tk.Label(frame, text="Hue Shift:").grid(row=2, column=0, sticky="e")
        ttk.Scale(frame, from_=0.0, to=1.0, variable=self.hue_shift_var,
                  orient="horizontal", length=100,
                  command=lambda x: self.update_preview()).grid(row=2, column=1)

        tk.Label(frame, text="Sat Mult:").grid(row=3, column=0, sticky="e")
        ttk.Scale(frame, from_=0.0, to=2.0, variable=self.sat_var,
                  orient="horizontal", length=100,
                  command=lambda x: self.update_preview()).grid(row=3, column=1)

        tk.Label(frame, text="Val Mult:").grid(row=4, column=0, sticky="e")
        ttk.Scale(frame, from_=0.0, to=2.0, variable=self.val_var,
                  orient="horizontal", length=100,
                  command=lambda x: self.update_preview()).grid(row=4, column=1)

        # Generate
        tk.Button(frame, text="Generate", command=self.generate_tile).grid(row=5, column=0, columnspan=2, pady=4)

        # Preview
        self.preview_label = tk.Label(frame, text="No Tile", width=12, height=12)
        self.preview_label.grid(row=6, column=0, columnspan=2, pady=4)

        # Export single tile
        tk.Button(frame, text="Export Single Tile", command=self.export_generated_tile).grid(row=7, column=0, columnspan=2, pady=4)

    def build_recent_tiles_ui(self, parent):
        # "Recent Tiles" + "Edit Selected Tile" button
        self.recent_frame = tk.LabelFrame(parent, text="Recent Tiles", padx=5, pady=5)
        self.recent_frame.pack(fill=tk.X, pady=5)

        # A small button for "Edit Selected Tile"
        # We'll place it below the row
        edit_btn = tk.Button(parent, text="Edit Selected Tile", command=self.edit_selected_tile)
        edit_btn.pack(pady=5)

    def build_map_controls_ui(self, parent):
        frame = tk.LabelFrame(parent, text="Map & Tools", padx=5, pady=5)
        frame.pack(fill=tk.X, pady=5)

        # Tools
        tk.Label(frame, text="Tool:").grid(row=0, column=0, sticky="e")
        tool_options = [
            (self.TOOL_PAINT,   self.TOOL_PAINT),
            (self.TOOL_ERASE,   self.TOOL_ERASE),
            (self.TOOL_SELECT,  self.TOOL_SELECT),
            (self.TOOL_BUCKET,  self.TOOL_BUCKET),
            (self.TOOL_LINE,    self.TOOL_LINE),
            (self.TOOL_RECT,    self.TOOL_RECT),
            (self.TOOL_CIRCLE,  self.TOOL_CIRCLE),
            (self.TOOL_SAMPLER, self.TOOL_SAMPLER),
        ]
        col_idx = 1
        for label_txt, val in tool_options:
            ttk.Radiobutton(frame, text=label_txt, variable=self.current_tool, value=val).grid(row=0, column=col_idx, sticky="w")
            col_idx+=1

        # stroke
        tk.Label(frame, text="Stroke Width:").grid(row=1, column=0, sticky="e")
        tk.Spinbox(frame, from_=1, to=10, textvariable=self.stroke_width_var, width=5).grid(row=1, column=1, padx=2)

        # map dims
        tk.Label(frame, text="Width (tiles):").grid(row=2, column=0, sticky="e")
        self.map_width_var = tk.IntVar(value=16)
        tk.Spinbox(frame, from_=4, to=500, textvariable=self.map_width_var, width=5).grid(row=2, column=1, padx=2)

        tk.Label(frame, text="Height (tiles):").grid(row=2, column=2, sticky="e")
        self.map_height_var = tk.IntVar(value=16)
        tk.Spinbox(frame, from_=4, to=500, textvariable=self.map_height_var, width=5).grid(row=2, column=3, padx=2)

        tk.Button(frame, text="Resize Map", command=self.resize_map).grid(row=2, column=4, padx=5)

        # export map
        tk.Button(frame, text="Export Map to PNG", command=self.export_map).grid(row=3, column=0, columnspan=5, pady=4)
        # export selected tile
        tk.Button(frame, text="Export Selected Tile", command=self.export_selected_tile).grid(row=4, column=0, columnspan=5, pady=4)

        # gameboy-ize
        tk.Button(frame, text="Gameboy-ize Map", command=self.gameboyize_map).grid(row=5, column=0, columnspan=5, pady=4)

    def build_scrollable_map(self, parent):
        x_scroll = tk.Scrollbar(parent, orient=tk.HORIZONTAL)
        y_scroll = tk.Scrollbar(parent, orient=tk.VERTICAL)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.map_canvas = tk.Canvas(parent,
                                    width=self.map_width*self.tile_size,
                                    height=self.map_height*self.tile_size,
                                    xscrollcommand=x_scroll.set,
                                    yscrollcommand=y_scroll.set)
        self.map_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        x_scroll.config(command=self.map_canvas.xview)
        y_scroll.config(command=self.map_canvas.yview)

        self.map_canvas.config(scrollregion=(0,0,
                                             self.map_width*self.tile_size,
                                             self.map_height*self.tile_size))

        self.map_canvas.bind("<Button-1>", self.on_map_click)
        self.map_canvas.bind("<B1-Motion>", self.on_map_drag)
        self.map_canvas.bind("<ButtonRelease-1>", self.on_map_release)
        self.map_canvas.bind("<Motion>", self.on_map_motion)

        self.draw_map_grid()

    # -------------------------------------------------------------------------
    # Edit Selected Tile in Recent Tiles
    # -------------------------------------------------------------------------
    def edit_selected_tile(self):
        """
        If we have a tile selected in "recent_tiles",
        open a PixelEditor window to modify it.
        """
        if self.selected_recent_tile_index is None:
            messagebox.showinfo("No Recent Tile", "Please select a tile from Recent Tiles first.")
            return
        tile_data = self.recent_tiles[self.selected_recent_tile_index]
        # tile_data = (PIL, tk_img, container)
        tile_pil = tile_data[0]

        def on_save(new_pil):
            """
            Callback from PixelEditor, user saved.
            We update the tile in the recent list, refresh the UI.
            """
            # update the tile
            new_tk = ImageTk.PhotoImage(new_pil.resize((32,32), Image.NEAREST))
            self.recent_tiles[self.selected_recent_tile_index] = (new_pil, new_tk, None)
            self.refresh_recent_tiles_ui()
            messagebox.showinfo("Pixel Editor", "Tile updated successfully!")

        PixelEditor(self, tile_pil, on_save)

    # -------------------------------------------------------------------------
    # Key Bindings
    # -------------------------------------------------------------------------
    def setup_keybindings(self):
        # normal
        for i in map(str, range(1,10)):
            self.bind(i, self.on_recent_hotkey)
        self.bind("0", self.on_recent_hotkey)
        self.bind("<Return>", lambda e: self.generate_tile())
        self.bind("<Right>", self.on_key_right)
        self.bind("<Left>", self.on_key_left)
        self.bind("<Up>", self.on_key_up)
        self.bind("<Down>", self.on_key_down)
        # e => edit selected tile
        self.bind("e", lambda e: self.edit_selected_recent_tile())

        # undo/redo
        self.bind_all("<Command-z>", self.on_undo)
        self.bind_all("<Command-Shift-z>", self.on_redo)
        self.bind_all("<Command-Z>", self.on_undo)
        self.bind_all("<Command-Shift-Z>", self.on_redo)

        # SHIFT/CTRL
        self.bind("<Shift_L>", self.on_shift_pressed)
        self.bind("<Shift_R>", self.on_shift_pressed)
        self.bind("<KeyRelease-Shift_L>", self.on_shift_released)
        self.bind("<KeyRelease-Shift_R>", self.on_shift_released)
        self.bind("<Control_L>", self.on_ctrl_pressed)
        self.bind("<Control_R>", self.on_ctrl_pressed)
        self.bind("<KeyRelease-Control_L>", self.on_ctrl_released)
        self.bind("<KeyRelease-Control_R>", self.on_ctrl_released)
        # Delete
        self.bind("<Delete>", self.on_delete_key)

    def build_recent_tiles_ui(self, parent):
        self.recent_frame = tk.LabelFrame(parent, text="Recent Tiles", padx=5, pady=5)
        self.recent_frame.pack(fill=tk.X, pady=5)

        # Edit button
        tk.Button(parent, text="Edit Selected Tile", command=self.edit_selected_recent_tile).pack(pady=5)

    def refresh_recent_tiles_ui(self):
        for w in self.recent_frame.winfo_children():
            w.destroy()

        for i,(pil_img,tki,_) in enumerate(self.recent_tiles):
            cont = tk.Frame(self.recent_frame, borderwidth=2, relief=tk.RIDGE)
            cont.grid(row=0,column=i,padx=2)

            lbl = tk.Label(cont, image=tki)
            lbl.pack()
            # single click => select
            lbl.bind("<Button-1>", lambda e, idx=i: self.select_recent_tile(idx))
            # double click => open editor
            lbl.bind("<Double-Button-1>", lambda e, idx=i: self.open_tile_editor(idx))

            digit = "0" if i==9 else str(i+1)
            digit_lbl = tk.Label(cont, text=digit, fg="yellow", bg="black", font=("TkDefaultFont",8))
            digit_lbl.place(relx=1.0,rely=0.0,anchor="ne")

            if self.selected_recent_tile_index==i:
                cont.config(relief=tk.SOLID, bd=2, highlightcolor="red", highlightthickness=2)

            self.recent_tiles[i] = (pil_img,tki,cont)

    # 'Edit Selected Tile' button or pressing "e"
    def edit_selected_recent_tile(self):
        if self.selected_recent_tile_index is None:
            messagebox.showinfo("No Tile","Please select a tile in recent first.")
            return
        self.open_tile_editor(self.selected_recent_tile_index)

    def open_tile_editor(self, idx):
        if idx<0 or idx>=len(self.recent_tiles): return
        tile_pil = self.recent_tiles[idx][0]

        def on_save(new_pil):
            # update
            new_tk = ImageTk.PhotoImage(new_pil.resize((32,32), Image.NEAREST))
            self.recent_tiles[idx] = (new_pil, new_tk, None)
            self.refresh_recent_tiles_ui()
            messagebox.showinfo("Pixel Editor","Tile updated!")
        # open
        TileEditorWithTools(self, tile_pil, on_save)

    def on_recent_hotkey(self, event):
        key = event.keysym
        if key=="0":
            idx=9
        else:
            idx=int(key)-1
        if 0<=idx<len(self.recent_tiles):
            self.select_recent_tile(idx)

    # Arrow keys => cycle dictionary
    def on_key_right(self, event):
        self.dict_index = (self.dict_index+1)%len(self.dict_keys)
        self.word_var.set(self.dict_keys[self.dict_index])

    def on_key_left(self, event):
        self.dict_index = (self.dict_index-1)%len(self.dict_keys)
        self.word_var.set(self.dict_keys[self.dict_index])

    def on_key_up(self, event):
        self.dict_index = (self.dict_index+10)%len(self.dict_keys)
        self.word_var.set(self.dict_keys[self.dict_index])

    def on_key_down(self, event):
        self.dict_index = (self.dict_index-10)%len(self.dict_keys)
        self.word_var.set(self.dict_keys[self.dict_index])

    # Undo/Redo
    def on_undo(self, event=None):
        if len(self.undo_stack)>1:
            # push current to redo
            self.redo_stack.append(self.undo_stack.pop())
            state = self.undo_stack[-1]
            self.load_undo_state(state)
        else:
            messagebox.showinfo("Undo", "No more undo steps.")

    def on_redo(self, event=None):
        if self.redo_stack:
            state = self.redo_stack.pop()
            self.undo_stack.append(copy.deepcopy(self.map_data))
            self.load_undo_state(state)
        else:
            messagebox.showinfo("Redo","No redo steps available.")

    def record_undo_state(self):
        st = copy.deepcopy(self.map_data)
        self.undo_stack.append(st)
        self.redo_stack.clear()

    def load_undo_state(self, state):
        self.map_data = copy.deepcopy(state)
        self.map_canvas.delete("all")
        self.draw_map_grid()
        for r in range(self.map_height):
            for c in range(self.map_width):
                cell = self.map_data[r][c]
                if cell:
                    pil_img = cell["image_pil"]
                    x0 = c*self.tile_size
                    y0 = r*self.tile_size
                    tki = ImageTk.PhotoImage(pil_img)
                    cid = self.map_canvas.create_image(x0,y0,image=tki,anchor=tk.NW)
                    self.map_canvas.image[cid] = tki
                    self.map_data[r][c]={"image_pil": pil_img,"canvas_id":cid}

    # -------------------------------------------------------------------------
    # Generate Tile
    # -------------------------------------------------------------------------
    def generate_tile(self):
        w = self.word_var.get().strip()
        if w.lower() in self.dict_keys:
            self.dict_index = self.dict_keys.index(w.lower())

        pat = self.pattern_var.get().strip()
        pal = get_color_palette(w)

        tile_pil = generate_16x16_tile_with_pattern(
            pal,
            pattern_name=pat,
            hue_shift=self.hue_shift_var.get(),
            sat_mult=self.sat_var.get(),
            val_mult=self.val_var.get()
        )
        self.generated_tile_pil = tile_pil
        self.update_preview(tile_pil)
        self.add_to_recent_tiles(tile_pil)

    def update_preview(self, tile_pil):
        tki = ImageTk.PhotoImage(tile_pil.resize((96,96),Image.NEAREST))
        self.preview_label.config(image=tki,text="")
        self.preview_label.image=tki

    def add_to_recent_tiles(self, tile_pil):
        tki = ImageTk.PhotoImage(tile_pil.resize((32,32),Image.NEAREST))
        self.recent_tiles.insert(0,(tile_pil,tki,None))
        if len(self.recent_tiles)>10:
            self.recent_tiles.pop()
        self.refresh_recent_tiles_ui()

    def refresh_recent_tiles_ui(self):
        for w in self.recent_frame.winfo_children():
            w.destroy()

        for i,(pil_img,tki,_) in enumerate(self.recent_tiles):
            cont = tk.Frame(self.recent_frame, borderwidth=2, relief=tk.RIDGE)
            cont.grid(row=0,column=i,padx=2)

            lbl = tk.Label(cont, image=tki)
            lbl.pack()
            lbl.bind("<Button-1>", lambda e, idx=i: self.select_recent_tile(idx))

            digit = "0" if i==9 else str(i+1)
            digit_lbl = tk.Label(cont, text=digit, fg="yellow", bg="black", font=("TkDefaultFont",8))
            digit_lbl.place(relx=1.0,rely=0.0,anchor="ne")

            if self.selected_recent_tile_index==i:
                cont.config(relief=tk.SOLID, bd=2, highlightcolor="red", highlightthickness=2)

            self.recent_tiles[i] = (pil_img,tki,cont)

    def select_recent_tile(self, idx):
        if idx<0 or idx>=len(self.recent_tiles): return
        old_tool = self.current_tool.get()
        self.selected_recent_tile_index = idx
        self.selected_tile_image = self.recent_tiles[idx][0]

        # only if old_tool == "Select" => switch to Paint
        if old_tool==self.TOOL_SELECT:
            self.current_tool.set(self.TOOL_PAINT)

        self.refresh_recent_tiles_ui()

    def export_generated_tile(self):
        if not self.generated_tile_pil:
            messagebox.showwarning("No Tile","Generate a tile first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG Files","*.png")],
                                            title="Save Generated Tile")
        if not path:
            return
        self.generated_tile_pil.save(path,"PNG")
        messagebox.showinfo("Saved", f"Tile saved to {path}")

    # -------------------------------------------------------------------------
    # Map
    # -------------------------------------------------------------------------
    def build_map(self):
        self.map_data=[[None for _ in range(self.map_width)] for _ in range(self.map_height)]
        self.map_canvas.config(width=self.map_width*self.tile_size,
                               height=self.map_height*self.tile_size)
        self.map_canvas.config(scrollregion=(0,0,self.map_width*self.tile_size,
                                             self.map_height*self.tile_size))
        self.map_canvas.delete("all")
        self.draw_map_grid()

    def resize_map(self):
        w = self.map_width_var.get()
        h = self.map_height_var.get()
        if w<1 or h<1:
            messagebox.showerror("Invalid Size","Width/Height must be > 0.")
            return
        self.map_width = w
        self.map_height = h
        self.build_map()
        self.selected_cells.clear()
        self.record_undo_state()

    def draw_map_grid(self):
        for x in range(0,self.map_width*self.tile_size,self.tile_size):
            self.map_canvas.create_line(x,0,x,self.map_height*self.tile_size,
                                        fill="#cccccc",tags="grid")
        for y in range(0,self.map_height*self.tile_size,self.tile_size):
            self.map_canvas.create_line(0,y,self.map_width*self.tile_size,y,
                                        fill="#cccccc",tags="grid")

    # -------------------------------------------------------------------------
    # Tools
    # -------------------------------------------------------------------------
    def on_tool_changed(self,*args):
        newt = self.current_tool.get()
        # leaving "Select"
        if newt!=self.TOOL_SELECT and self.selected_cells:
            self.selected_cells.clear()
            self.redraw_selection()
        # remove cursor ghost
        self.remove_cursor_ghost()

    # -------------------------------------------------------------------------
    # Canvas
    # -------------------------------------------------------------------------
    def on_map_motion(self,event):
        px = self.map_canvas.canvasx(event.x)
        py = self.map_canvas.canvasy(event.y)
        tool = self.current_tool.get()
        # If tool=Paint & we have selected tile => show ghost
        if tool==self.TOOL_PAINT and self.selected_tile_image:
            if not self.cursor_ghost_id:
                tki = ImageTk.PhotoImage(self.selected_tile_image)
                gid = self.map_canvas.create_image(px,py,image=tki,anchor=tk.CENTER,tags="cursor_ghost")
                self.map_canvas.image = getattr(self.map_canvas,"image",{})
                self.map_canvas.image[gid]=tki
                self.cursor_ghost_id=gid
            else:
                self.map_canvas.coords(self.cursor_ghost_id, px, py)
        else:
            self.remove_cursor_ghost()

    def remove_cursor_ghost(self):
        if self.cursor_ghost_id:
            self.map_canvas.delete(self.cursor_ghost_id)
            self.cursor_ghost_id=None

    def on_map_click(self,event):
        self.map_canvas.focus_set()
        px = self.map_canvas.canvasx(event.x)
        py = self.map_canvas.canvasy(event.y)
        cx, cy = int(px//self.tile_size), int(py//self.tile_size)

        # shape tool?
        if self.current_tool.get() in (self.TOOL_LINE,self.TOOL_RECT,self.TOOL_CIRCLE):
            self.shape_start_cell = (cx,cy)
            return

        if not (0<=cx<self.map_width and 0<=cy<self.map_height):
            self.last_cell=None
            return

        tool = self.current_tool.get()

        # SHIFT+Select => multi-drag
        if self.shift_down and tool==self.TOOL_SELECT:
            if not self.selected_cells: return
            self.dragging_multi=True
            self.drag_origin_cell=(cx,cy)
            self.multi_offsets=[]
            self.drag_ghost_ids=[]
            for(scx,scy) in self.selected_cells:
                d=self.map_data[scy][scx]
                if not d: continue
                dx=scx-cx
                dy=scy-cy
                self.multi_offsets.append((scx,scy,dx,dy,d["image_pil"]))
                self.map_canvas.delete(d["canvas_id"])
                self.map_data[scy][scx]=None
            for(_,_,dx,dy,pilimg) in self.multi_offsets:
                tki=ImageTk.PhotoImage(pilimg)
                gx=px+dx*self.tile_size
                gy=py+dy*self.tile_size
                gid=self.map_canvas.create_image(gx,gy,image=tki,anchor=tk.CENTER)
                self.map_canvas.image[gid]=tki
                self.drag_ghost_ids.append(gid)
            return

        # sampler => pick tile, add to recent, switch to paint
        if tool==self.TOOL_SAMPLER:
            cell=self.map_data[cy][cx]
            if cell:
                self.add_to_recent_tiles(cell["image_pil"])
            self.current_tool.set(self.TOOL_PAINT)
            return

        # paint/erase/select/bucket
        self.do_tool_action(cx,cy,tool,is_drag=False)
        self.last_cell=(cx,cy)

    def on_map_drag(self,event):
        if self.dragging_multi and self.drag_ghost_ids:
            px=self.map_canvas.canvasx(event.x)
            py=self.map_canvas.canvasy(event.y)
            for i,(_,_,dx,dy,pilimg) in enumerate(self.multi_offsets):
                gid=self.drag_ghost_ids[i]
                self.map_canvas.coords(gid, px+dx*self.tile_size, py+dy*self.tile_size)
            return

        if self.current_tool.get() in (self.TOOL_LINE,self.TOOL_RECT,self.TOOL_CIRCLE):
            return

        px=self.map_canvas.canvasx(event.x)
        py=self.map_canvas.canvasy(event.y)
        cx,cy=int(px//self.tile_size), int(py//self.tile_size)
        if 0<=cx<self.map_width and 0<=cy<self.map_height:
            if (cx,cy)!=self.last_cell:
                self.do_tool_action(cx,cy,self.current_tool.get(),True)
                self.last_cell=(cx,cy)

    def on_map_release(self,event):
        if self.dragging_multi and self.drag_ghost_ids:
            self.dragging_multi=False
            px=self.map_canvas.canvasx(event.x)
            py=self.map_canvas.canvasy(event.y)
            cx,cy=int(px//self.tile_size), int(py//self.tile_size)
            for gid in self.drag_ghost_ids:
                self.map_canvas.delete(gid)
            self.drag_ghost_ids=[]
            dx2 = cx-self.drag_origin_cell[0]
            dy2 = cy-self.drag_origin_cell[1]
            newsel=set()
            for(ocx,ocy,dx,dy,pilimg) in self.multi_offsets:
                ncx=ocx+dx2
                ncy=ocy+dy2
                if 0<=ncx<self.map_width and 0<=ncy<self.map_height:
                    tki=ImageTk.PhotoImage(pilimg)
                    x0=ncx*self.tile_size
                    y0=ncy*self.tile_size
                    cid=self.map_canvas.create_image(x0,y0,image=tki,anchor=tk.NW)
                    self.map_canvas.image[cid]=tki
                    self.map_data[ncy][ncx]={"image_pil":pilimg,"canvas_id":cid}
                    newsel.add((ncx,ncy))
            self.selected_cells=newsel
            self.redraw_selection()
            self.multi_offsets=[]
            self.drag_origin_cell=None
            self.record_undo_state()

        # shapes
        if self.current_tool.get() in (self.TOOL_LINE,self.TOOL_RECT,self.TOOL_CIRCLE):
            if self.shape_start_cell:
                px=self.map_canvas.canvasx(event.x)
                py=self.map_canvas.canvasy(event.y)
                ecx, ecy=int(px//self.tile_size), int(py//self.tile_size)
                sx,sy=self.shape_start_cell
                self.draw_shape(self.current_tool.get(), sx,sy,ecx,ecy)
                self.record_undo_state()
            self.shape_start_cell=None

        self.last_cell=None

    def do_tool_action(self, cx, cy, tool, is_drag=False):
        if tool==self.TOOL_PAINT:
            self.paint_tile(cx,cy)
            if not is_drag:
                self.record_undo_state()
        elif tool==self.TOOL_ERASE:
            self.erase_tile(cx,cy)
            if not is_drag:
                self.record_undo_state()
        elif tool==self.TOOL_SELECT:
            self.select_tile(cx,cy)
        elif tool==self.TOOL_BUCKET and not is_drag:
            self.bucket_fill(cx,cy)
            self.record_undo_state()
        else:
            pass

    # Paint, Erase, Select, Bucket
    def paint_tile(self,cx,cy):
        if not self.selected_tile_image:return
        stroke=self.stroke_width_var.get()
        rad=(stroke-1)//2
        for dy in range(-rad,rad+1):
            for dx in range(-rad,rad+1):
                nx=cx+dx
                ny=cy+dy
                if 0<=nx<self.map_width and 0<=ny<self.map_height:
                    self._place_pil_at(nx,ny,self.selected_tile_image)

    def erase_tile(self,cx,cy):
        stroke=self.stroke_width_var.get()
        rad=(stroke-1)//2
        for dy in range(-rad,rad+1):
            for dx in range(-rad,rad+1):
                nx=cx+dx
                ny=cy+dy
                if 0<=nx<self.map_width and 0<=ny<self.map_height:
                    old=self.map_data[ny][nx]
                    if old:
                        self.map_canvas.delete(old["canvas_id"])
                    self.map_data[ny][nx]=None

    def select_tile(self,cx,cy):
        if self.ctrl_down:
            if (cx,cy) in self.selected_cells:
                self.selected_cells.remove((cx,cy))
            else:
                self.selected_cells.add((cx,cy))
        else:
            self.selected_cells.clear()
            self.selected_cells.add((cx,cy))
        self.redraw_selection()

    def redraw_selection(self):
        self.map_canvas.delete("selection_rect")
        for (scx,scy) in self.selected_cells:
            x0=scx*self.tile_size
            y0=scy*self.tile_size
            x1=x0+self.tile_size
            y1=y0+self.tile_size
            self.map_canvas.create_rectangle(x0,y0,x1,y1,
                                             outline="red",width=2,
                                             tags="selection_rect")

    def bucket_fill(self,cx,cy):
        if not self.selected_tile_image:return
        orig = self.map_data[cy][cx]
        orig_ref= orig["image_pil"] if orig else None
        if orig_ref==self.selected_tile_image: return

        st=[(cx,cy)]
        visited=set()
        while st:
            x,y=st.pop()
            if (x,y) in visited: continue
            visited.add((x,y))
            if 0<=x<self.map_width and 0<=y<self.map_height:
                cell=self.map_data[y][x]
                c_ref= cell["image_pil"] if cell else None
                if c_ref==orig_ref:
                    self._place_pil_at(x,y,self.selected_tile_image)
                    st.append((x-1,y))
                    st.append((x+1,y))
                    st.append((x,y-1))
                    st.append((x,y+1))

    def _place_pil_at(self,cx,cy,tile_pil):
        old=self.map_data[cy][cx]
        if old:
            self.map_canvas.delete(old["canvas_id"])
        x0=cx*self.tile_size
        y0=cy*self.tile_size
        tki=ImageTk.PhotoImage(tile_pil)
        cid=self.map_canvas.create_image(x0,y0,image=tki,anchor=tk.NW)
        self.map_canvas.image=getattr(self.map_canvas,"image",{})
        self.map_canvas.image[cid]=tki
        self.map_data[cy][cx]={"image_pil":tile_pil,"canvas_id":cid}

    # Shapes: line, rect, circle
    def draw_shape(self, shape_tool, sx, sy, ex, ey):
        stroke=self.stroke_width_var.get()
        if shape_tool==self.TOOL_LINE:
            self._draw_line_shape(sx,sy,ex,ey,stroke)
        elif shape_tool==self.TOOL_RECT:
            self._draw_rect_shape(sx,sy,ex,ey,stroke)
        elif shape_tool==self.TOOL_CIRCLE:
            self._draw_circle_shape(sx,sy,ex,ey,stroke)

    def _draw_line_shape(self,sx,sy,ex,ey,stroke):
        dx=abs(ex-sx)
        dy=abs(ey-sy)
        x,y=sx,sy
        sxn=1 if ex>sx else -1
        syn=1 if ey>sy else -1
        err=dx-dy
        rad=(stroke-1)//2
        while True:
            for rdy in range(-rad,rad+1):
                for rdx in range(-rad,rad+1):
                    nx=x+rdx
                    ny=y+rdy
                    if 0<=nx<self.map_width and 0<=ny<self.map_height and self.selected_tile_image:
                        self._place_pil_at(nx,ny,self.selected_tile_image)
            if x==ex and y==ey: break
            e2=2*err
            if e2> -dy:
                err-=dy
                x+=sxn
            if e2<dx:
                err+=dx
                y+=syn

    def _draw_rect_shape(self,sx,sy,ex,ey,stroke):
        x1,y1=min(sx,ex),min(sy,ey)
        x2,y2=max(sx,ex),max(sy,ey)
        rad=(stroke-1)//2
        def paint_cell(cx,cy):
            if 0<=cx<self.map_width and 0<=cy<self.map_height and self.selected_tile_image:
                self._place_pil_at(cx,cy,self.selected_tile_image)
        for cx in range(x1,x2+1):
            for thick in range(-rad,rad+1):
                paint_cell(cx,y1+thick)
                paint_cell(cx,y2+thick)
        for cy in range(y1,y2+1):
            for thick in range(-rad,rad+1):
                paint_cell(x1+thick,cy)
                paint_cell(x2+thick,cy)

    def _draw_circle_shape(self,sx,sy,ex,ey,stroke):
        x1,y1=min(sx,ex),min(sy,ey)
        x2,y2=max(sx,ex),max(sy,ey)
        w=x2-x1
        h=y2-y1
        cx=(x1+x2)/2
        cy=(y1+y2)/2
        rx=w/2
        ry=h/2
        rad=(stroke-1)//2
        def paint_cell(nx,ny):
            if 0<=nx<self.map_width and 0<=ny<self.map_height and self.selected_tile_image:
                self._place_pil_at(nx,ny,self.selected_tile_image)
        steps=int(max(w,h)*360)
        for step in range(steps+1):
            if steps==0: break
            theta=2*math.pi*step/steps
            fx=cx+rx*math.cos(theta)
            fy=cy+ry*math.sin(theta)
            tx,ty=int(round(fx)),int(round(fy))
            for rdy in range(-rad,rad+1):
                for rdx in range(-rad,rad+1):
                    paint_cell(tx+rdx,ty+rdy)

    # -------------------------------------------------------------------------
    # Undo / Redo
    # -------------------------------------------------------------------------
    def on_undo(self,event=None):
        if len(self.undo_stack)>1:
            self.redo_stack.append(self.undo_stack.pop())
            state=self.undo_stack[-1]
            self.load_undo_state(state)
        else:
            messagebox.showinfo("Undo","No more steps.")

    def on_redo(self,event=None):
        if self.redo_stack:
            st=self.redo_stack.pop()
            self.undo_stack.append(copy.deepcopy(self.map_data))
            self.load_undo_state(st)
        else:
            messagebox.showinfo("Redo","No redo steps available.")

    def record_undo_state(self):
        st=copy.deepcopy(self.map_data)
        self.undo_stack.append(st)
        self.redo_stack.clear()

    def load_undo_state(self,state):
        self.map_data=copy.deepcopy(state)
        self.map_canvas.delete("all")
        self.draw_map_grid()
        for r in range(self.map_height):
            for c in range(self.map_width):
                cell=self.map_data[r][c]
                if cell:
                    pil_img=cell["image_pil"]
                    x0=c*self.tile_size
                    y0=r*self.tile_size
                    tki=ImageTk.PhotoImage(pil_img)
                    cid=self.map_canvas.create_image(x0,y0,image=tki,anchor=tk.NW)
                    self.map_canvas.image[cid]=tki
                    self.map_data[r][c]={"image_pil":pil_img,"canvas_id":cid}

    # -------------------------------------------------------------------------
    # Delete/Shift/Control
    # -------------------------------------------------------------------------
    def on_delete_key(self, event):
        for (cx, cy) in list(self.selected_cells):
            old = self.map_data[cy][cx]
            if old:
                self.map_canvas.delete(old["canvas_id"])
            self.map_data[cy][cx] = None
        self.selected_cells.clear()
        self.redraw_selection()
    def on_shift_pressed(self, event):
        self.shift_down = True

    def on_shift_released(self, event):
        self.shift_down = False

    def on_ctrl_pressed(self, event):
        self.ctrl_down = True

    def on_ctrl_released(self, event):
        self.ctrl_down = False


    # -------------------------------------------------------------------------
    # Export Map / Export Selected
    # -------------------------------------------------------------------------
    def export_map(self):
        fp=filedialog.asksaveasfilename(defaultextension=".png",
                                        filetypes=[("PNG Files","*.png")],
                                        title="Save Entire Map")
        if not fp: return
        from PIL import Image
        W=self.map_width*self.tile_size
        H=self.map_height*self.tile_size
        out=Image.new("RGBA",(W,H),(0,0,0,0))
        for r in range(self.map_height):
            for c in range(self.map_width):
                cell=self.map_data[r][c]
                if cell:
                    tile=cell["image_pil"].convert("RGBA")
                    x0=c*self.tile_size
                    y0=r*self.tile_size
                    out.alpha_composite(tile,(x0,y0))
        out.save(fp,"PNG")
        messagebox.showinfo("Map Exported", f"Map saved to {fp}")

    def export_selected_tile(self):
        if not self.selected_cells:
            messagebox.showwarning("No Selection","No cell selected.")
            return
        cx, cy = next(iter(self.selected_cells))
        cell=self.map_data[cy][cx]
        if not cell:
            messagebox.showwarning("Empty","Selected cell has no tile.")
            return
        fp=filedialog.asksaveasfilename(defaultextension=".png",
                                        filetypes=[("PNG Files","*.png")],
                                        title="Save Selected Tile")
        if not fp: return
        cell["image_pil"].save(fp,"PNG")
        messagebox.showinfo("Exported", f"Tile saved to {fp}")

    # -------------------------------------------------------------------------
    # Gameboy-ize
    # -------------------------------------------------------------------------
    def gameboyize_map(self):
        """
        Convert every pixel of every tile on the map to the nearest of:
           #071821, #86c06c, #e0f8cf
        and special case black=>white => #65ff00
        """
        gb_colors = [
            (7,24,33),
            (134,192,108),
            (224,248,207)
        ]
        TRANSPARENT_GB=(101,255,0) # #65ff00
        def nearest_gb(rgb):
            (r,g,b)=rgb
            if (r,g,b)==(0,0,0) or (r,g,b)==(255,255,255):
                return TRANSPARENT_GB
            best=None
            bestd=999999
            for col in gb_colors:
                dr=col[0]-r
                dg=col[1]-g
                db=col[2]-b
                dist2=dr*dr+dg*dg+db*db
                if dist2<bestd:
                    bestd=dist2
                    best=col
            return best
        from PIL import Image
        for row in range(self.map_height):
            for col in range(self.map_width):
                cell=self.map_data[row][col]
                if cell:
                    pil_img=cell["image_pil"].convert("RGB")
                    px=pil_img.load()
                    for y in range(16):
                        for x in range(16):
                            oldc=px[x,y]
                            px[x,y]=nearest_gb(oldc)
                    self.map_data[row][col]["image_pil"]=pil_img
        # rebuild
        self.map_canvas.delete("all")
        self.draw_map_grid()
        for r in range(self.map_height):
            for c in range(self.map_width):
                cell=self.map_data[r][c]
                if cell:
                    tile=cell["image_pil"]
                    x0=c*self.tile_size
                    y0=r*self.tile_size
                    tki=ImageTk.PhotoImage(tile)
                    cid=self.map_canvas.create_image(x0,y0,image=tki,anchor=tk.NW)
                    self.map_canvas.image[cid]=tki
                    self.map_data[r][c]={"image_pil":tile,"canvas_id":cid}

        self.record_undo_state()
        messagebox.showinfo("Gameboy-ize","Map converted to Game Boy style!")


def main():
    app = TileGeneratorApp()
    app.mainloop()

if __name__=="__main__":
    main()
