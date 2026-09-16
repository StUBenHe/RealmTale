#!/usr/bin/env python3
"""Generate all placeholder pixel art sprites for RealmTale."""
from PIL import Image, ImageDraw
import os

BASE = os.path.join(os.path.dirname(__file__))
B = os.path.join(BASE, "buildings")
C = os.path.join(BASE, "characters")
T = os.path.join(BASE, "terrain")
U = os.path.join(BASE, "ui")
E = os.path.join(BASE, "effects")

# --- Colors ---
STONE    = "#8B8682"
WOOD     = "#8B4513"
GRASS    = "#4A7C4A"
WATER    = "#4A7CB5"
GOLD     = "#DAA520"
IRON     = "#708090"
HERBS    = "#228B22"
PARCH    = "#F5DEB3"
K_BLUE   = "#4169E1"
W_PURP   = "#8B008B"
R_GREEN  = "#2E8B57"
C_GOLD   = "#FFD700"
BLACK    = "#000000"
WHITE    = "#FFFFFF"
DARK_BG  = "#1a1a2e"
RED      = "#CC3333"
ROOF_RED = "#A0522D"

def new64(): return Image.new("RGBA", (64, 64), (0, 0, 0, 0))
def new32(): return Image.new("RGBA", (32, 32), (0, 0, 0, 0))
def d(img): return ImageDraw.Draw(img)

def outline_rect(draw, xy, fill, outline=BLACK, width=2):
    draw.rectangle(xy, fill=fill, outline=outline, width=width)

def outline_ellipse(draw, xy, fill, outline=BLACK, width=2):
    draw.ellipse(xy, fill=fill, outline=outline, width=width)

def outline_polygon(draw, pts, fill, outline=BLACK, width=2):
    draw.polygon(pts, fill=fill, outline=outline)
    # Thicken outline
    draw.line(pts + [pts[0]], fill=outline, width=width)

# ============================================================
# BUILDINGS
# ============================================================

def draw_house(img, level):
    """House gets bigger and more ornate with level."""
    dm = d(img)
    # Base size scales with level
    bw = 20 + level * 4   # building width
    bh = 16 + level * 4   # building height
    ox = (64 - bw) // 2   # x offset
    oy = 64 - bh - 4      # y offset (grounded)

    # Foundation
    outline_rect(dm, (ox-1, 60, ox+bw+1, 63), STONE)
    # Walls
    outline_rect(dm, (ox, oy, ox+bw, oy+bh), PARCH)
    # Roof
    roof_pts = [(ox-2, oy), (ox+bw//2, oy-8-level*2), (ox+bw+2, oy)]
    outline_polygon(dm, roof_pts, WOOD)
    # Door
    dx = ox + bw//2 - 3
    outline_rect(dm, (dx, oy+bh-8, dx+6, oy+bh), WOOD)
    # Window(s) based on level
    wy = oy + 4
    if level >= 1:
        outline_rect(dm, (ox+3, wy, ox+9, wy+6), WATER)
    if level >= 2:
        outline_rect(dm, (ox+bw-9, wy, ox+bw-3, wy+6), WATER)
    if level >= 3:
        # Chimney
        cx = ox + bw - 8
        outline_rect(dm, (cx, oy-10-level, cx+5, oy), STONE)
    if level >= 4:
        # Second floor
        outline_rect(dm, (ox+2, oy-6, ox+bw-2, oy), PARCH)
        outline_rect(dm, (ox+bw//2-2, oy-4, ox+bw//2+2, oy-1), WOOD)
    if level >= 5:
        # Towers on sides
        outline_rect(dm, (ox-6, oy-12, ox+4, oy+bh), STONE)
        outline_rect(dm, (ox+bw-4, oy-12, ox+bw+6, oy+bh), STONE)
        # Tower tops
        outline_polygon(dm, [(ox-8, oy-12), (ox-1, oy-18), (ox+6, oy-12)], WOOD)
        outline_polygon(dm, [(ox+bw-6, oy-12), (ox+bw+1, oy-18), (ox+bw+8, oy-12)], WOOD)

for lv in range(1, 6):
    img = new64()
    draw_house(img, lv)
    img.save(os.path.join(B, f"house_lv{lv}.png"))

def draw_blacksmith(img, level):
    dm = d(img)
    bw = 22 + level * 4
    bh = 18 + level * 3
    ox = (64 - bw) // 2
    oy = 64 - bh - 4

    outline_rect(dm, (ox, oy, ox+bw, oy+bh), STONE)
    # Chimney/smoke stack
    outline_rect(dm, (ox+bw-8, oy-10-level*2, ox+bw-3, oy), IRON)
    # Roof
    roof_pts = [(ox-2, oy), (ox+bw//2, oy-6-level), (ox+bw+2, oy)]
    outline_polygon(dm, roof_pts, IRON)
    # Anvil symbol on front
    ax = ox + bw//2
    ay = oy + bh//2
    outline_rect(dm, (ax-6, ay-2, ax+6, ay+2), IRON)  # anvil top
    outline_rect(dm, (ax-2, ay+2, ax+2, ay+6), IRON)   # anvil base
    # Door
    outline_rect(dm, (ox+3, oy+bh-10, ox+10, oy+bh), WOOD)
    # Fire glow
    if level >= 2:
        outline_rect(dm, (ox+bw-14, oy+bh-8, ox+bw-8, oy+bh-2), RED)
    if level >= 3:
        outline_rect(dm, (ox+bw-22, oy+bh-8, ox+bw-16, oy+bh-2), RED)
        # Larger anvil detail
        outline_rect(dm, (ax-8, ay-4, ax+8, ay), IRON)

for lv in range(1, 4):
    img = new64()
    draw_blacksmith(img, lv)
    img.save(os.path.join(B, f"blacksmith_lv{lv}.png"))

def draw_herb_garden(img, level):
    dm = d(img)
    # Wooden fence border
    outline_rect(dm, (4, 4, 60, 60), WOOD)
    # Soil inside
    outline_rect(dm, (6, 6, 58, 58), "#5C4033")
    # Plants grow with level
    for i in range(level + 1):
        px = 10 + i * 16
        py = 14
        # Stem
        outline_rect(dm, (px+2, py+4, px+4, py+14), HERBS)
        # Leaves
        outline_ellipse(dm, (px-2, py, px+8, py+8), HERBS)
        if level >= 2 and i < 2:
            # Small flowers
            outline_ellipse(dm, (px+1, py-3, px+5, py+1), GOLD)
        if level >= 3:
            # More plants, second row
            outline_rect(dm, (px+2, py+20, px+4, py+30), HERBS)
            outline_ellipse(dm, (px-1, py+16, px+7, py+24), HERBS)
    # Watering can for level 3
    if level >= 3:
        outline_rect(dm, (50, 50, 58, 58), IRON)
        outline_rect(dm, (48, 48, 52, 52), IRON)

for lv in range(1, 4):
    img = new64()
    draw_herb_garden(img, lv)
    img.save(os.path.join(B, f"herb_garden_lv{lv}.png"))

def draw_library(img, level):
    dm = d(img)
    bw = 24 + level * 2
    bh = 20 + level * 3
    ox = (64 - bw) // 2
    oy = 64 - bh - 4

    outline_rect(dm, (ox, oy, ox+bw, oy+bh), PARCH)
    # Peaked roof
    outline_polygon(dm, [(ox-2, oy), (ox+bw//2, oy-8-level*2), (ox+bw+2, oy)], WOOD)
    # Door
    outline_rect(dm, (ox+bw//2-3, oy+bh-8, ox+bw//2+3, oy+bh), WOOD)
    # Book symbol (horizontal lines)
    bx = ox + 4
    by = oy + 4
    for row in range(level + 1):
        outline_rect(dm, (bx, by + row*6, bx + bw - 8, by + row*6 + 4), IRON)
    # Window
    if level >= 2:
        outline_rect(dm, (ox+bw-12, oy+4, ox+bw-4, oy+12), WATER)
    if level >= 3:
        # Book on roof
        outline_rect(dm, (ox+bw//2-4, oy-12-level*2, ox+bw//2+4, oy-6-level*2), PARCH)
        outline_rect(dm, (ox+bw//2-2, oy-10-level*2, ox+bw//2+2, oy-8-level*2), IRON)

for lv in range(1, 4):
    img = new64()
    draw_library(img, lv)
    img.save(os.path.join(B, f"library_lv{lv}.png"))

def draw_castle(img, level):
    dm = d(img)
    # Castle gets wider and taller
    bw = 16 + level * 6
    bh = 14 + level * 5
    ox = (64 - bw) // 2
    oy = 64 - bh - 2

    # Main wall
    outline_rect(dm, (ox, oy, ox+bw, oy+bh), STONE)
    # Battlements (crenellations)
    cren_w = 4
    for cx in range(ox, ox+bw, cren_w*2):
        outline_rect(dm, (cx, oy-4, cx+cren_w, oy), STONE)
    # Gate
    gw = 6 + level
    gx = ox + bw//2 - gw//2
    outline_rect(dm, (gx, oy+bh-10-level*2, gx+gw, oy+bh), WOOD)
    # Door arch
    outline_ellipse(dm, (gx-1, oy+bh-12-level*2, gx+gw+1, oy+bh-4-level*2+4), WOOD)
    # Tower(s)
    if level >= 2:
        tw = 6
        # Left tower
        outline_rect(dm, (ox-4, oy-10, ox+tw-2, oy+bh), STONE)
        outline_polygon(dm, [(ox-6, oy-10), (ox+tw//2-3, oy-18), (ox+tw, oy-10)], WOOD)
        # Right tower
        outline_rect(dm, (ox+bw-tw+2, oy-10, ox+bw+4, oy+bh), STONE)
        outline_polygon(dm, [(ox+bw-tw, oy-10), (ox+bw-tw//2+1, oy-18), (ox+bw+6, oy-10)], WOOD)
    if level >= 3:
        # Windows
        for wy in [oy+4, oy+14]:
            outline_rect(dm, (ox+3, wy, ox+7, wy+4), WATER)
            outline_rect(dm, (ox+bw-7, wy, ox+bw-3, wy+4), WATER)
    if level >= 4:
        # Flag on left tower
        outline_rect(dm, (ox-1, oy-22, ox+1, oy-10), IRON)
        outline_polygon(dm, [(ox+1, oy-22), (ox+8, oy-18), (ox+1, oy-14)], RED)
        # Flag on right tower
        outline_rect(dm, (ox+bw, oy-22, ox+bw+2, oy-10), IRON)
        outline_polygon(dm, [(ox, oy-22), (ox-7, oy-18), (ox, oy-14)], K_BLUE)
    if level >= 5:
        # Keep (tall center tower)
        kw = 8
        kx = ox + bw//2 - kw//2
        outline_rect(dm, (kx, oy-18, kx+kw, oy), STONE)
        outline_polygon(dm, [(kx-2, oy-18), (kx+kw//2, oy-26), (kx+kw+2, oy-18)], GOLD)
        # Extra windows
        for wy in [oy-14, oy-6]:
            outline_rect(dm, (kx+1, wy, kx+kw-1, wy+4), WATER)
        # Moat
        outline_rect(dm, (0, 62, 64, 64), WATER)

for lv in range(1, 6):
    img = new64()
    draw_castle(img, lv)
    img.save(os.path.join(B, f"castle_lv{lv}.png"))

# ============================================================
# CHARACTERS
# ============================================================

def draw_knight(img):
    dm = d(img)
    # Body (armored torso)
    outline_rect(dm, (20, 20, 44, 52), K_BLUE)
    # Head (helmet)
    outline_ellipse(dm, (24, 4, 40, 20), K_BLUE)
    # Visor slit
    outline_rect(dm, (27, 10, 37, 13), BLACK)
    # Arms
    outline_rect(dm, (14, 24, 20, 44), K_BLUE)
    outline_rect(dm, (44, 24, 50, 44), K_BLUE)
    # Shield (left hand)
    outline_ellipse(dm, (8, 28, 18, 42), IRON)
    outline_ellipse(dm, (10, 30, 16, 38), GOLD)
    # Sword (right hand)
    outline_rect(dm, (50, 20, 52, 48), IRON)
    outline_rect(dm, (48, 18, 54, 22), GOLD)
    # Legs
    outline_rect(dm, (22, 52, 30, 62), K_BLUE)
    outline_rect(dm, (34, 52, 42, 62), K_BLUE)
    # Boots
    outline_rect(dm, (20, 58, 30, 64), WOOD)
    outline_rect(dm, (34, 58, 44, 64), WOOD)

def draw_wizard(img):
    dm = d(img)
    # Robe (triangular body)
    outline_polygon(dm, [(22, 16), (14, 62), (50, 62), (42, 16)], W_PURP)
    # Head
    outline_ellipse(dm, (24, 4, 40, 20), PARCH)
    # Hat (cone)
    outline_polygon(dm, [(24, 8), (32, -2), (40, 8)], W_PURP)
    outline_rect(dm, (22, 8, 42, 12), W_PURP)  # hat brim
    # Eyes
    outline_rect(dm, (28, 10, 30, 12), BLACK)
    outline_rect(dm, (34, 10, 36, 12), BLACK)
    # Staff (right side)
    outline_rect(dm, (50, 2, 52, 62), WOOD)
    outline_ellipse(dm, (48, 0, 56, 8), GOLD)
    # Belt
    outline_rect(dm, (20, 36, 44, 40), GOLD)
    # Beard
    outline_polygon(dm, [(28, 16), (32, 28), (36, 16)], "#C0C0C0")

def draw_rogue(img):
    dm = d(img)
    # Cloak body
    outline_polygon(dm, [(22, 18), (16, 60), (48, 60), (42, 18)], R_GREEN)
    # Hood (pointed)
    outline_polygon(dm, [(22, 14), (32, 2), (42, 14)], R_GREEN)
    # Face (dark, in shadow)
    outline_ellipse(dm, (26, 8, 38, 20), "#2a2a2a")
    # Eyes (glinting)
    outline_rect(dm, (29, 12, 31, 14), GOLD)
    outline_rect(dm, (33, 12, 35, 14), GOLD)
    # Daggers (both hands)
    outline_rect(dm, (10, 30, 14, 50), IRON)
    outline_rect(dm, (50, 30, 54, 50), IRON)
    # Belt with pouches
    outline_rect(dm, (22, 38, 42, 42), WOOD)
    outline_rect(dm, (26, 42, 30, 46), WOOD)
    # Boots
    outline_rect(dm, (18, 56, 28, 64), WOOD)
    outline_rect(dm, (36, 56, 46, 64), WOOD)

def draw_cleric(img):
    dm = d(img)
    # Robe
    outline_polygon(dm, [(22, 16), (14, 62), (50, 62), (42, 16)], C_GOLD)
    # Head
    outline_ellipse(dm, (24, 4, 40, 20), PARCH)
    # Halo
    outline_ellipse(dm, (22, 0, 42, 8), outline=GOLD, fill=None, width=2)
    # Eyes
    outline_rect(dm, (29, 10, 31, 12), BLACK)
    outline_rect(dm, (33, 10, 35, 12), BLACK)
    # Holy symbol on chest (cross)
    outline_rect(dm, (30, 22, 34, 36), GOLD)
    outline_rect(dm, (26, 26, 38, 30), GOLD)
    # Staff/crozier (left hand)
    outline_rect(dm, (10, 4, 12, 62), WOOD)
    outline_ellipse(dm, (8, 0, 16, 8), GOLD)
    # Hands in prayer or holding symbol
    outline_rect(dm, (26, 36, 38, 40), PARCH)
    # Belt
    outline_rect(dm, (22, 38, 42, 42), IRON)
    # Feet
    outline_rect(dm, (18, 58, 28, 64), WOOD)
    outline_rect(dm, (36, 58, 46, 64), WOOD)

for name, fn in [("knight", draw_knight), ("wizard", draw_wizard),
                  ("rogue", draw_rogue), ("cleric", draw_cleric)]:
    img = new64()
    fn(img)
    img.save(os.path.join(C, f"{name}.png"))

# ============================================================
# TERRAIN
# ============================================================

def draw_grass(img):
    dm = d(img)
    # Base green
    dm.rectangle([0, 0, 64, 64], fill=GRASS)
    # Grass tufts for texture
    for x in range(4, 64, 8):
        for y in range(4, 64, 8):
            dm.rectangle([x, y, x+2, y+4], fill="#3d6b3d")

def draw_dirt(img):
    dm = d(img)
    dm.rectangle([0, 0, 64, 64], fill="#8B6914")
    # Pebbles/stones
    for x in range(6, 64, 10):
        for y in range(6, 64, 10):
            dm.ellipse([x, y, x+4, y+3], fill="#7a5c12")

def draw_stone(img):
    dm = d(img)
    dm.rectangle([0, 0, 64, 64], fill=STONE)
    # Brick/stone pattern
    for row in range(0, 64, 16):
        offset = 8 if (row // 16) % 2 else 0
        for col in range(offset, 64, 16):
            dm.rectangle([col, row, col+14, row+14], outline="#6b6662", width=1)

def draw_water(img):
    dm = d(img)
    dm.rectangle([0, 0, 64, 64], fill=WATER)
    # Wave lines
    for y in range(10, 64, 12):
        for x in range(0, 60, 12):
            dm.arc([x, y-2, x+10, y+4], 0, 180, fill="#6a9cd5", width=2)

for name, fn in [("grass", draw_grass), ("dirt", draw_dirt),
                  ("stone", draw_stone), ("water", draw_water)]:
    img = new64()
    fn(img)
    img.save(os.path.join(T, f"{name}.png"))

# ============================================================
# UI
# ============================================================

def draw_btn_build(img):
    dm = d(img)
    # Button background (rounded rect approx)
    outline_rect(dm, (2, 2, 62, 62), "#3a3a5c")
    # Hammer head
    outline_rect(dm, (18, 10, 46, 24), IRON)
    # Handle
    outline_rect(dm, (30, 24, 34, 54), WOOD)

def draw_btn_heroes(img):
    dm = d(img)
    outline_rect(dm, (2, 2, 62, 62), "#3a3a5c")
    # Shield shape
    outline_polygon(dm, [(32, 8), (52, 16), (52, 36), (32, 56), (12, 36), (12, 16)], K_BLUE)
    outline_polygon(dm, [(32, 14), (46, 20), (46, 34), (32, 48), (18, 34), (18, 20)], "#6a9ae1")

def draw_btn_map(img):
    dm = d(img)
    outline_rect(dm, (2, 2, 62, 62), "#3a3a5c")
    # Compass circle
    outline_ellipse(dm, (12, 12, 52, 52), PARCH)
    outline_ellipse(dm, (16, 16, 48, 48), "#e8d4a8")
    # N/S/E/W pointers
    outline_polygon(dm, [(32, 14), (29, 30), (35, 30)], RED)     # N
    outline_polygon(dm, [(32, 50), (29, 34), (35, 34)], WHITE)   # S
    outline_polygon(dm, [(14, 32), (30, 29), (30, 35)], WHITE)   # W
    outline_polygon(dm, [(50, 32), (34, 29), (34, 35)], K_BLUE)  # E

def draw_btn_menu(img):
    dm = d(img)
    outline_rect(dm, (2, 2, 62, 62), "#3a3a5c")
    # Gear: center circle + teeth
    outline_ellipse(dm, (20, 20, 44, 44), IRON)
    outline_ellipse(dm, (26, 26, 38, 38), "#3a3a5c")
    # Gear teeth (rectangles around circle)
    for tl, br in [
        ((28, 16), (36, 20)),   # top
        ((28, 44), (36, 48)),   # bottom
        ((16, 28), (20, 36)),   # left
        ((44, 28), (48, 36)),   # right
    ]:
        dm.rectangle([tl[0], tl[1], br[0], br[1]], fill=IRON)

def draw_icon_gold(img):
    dm = d(img)
    # Coin
    outline_ellipse(dm, (4, 4, 28, 28), GOLD)
    outline_ellipse(dm, (8, 8, 24, 24), "#f0c850")
    # G symbol
    outline_rect(dm, (13, 10, 19, 22), GOLD)
    outline_rect(dm, (13, 10, 19, 14), GOLD)
    outline_rect(dm, (13, 10, 16, 22), GOLD)

def draw_icon_iron(img):
    dm = d(img)
    # Ingot shape (trapezoid)
    outline_polygon(dm, [(4, 14), (10, 6), (22, 6), (28, 14)], IRON)
    outline_rect(dm, (4, 14, 28, 26), IRON)
    outline_polygon(dm, [(6, 16), (10, 10), (22, 10), (26, 16)], "#909090")

def draw_icon_herbs(img):
    dm = d(img)
    # Leaf shape
    outline_ellipse(dm, (4, 8, 26, 28), HERBS)
    outline_ellipse(dm, (8, 10, 22, 26), "#32b032")
    # Stem
    outline_rect(dm, (15, 22, 17, 30), HERBS)
    # Leaf veins
    outline_rect(dm, (12, 14, 14, 20), "#1a6b1a")
    outline_rect(dm, (18, 12, 20, 18), "#1a6b1a")

def draw_icon_scrolls(img):
    dm = d(img)
    # Scroll body
    outline_rect(dm, (6, 8, 26, 24), PARCH)
    # Top roll
    outline_ellipse(dm, (4, 6, 10, 12), "#d4b896")
    # Bottom roll
    outline_ellipse(dm, (4, 22, 10, 28), "#d4b896")
    # Text lines
    outline_rect(dm, (10, 12, 22, 14), "#b89870")
    outline_rect(dm, (10, 16, 20, 18), "#b89870")
    outline_rect(dm, (10, 20, 18, 22), "#b89870")

# 64x64 buttons
for name, fn in [("btn_build", draw_btn_build), ("btn_heroes", draw_btn_heroes),
                  ("btn_map", draw_btn_map), ("btn_menu", draw_btn_menu)]:
    img = new64()
    fn(img)
    img.save(os.path.join(U, f"{name}.png"))

# 32x32 icons
for name, fn in [("icon_gold", draw_icon_gold), ("icon_iron", draw_icon_iron),
                  ("icon_herbs", draw_icon_herbs), ("icon_scrolls", draw_icon_scrolls)]:
    img = new32()
    fn(img)
    img.save(os.path.join(U, f"{name}.png"))

# Panel background (256x512, semi-transparent dark)
panel = Image.new("RGBA", (256, 512), (26, 26, 46, 200))
dm = d(panel)
# Border
dm.rectangle([0, 0, 255, 515], outline="#4a4a6c", width=4)
# Inner border accent
dm.rectangle([6, 6, 250, 510], outline="#6a6a8c", width=2)
panel.save(os.path.join(U, "panel_bg.png"))

# Menu background (1920x1080 dark gradient)
menu_bg = Image.new("RGBA", (1920, 1080))
for y in range(1080):
    r = int(10 + (y / 1080) * 20)
    g = int(10 + (y / 1080) * 15)
    b = int(30 + (y / 1080) * 25)
    dm_menu = ImageDraw.Draw(menu_bg)
    dm_menu.line([(0, y), (1920, y)], fill=(r, g, b, 255))
menu_bg.save(os.path.join(U, "menu_bg.png"))

# ============================================================
# EFFECTS
# ============================================================

def draw_placeholder(img):
    dm = d(img)
    # Purple diamond
    outline_polygon(dm, [(16, 2), (30, 16), (16, 30), (2, 16)], W_PURP)
    outline_polygon(dm, [(16, 6), (26, 16), (16, 26), (6, 16)], "#a020a0")
    # Sparkle
    outline_rect(dm, (14, 12, 18, 20), "#d060d0")

img = new32()
draw_placeholder(img)
img.save(os.path.join(E, "placeholder.png"))

# ============================================================
# VERIFY
# ============================================================
expected_files = []
# Buildings: house 1-5, blacksmith 1-3, herb_garden 1-3, library 1-3, castle 1-5
for lv in range(1, 6): expected_files.append(f"buildings/house_lv{lv}.png")
for lv in range(1, 4): expected_files.append(f"buildings/blacksmith_lv{lv}.png")
for lv in range(1, 4): expected_files.append(f"buildings/herb_garden_lv{lv}.png")
for lv in range(1, 4): expected_files.append(f"buildings/library_lv{lv}.png")
for lv in range(1, 6): expected_files.append(f"buildings/castle_lv{lv}.png")
# Characters
for name in ["knight", "wizard", "rogue", "cleric"]:
    expected_files.append(f"characters/{name}.png")
# Terrain
for name in ["grass", "dirt", "stone", "water"]:
    expected_files.append(f"terrain/{name}.png")
# UI
for name in ["btn_build", "btn_heroes", "btn_map", "btn_menu"]:
    expected_files.append(f"ui/{name}.png")
for name in ["icon_gold", "icon_iron", "icon_herbs", "icon_scrolls"]:
    expected_files.append(f"ui/{name}.png")
expected_files.extend(["ui/panel_bg.png", "ui/menu_bg.png"])
# Effects
expected_files.append("effects/placeholder.png")

all_ok = True
for f in expected_files:
    fp = os.path.join(BASE, f)
    if not os.path.exists(fp):
        print(f"MISSING: {f}")
        all_ok = False

print(f"\nGenerated {len(expected_files)} sprites.")
if all_ok:
    print("ALL FILES VERIFIED OK")
else:
    print("SOME FILES MISSING!")
