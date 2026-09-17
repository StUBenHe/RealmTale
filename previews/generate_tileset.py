#!/usr/bin/env python3
"""Generate 32x32 pixel art tileset for medieval fantasy city-builder game.
Style: Cainos Pixel Art Top Down (earthy, organic, subtle shadows).
"""

import random
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

random.seed(42)  # Reproducible

TILE_SIZE = 32
COLS = 4
ROWS = 6

# ── Color palettes ──────────────────────────────────────────────
GRASS_BASE = (91, 140, 62)
GRASS_DARK = (72, 115, 48)
GRASS_LIGHT = (110, 165, 78)

DIRT_BASE = (160, 120, 76)
DIRT_DARK = (130, 95, 58)
DIRT_LIGHT = (180, 140, 95)
DIRT_EDGE = (110, 82, 50)

STONE_BASE = (139, 134, 130)
STONE_DARK = (112, 104, 96)
STONE_LIGHT = (160, 155, 150)
MORTAR = (112, 104, 96)
MOSS_GREEN = (75, 105, 55)

WATER_BASE = (74, 124, 181)
WATER_DARK = (50, 90, 145)
WATER_LIGHT = (100, 155, 210)
WATER_SHALLOW = (100, 160, 210)
WATER_DEEP = (40, 75, 125)

WOOD_BASE = (139, 90, 43)
WOOD_DARK = (105, 68, 30)
WOOD_LIGHT = (165, 115, 60)
PLANK_LINE = (85, 55, 25)

SAND_BASE = (212, 184, 150)
SAND_DARK = (190, 160, 125)
SAND_LIGHT = (230, 205, 175)

# ── Helper functions ────────────────────────────────────────────
def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, int(v)))

def lerp_color(c1, c2, t):
    return tuple(clamp(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def add_speckle(img, region, base_color, dark_color, count, rng):
    """Add random darker pixels for organic texture."""
    draw = ImageDraw.Draw(img)
    x0, y0, w, h = region
    for _ in range(count):
        x = rng.randint(x0, x0 + w - 1)
        y = rng.randint(y0, y0 + h - 1)
        offset = rng.uniform(0.3, 0.7)
        c = lerp_color(base_color, dark_color, offset)
        draw.point((x, y), fill=c)

def add_edge_darkening(img, region, edge_color, width=2):
    """Add darker edges for depth on bottom/right."""
    draw = ImageDraw.Draw(img)
    x0, y0, w, h = region
    # Bottom edge
    for dy in range(width):
        for x in range(x0, x0 + w):
            alpha = 0.4 - 0.15 * dy
            orig = img.getpixel((x, y0 + h - 1 - dy))
            blended = lerp_color(orig, edge_color, alpha)
            draw.point((x, y0 + h - 1 - dy), fill=blended)
    # Right edge
    for dx in range(width):
        for y in range(y0, y0 + h):
            alpha = 0.35 - 0.1 * dx
            orig = img.getpixel((x0 + w - 1 - dx, y))
            blended = lerp_color(orig, edge_color, alpha)
            draw.point((x0 + w - 1 - dx, y), fill=blended)

def fill_rect(img, x, y, w, h, color):
    draw = ImageDraw.Draw(img)
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=color)

# ── Tile renderers ──────────────────────────────────────────────

def render_grass_solid(img, ox, oy):
    """[0,0] Solid grass with speckle texture."""
    fill_rect(img, ox, oy, TILE_SIZE, TILE_SIZE, GRASS_BASE)
    rng = random.Random(100)
    add_speckle(img, (ox, oy, TILE_SIZE, TILE_SIZE), GRASS_BASE, GRASS_DARK, 40, rng)
    add_speckle(img, (ox, oy, TILE_SIZE, TILE_SIZE), GRASS_BASE, GRASS_LIGHT, 15, rng)
    add_edge_darkening(img, (ox, oy, TILE_SIZE, TILE_SIZE), GRASS_DARK, 2)

def render_grass_flowers(img, ox, oy):
    """[1,0] Grass with small flowers."""
    render_grass_solid(img, ox, oy)
    draw = ImageDraw.Draw(img)
    rng = random.Random(200)
    flower_colors = [(230, 80, 80), (240, 200, 60), (200, 130, 220), (255, 255, 200)]
    for _ in range(4):
        x = rng.randint(ox + 4, ox + 27)
        y = rng.randint(oy + 4, oy + 27)
        c = rng.choice(flower_colors)
        draw.point((x, y), fill=c)
        # Small petal hints
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if rng.random() > 0.4:
                draw.point((x + dx, y + dy), fill=lerp_color(c, (255, 255, 255), 0.3))

def render_grass_dirt_patch(img, ox, oy):
    """[2,0] Grass with dirt patch in center."""
    render_grass_solid(img, ox, oy)
    draw = ImageDraw.Draw(img)
    rng = random.Random(300)
    # Irregular dirt patch in center
    for dx in range(-5, 6):
        for dy in range(-5, 6):
            dist = math.sqrt(dx * dx + dy * dy)
            # Make it irregular
            noise = rng.uniform(-1.5, 1.5)
            if dist + noise < 4.5:
                x, y = ox + 16 + dx, oy + 16 + dy
                t = dist / 5.0
                c = lerp_color(DIRT_BASE, GRASS_BASE, t)
                draw.point((x, y), fill=c)
    add_speckle(img, (ox + 11, oy + 11, 10, 10), DIRT_BASE, DIRT_DARK, 8, rng)

def render_grass_edge(img, ox, oy):
    """[3,0] Grass edge (transition to dirt)."""
    fill_rect(img, ox, oy, TILE_SIZE, TILE_SIZE, GRASS_BASE)
    draw = ImageDraw.Draw(img)
    rng = random.Random(400)
    # Dirt on bottom half, grass on top
    for y in range(oy, oy + TILE_SIZE):
        for x in range(ox, ox + TILE_SIZE):
            ny = (y - oy) / TILE_SIZE  # 0=top, 1=bottom
            transition = 0.4 + 0.1 * math.sin((x - ox) * 0.5)
            noise = rng.uniform(-0.08, 0.08)
            if ny + noise > transition:
                t = min(1.0, (ny - transition + noise) * 3)
                c = lerp_color(GRASS_BASE, DIRT_BASE, t)
                draw.point((x, y), fill=c)
            else:
                c = lerp_color(GRASS_BASE, GRASS_DARK, rng.uniform(0, 0.2))
                draw.point((x, y), fill=c)
    add_speckle(img, (ox, oy, TILE_SIZE, TILE_SIZE), DIRT_BASE, DIRT_DARK, 15, rng)
    add_edge_darkening(img, (ox, oy, TILE_SIZE, TILE_SIZE), DIRT_DARK, 1)

def render_dirt_solid(img, ox, oy):
    """[0,1] Solid dirt path."""
    fill_rect(img, ox, oy, TILE_SIZE, TILE_SIZE, DIRT_BASE)
    rng = random.Random(500)
    add_speckle(img, (ox, oy, TILE_SIZE, TILE_SIZE), DIRT_BASE, DIRT_DARK, 35, rng)
    add_speckle(img, (ox, oy, TILE_SIZE, TILE_SIZE), DIRT_BASE, DIRT_LIGHT, 10, rng)
    add_edge_darkening(img, (ox, oy, TILE_SIZE, TILE_SIZE), DIRT_DARK, 2)

def render_dirt_horizontal(img, ox, oy):
    """[1,1] Dirt path horizontal."""
    fill_rect(img, ox, oy, TILE_SIZE, TILE_SIZE, GRASS_BASE)
    draw = ImageDraw.Draw(img)
    rng = random.Random(600)
    # Dirt band across horizontal center
    for y in range(oy, oy + TILE_SIZE):
        for x in range(ox, ox + TILE_SIZE):
            ny = abs((y - oy) - 15.5) / 15.5
            noise = rng.uniform(-0.05, 0.05)
            if ny + noise < 0.55:
                t = (ny + noise) / 0.55
                c = lerp_color(DIRT_BASE, GRASS_BASE, t)
                c = lerp_color(c, DIRT_DARK, rng.uniform(0, 0.15))
                draw.point((x, y), fill=c)
    add_edge_darkening(img, (ox, oy, TILE_SIZE, TILE_SIZE), DIRT_DARK, 1)

def render_dirt_vertical(img, ox, oy):
    """[2,1] Dirt path vertical."""
    fill_rect(img, ox, oy, TILE_SIZE, TILE_SIZE, GRASS_BASE)
    draw = ImageDraw.Draw(img)
    rng = random.Random(700)
    for y in range(oy, oy + TILE_SIZE):
        for x in range(ox, ox + TILE_SIZE):
            nx = abs((x - ox) - 15.5) / 15.5
            noise = rng.uniform(-0.05, 0.05)
            if nx + noise < 0.55:
                t = (nx + noise) / 0.55
                c = lerp_color(DIRT_BASE, GRASS_BASE, t)
                c = lerp_color(c, DIRT_DARK, rng.uniform(0, 0.15))
                draw.point((x, y), fill=c)
    add_edge_darkening(img, (ox, oy, TILE_SIZE, TILE_SIZE), DIRT_DARK, 1)

def render_dirt_intersection(img, ox, oy):
    """[3,1] Dirt path intersection."""
    fill_rect(img, ox, oy, TILE_SIZE, TILE_SIZE, GRASS_BASE)
    draw = ImageDraw.Draw(img)
    rng = random.Random(800)
    for y in range(oy, oy + TILE_SIZE):
        for x in range(ox, ox + TILE_SIZE):
            nx = abs((x - ox) - 15.5) / 15.5
            ny = abs((y - oy) - 15.5) / 15.5
            min_dist = min(nx, ny)
            noise = rng.uniform(-0.05, 0.05)
            if min_dist + noise < 0.55:
                t = (min_dist + noise) / 0.55
                c = lerp_color(DIRT_BASE, GRASS_BASE, t)
                c = lerp_color(c, DIRT_DARK, rng.uniform(0, 0.12))
                draw.point((x, y), fill=c)
    add_edge_darkening(img, (ox, oy, TILE_SIZE, TILE_SIZE), DIRT_DARK, 1)

def render_stone_floor(img, ox, oy):
    """[0,2] Stone floor with mortar lines in brick pattern."""
    fill_rect(img, ox, oy, TILE_SIZE, TILE_SIZE, STONE_BASE)
    draw = ImageDraw.Draw(img)
    rng = random.Random(900)
    # Brick pattern: rows of bricks offset
    brick_h = 8
    brick_w = 16
    for row in range(4):
        y_start = oy + row * brick_h
        offset = (brick_w // 2) if (row % 2) else 0
        # Horizontal mortar line
        draw.line([(ox, y_start), (ox + TILE_SIZE - 1, y_start)], fill=MORTAR, width=1)
        # Vertical mortar lines
        for col in range(3):
            x_pos = ox + offset + col * brick_w
            if ox <= x_pos < ox + TILE_SIZE:
                draw.line([(x_pos, y_start), (x_pos, y_start + brick_h)], fill=MORTAR, width=1)
    # Add stone texture variation
    for row in range(4):
        y_start = oy + row * brick_h + 1
        offset = (brick_w // 2) if (row % 2) else 0
        for col in range(3):
            bx = ox + offset + col * brick_w + 1
            by = y_start
            # Each brick slightly different shade
            shade = rng.uniform(-8, 8)
            fill_rect(img, bx, by, brick_w - 2, brick_h - 2,
                      (clamp(STONE_BASE[0] + shade), clamp(STONE_BASE[1] + shade), clamp(STONE_BASE[2] + shade)))
    add_speckle(img, (ox, oy, TILE_SIZE, TILE_SIZE), STONE_BASE, STONE_DARK, 12, rng)
    add_edge_darkening(img, (ox, oy, TILE_SIZE, TILE_SIZE), STONE_DARK, 1)

def render_stone_variant(img, ox, oy):
    """[1,2] Stone floor variant (different brick layout)."""
    fill_rect(img, ox, oy, TILE_SIZE, TILE_SIZE, STONE_BASE)
    draw = ImageDraw.Draw(img)
    rng = random.Random(1000)
    # Larger irregular stones
    stones = [
        (2, 2, 13, 10), (16, 1, 14, 11), (1, 13, 10, 9),
        (12, 13, 10, 9), (23, 13, 8, 9), (2, 23, 14, 8),
        (17, 23, 13, 8), (0, 0, 0, 0)  # placeholder
    ]
    for sx, sy, sw, sh in stones:
        if sw == 0:
            continue
        shade = rng.uniform(-10, 10)
        stone_color = (clamp(STONE_BASE[0] + shade), clamp(STONE_BASE[1] + shade), clamp(STONE_BASE[2] + shade))
        fill_rect(img, ox + sx, oy + sy, sw, sh, stone_color)
        # Mortar outline
        draw.rectangle([ox + sx, oy + sy, ox + sx + sw - 1, oy + sy + sh - 1], outline=MORTAR, width=1)
    add_speckle(img, (ox, oy, TILE_SIZE, TILE_SIZE), STONE_BASE, STONE_DARK, 8, rng)
    add_edge_darkening(img, (ox, oy, TILE_SIZE, TILE_SIZE), STONE_DARK, 1)

def render_stone_edge(img, ox, oy):
    """[2,2] Stone edge (transition to grass)."""
    render_stone_floor(img, ox, oy)
    draw = ImageDraw.Draw(img)
    rng = random.Random(1100)
    # Grass creeping from top-right corner
    for y in range(oy, oy + TILE_SIZE):
        for x in range(ox, ox + TILE_SIZE):
            dist_corner = math.sqrt((x - (ox + TILE_SIZE)) ** 2 + (y - oy) ** 2)
            noise = rng.uniform(-3, 3)
            if dist_corner + noise < 22:
                t = max(0, min(1, (dist_corner + noise) / 22))
                c = lerp_color(GRASS_BASE, STONE_BASE, t)
                draw.point((x, y), fill=c)
    add_speckle(img, (ox, oy, TILE_SIZE, TILE_SIZE), GRASS_BASE, GRASS_DARK, 12, rng)

def render_stone_moss(img, ox, oy):
    """[3,2] Stone with moss."""
    render_stone_floor(img, ox, oy)
    draw = ImageDraw.Draw(img)
    rng = random.Random(1200)
    # Moss patches in random spots
    for _ in range(5):
        cx = rng.randint(ox + 4, ox + 27)
        cy = rng.randint(oy + 4, oy + 27)
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < 3 and rng.random() > 0.2:
                    x, y = cx + dx, cy + dy
                    if ox <= x < ox + TILE_SIZE and oy <= y < oy + TILE_SIZE:
                        t = dist / 3
                        c = lerp_color(MOSS_GREEN, STONE_BASE, t)
                        draw.point((x, y), fill=c)

def render_water(img, ox, oy):
    """[0,3] Water with wave pattern."""
    fill_rect(img, ox, oy, TILE_SIZE, TILE_SIZE, WATER_BASE)
    draw = ImageDraw.Draw(img)
    rng = random.Random(1300)
    # Subtle wave variation
    for y in range(oy, oy + TILE_SIZE):
        for x in range(ox, ox + TILE_SIZE):
            wave = math.sin((x - ox) * 0.4 + (y - oy) * 0.3) * 8
            noise = rng.uniform(-3, 3)
            c = lerp_color(WATER_DARK, WATER_LIGHT, (wave + noise + 10) / 20)
            draw.point((x, y), fill=c)
    # Lighter wave streaks
    for i in range(3):
        wy = oy + 8 + i * 8 + rng.randint(-1, 1)
        for x in range(ox + 3, ox + TILE_SIZE - 3):
            if rng.random() > 0.3:
                draw.point((x, wy), fill=WATER_LIGHT)
                if rng.random() > 0.5:
                    draw.point((x, wy - 1), fill=lerp_color(WATER_LIGHT, WATER_BASE, 0.4))
    add_edge_darkening(img, (ox, oy, TILE_SIZE, TILE_SIZE), WATER_DARK, 2)

def render_water_edge(img, ox, oy):
    """[1,3] Water edge (shoreline)."""
    fill_rect(img, ox, oy, TILE_SIZE, TILE_SIZE, SAND_BASE)
    draw = ImageDraw.Draw(img)
    rng = random.Random(1400)
    # Water on bottom-left
    for y in range(oy, oy + TILE_SIZE):
        for x in range(ox, ox + TILE_SIZE):
            dist = math.sqrt((x - ox) ** 2 + (y - (oy + TILE_SIZE)) ** 2)
            noise = rng.uniform(-2, 2)
            if dist + noise < 28:
                t = max(0, min(1, (dist + noise) / 28))
                c = lerp_color(WATER_BASE, SAND_BASE, t)
                wave = math.sin(x * 0.5 + y * 0.3) * 0.1
                c = lerp_color(c, WATER_LIGHT, max(0, wave))
                draw.point((x, y), fill=c)
    add_speckle(img, (ox, oy, TILE_SIZE, TILE_SIZE), SAND_BASE, SAND_DARK, 15, rng)

def render_shallow_water(img, ox, oy):
    """[2,3] Shallow water (lighter blue)."""
    fill_rect(img, ox, oy, TILE_SIZE, TILE_SIZE, WATER_SHALLOW)
    draw = ImageDraw.Draw(img)
    rng = random.Random(1500)
    for y in range(oy, oy + TILE_SIZE):
        for x in range(ox, ox + TILE_SIZE):
            wave = math.sin((x - ox) * 0.35 + (y - oy) * 0.4) * 6
            noise = rng.uniform(-4, 4)
            c = lerp_color(WATER_BASE, WATER_LIGHT, (wave + noise + 12) / 24)
            draw.point((x, y), fill=c)
    # Wave highlights
    for i in range(2):
        wy = oy + 10 + i * 10 + rng.randint(-1, 1)
        for x in range(ox + 2, ox + TILE_SIZE - 2):
            if rng.random() > 0.4:
                draw.point((x, wy), fill=(140, 190, 230))
    add_edge_darkening(img, (ox, oy, TILE_SIZE, TILE_SIZE), WATER_DARK, 1)

def render_deep_water(img, ox, oy):
    """[3,3] Deep water (darker blue)."""
    fill_rect(img, ox, oy, TILE_SIZE, TILE_SIZE, WATER_DEEP)
    draw = ImageDraw.Draw(img)
    rng = random.Random(1600)
    for y in range(oy, oy + TILE_SIZE):
        for x in range(ox, ox + TILE_SIZE):
            wave = math.sin((x - ox) * 0.3 + (y - oy) * 0.5) * 5
            noise = rng.uniform(-3, 3)
            c = lerp_color(WATER_DARK, WATER_BASE, (wave + noise + 8) / 16)
            draw.point((x, y), fill=c)
    # Subtle deep wave hints
    for i in range(2):
        wy = oy + 8 + i * 12
        for x in range(ox + 4, ox + TILE_SIZE - 4):
            if rng.random() > 0.5:
                draw.point((x, wy), fill=lerp_color(WATER_BASE, WATER_DARK, 0.3))
    add_edge_darkening(img, (ox, oy, TILE_SIZE, TILE_SIZE), (30, 55, 100), 2)

def render_wood_planks(img, ox, oy):
    """[0,4] Wood planks with plank lines."""
    fill_rect(img, ox, oy, TILE_SIZE, TILE_SIZE, WOOD_BASE)
    draw = ImageDraw.Draw(img)
    rng = random.Random(1700)
    # Vertical plank lines
    plank_positions = [0, 8, 16, 24, 31]
    for px in plank_positions:
        x = ox + px
        draw.line([(x, oy), (x, oy + TILE_SIZE - 1)], fill=PLANK_LINE, width=1)
    # Each plank slightly different shade
    for i in range(4):
        px = ox + plank_positions[i] + 1
        pw = plank_positions[i + 1] - plank_positions[i] - 2
        shade = rng.uniform(-8, 8)
        fill_rect(img, px, oy + 1, pw, TILE_SIZE - 2,
                  (clamp(WOOD_BASE[0] + shade), clamp(WOOD_BASE[1] + shade), clamp(WOOD_BASE[2] + shade)))
    # Wood grain lines (horizontal)
    for i in range(6):
        gy = oy + 3 + i * 5 + rng.randint(-1, 1)
        for x in range(ox + 1, ox + TILE_SIZE - 1):
            if rng.random() > 0.6:
                draw.point((x, gy), fill=WOOD_DARK)
    add_speckle(img, (ox, oy, TILE_SIZE, TILE_SIZE), WOOD_BASE, WOOD_DARK, 12, rng)
    add_edge_darkening(img, (ox, oy, TILE_SIZE, TILE_SIZE), WOOD_DARK, 1)

def render_wood_variant(img, ox, oy):
    """[1,4] Wood floor variant (horizontal planks)."""
    fill_rect(img, ox, oy, TILE_SIZE, TILE_SIZE, WOOD_BASE)
    draw = ImageDraw.Draw(img)
    rng = random.Random(1800)
    # Horizontal plank lines
    plank_positions = [0, 8, 16, 24, 31]
    for py in plank_positions:
        y = oy + py
        draw.line([(ox, y), (ox + TILE_SIZE - 1, y)], fill=PLANK_LINE, width=1)
    # Each plank slightly different shade
    for i in range(4):
        py = oy + plank_positions[i] + 1
        ph = plank_positions[i + 1] - plank_positions[i] - 2
        shade = rng.uniform(-8, 8)
        fill_rect(img, ox + 1, py, TILE_SIZE - 2, ph,
                  (clamp(WOOD_BASE[0] + shade), clamp(WOOD_BASE[1] + shade), clamp(WOOD_BASE[2] + shade)))
    # Wood grain (vertical hints)
    for i in range(6):
        gx = ox + 4 + i * 4 + rng.randint(-1, 1)
        for y in range(oy + 1, oy + TILE_SIZE - 1):
            if rng.random() > 0.65:
                draw.point((gx, y), fill=WOOD_DARK)
    add_speckle(img, (ox, oy, TILE_SIZE, TILE_SIZE), WOOD_BASE, WOOD_DARK, 10, rng)
    add_edge_darkening(img, (ox, oy, TILE_SIZE, TILE_SIZE), WOOD_DARK, 1)

def render_sand(img, ox, oy):
    """[0,5] Sand with grain texture."""
    fill_rect(img, ox, oy, TILE_SIZE, TILE_SIZE, SAND_BASE)
    draw = ImageDraw.Draw(img)
    rng = random.Random(1900)
    add_speckle(img, (ox, oy, TILE_SIZE, TILE_SIZE), SAND_BASE, SAND_DARK, 30, rng)
    add_speckle(img, (ox, oy, TILE_SIZE, TILE_SIZE), SAND_BASE, SAND_LIGHT, 15, rng)
    add_edge_darkening(img, (ox, oy, TILE_SIZE, TILE_SIZE), SAND_DARK, 1)

def render_sand_edge(img, ox, oy):
    """[1,5] Sand edge (transition to grass)."""
    fill_rect(img, ox, oy, TILE_SIZE, TILE_SIZE, SAND_BASE)
    draw = ImageDraw.Draw(img)
    rng = random.Random(2000)
    # Grass on top, sand on bottom
    for y in range(oy, oy + TILE_SIZE):
        for x in range(ox, ox + TILE_SIZE):
            ny = (y - oy) / TILE_SIZE
            transition = 0.45 + 0.1 * math.sin((x - ox) * 0.4)
            noise = rng.uniform(-0.06, 0.06)
            if ny + noise < transition:
                t = max(0, min(1, (transition - ny - noise) * 3))
                c = lerp_color(SAND_BASE, GRASS_BASE, t)
                draw.point((x, y), fill=c)
            else:
                c = lerp_color(SAND_BASE, SAND_DARK, rng.uniform(0, 0.15))
                draw.point((x, y), fill=c)
    add_speckle(img, (ox, oy, TILE_SIZE, TILE_SIZE), GRASS_BASE, GRASS_DARK, 12, rng)
    add_edge_darkening(img, (ox, oy, TILE_SIZE, TILE_SIZE), SAND_DARK, 1)

# ── Tile map ────────────────────────────────────────────────────
tile_renderers = {
    (0, 0): render_grass_solid,
    (1, 0): render_grass_flowers,
    (2, 0): render_grass_dirt_patch,
    (3, 0): render_grass_edge,
    (0, 1): render_dirt_solid,
    (1, 1): render_dirt_horizontal,
    (2, 1): render_dirt_vertical,
    (3, 1): render_dirt_intersection,
    (0, 2): render_stone_floor,
    (1, 2): render_stone_variant,
    (2, 2): render_stone_edge,
    (3, 2): render_stone_moss,
    (0, 3): render_water,
    (1, 3): render_water_edge,
    (2, 3): render_shallow_water,
    (3, 3): render_deep_water,
    (0, 4): render_wood_planks,
    (1, 4): render_wood_variant,
    (0, 5): render_sand,
    (1, 5): render_sand_edge,
}

tile_names = {
    (0, 0): "Grass",
    (1, 0): "Grass+Flowers",
    (2, 0): "Grass+Dirt",
    (3, 0): "Grass Edge",
    (0, 1): "Dirt Path",
    (1, 1): "Dirt Horiz",
    (2, 1): "Dirt Vert",
    (3, 1): "Dirt Cross",
    (0, 2): "Stone Floor",
    (1, 2): "Stone Variant",
    (2, 2): "Stone Edge",
    (3, 2): "Stone+Moss",
    (0, 3): "Water",
    (1, 3): "Water Edge",
    (2, 3): "Shallow Water",
    (3, 3): "Deep Water",
    (0, 4): "Wood Planks",
    (1, 4): "Wood Variant",
    (0, 5): "Sand",
    (1, 5): "Sand Edge",
}

# ════════════════════════════════════════════════════════════════
# Generate spritesheet
# ════════════════════════════════════════════════════════════════
print("Generating spritesheet...")
spritesheet = Image.new("RGBA", (COLS * TILE_SIZE, ROWS * TILE_SIZE), (0, 0, 0, 0))

for (cx, cy), renderer in tile_renderers.items():
    ox, oy = cx * TILE_SIZE, cy * TILE_SIZE
    renderer(spritesheet, ox, oy)
    print(f"  Tile [{cx},{cy}] rendered: {tile_names.get((cx, cy), 'unknown')}")

spritesheet_path = "C:/Users/benhe/Desktop/RealmTale/src/assets/terrain/tileset_32.png"
spritesheet.save(spritesheet_path)
print(f"Spritesheet saved: {spritesheet_path}")
print(f"  Size: {spritesheet.size[0]}x{spritesheet.size[1]} pixels")
print(f"  Tiles: {len(tile_renderers)}")

# ════════════════════════════════════════════════════════════════
# Generate preview
# ════════════════════════════════════════════════════════════════
print("\nGenerating preview...")
preview_scale = 3  # Scale up for readability
label_h = 24
preview_tile_size = TILE_SIZE * preview_scale
preview_w = COLS * (preview_tile_size + 8) + 8
preview_h = ROWS * (preview_tile_size + label_h + 8) + 8

preview = Image.new("RGBA", (preview_w, preview_h), (30, 30, 35, 255))
draw_preview = ImageDraw.Draw(preview)

# Try to load a font
try:
    font = ImageFont.truetype("arial.ttf", 14)
except:
    try:
        font = ImageFont.truetype("/c/Windows/Fonts/arial.ttf", 14)
    except:
        font = ImageFont.load_default()

for cy in range(ROWS):
    for cx in range(COLS):
        key = (cx, cy)
        if key not in tile_renderers:
            continue
        # Get tile from spritesheet
        tile = spritesheet.crop((cx * TILE_SIZE, cy * TILE_SIZE, (cx + 1) * TILE_SIZE, (cy + 1) * TILE_SIZE))
        scaled = tile.resize((preview_tile_size, preview_tile_size), Image.NEAREST)

        px = 8 + cx * (preview_tile_size + 8)
        py = 8 + cy * (preview_tile_size + label_h + 8)

        preview.paste(scaled, (px, py), scaled)

        # Label
        name = tile_names.get(key, "?")
        draw_preview.text((px + 2, py + preview_tile_size + 2), name, fill=(220, 220, 220), font=font)

preview_path = "C:/Users/benhe/Desktop/RealmTale/previews/custom_tileset_preview.png"
preview.save(preview_path)
print(f"Preview saved: {preview_path}")
print(f"  Size: {preview.size[0]}x{preview.size[1]} pixels")

# ════════════════════════════════════════════════════════════════
# Generate village mockup
# ════════════════════════════════════════════════════════════════
print("\nGenerating village mockup...")
mockup_w, mockup_h = 640, 480
mockup = Image.new("RGBA", (mockup_w, mockup_h), (0, 0, 0, 0))
draw_mockup = ImageDraw.Draw(mockup)
rng_mockup = random.Random(42)

# Create a map: 20x15 grid of tiles
map_cols = mockup_w // TILE_SIZE  # 20
map_rows = mockup_h // TILE_SIZE  # 15

tile_map = [[(0, 0) for _ in range(map_cols)] for _ in range(map_rows)]

# Fill everything with grass first
for y in range(map_rows):
    for x in range(map_cols):
        tile_map[y][x] = (0, 0)

# Create a winding path from left to right with curves
path_points = [
    (0, 7), (1, 7), (2, 7), (3, 7), (3, 6), (4, 6), (5, 6), (5, 5),
    (6, 5), (7, 5), (8, 5), (8, 6), (9, 6), (10, 6), (10, 7), (11, 7),
    (12, 7), (12, 8), (13, 8), (14, 8), (14, 7), (15, 7), (16, 7),
    (16, 8), (17, 8), (18, 8), (19, 8),
]
# Vertical branch going up
path_up = [
    (7, 5), (7, 4), (7, 3), (7, 2), (8, 2), (9, 2), (10, 2),
    (10, 3), (10, 4), (10, 5), (10, 6),
]
# Vertical branch going down
path_down = [
    (14, 8), (14, 9), (14, 10), (14, 11), (15, 11), (16, 11),
    (16, 10), (16, 9), (16, 8),
]

for x, y in path_points + path_up + path_down:
    if 0 <= y < map_rows and 0 <= x < map_cols:
        tile_map[y][x] = (0, 1)  # Dirt path

# Set path edges to grass with dirt patch for transition
for x, y in path_points + path_up + path_down:
    for dx in [-1, 1]:
        nx, ny = x + dx, y
        if 0 <= ny < map_rows and 0 <= nx < map_cols and tile_map[ny][nx] == (0, 0):
            tile_map[ny][nx] = (2, 0)  # Grass with dirt patch

# Stone plaza in upper area
plaza_cx, plaza_cy = 8, 3
for dy in range(-1, 2):
    for dx in range(-2, 3):
        px, py = plaza_cx + dx, plaza_cy + dy
        if 0 <= py < map_rows and 0 <= px < map_cols:
            if abs(dx) + abs(dy) <= 3:
                tile_map[py][px] = (0, 2)  # Stone floor
            else:
                tile_map[py][px] = (2, 2)  # Stone edge

# Wood-floored building area (lower right)
for dy in range(3):
    for dx in range(4):
        bx, by = 4 + dx, 11 + dy
        if 0 <= by < map_rows and 0 <= bx < map_cols:
            tile_map[by][bx] = (0, 4)  # Wood planks
# Wood variant for door area
tile_map[11][5] = (1, 4)
tile_map[12][5] = (1, 4)

# Water pond (lower left)
pond_cx, pond_cy = 3, 10
for dy in range(-2, 3):
    for dx in range(-2, 3):
        wx, wy = pond_cx + dx, pond_cy + dy
        dist = math.sqrt(dx * dx + dy * dy)
        if 0 <= wy < map_rows and 0 <= wx < map_cols:
            if dist < 1.5:
                tile_map[wy][wx] = (3, 3)  # Deep water
            elif dist < 2.2:
                tile_map[wy][wx] = (2, 3)  # Shallow water
            elif dist < 3:
                tile_map[wy][wx] = (1, 3)  # Water edge

# Sand patch near pond
for dx in range(-1, 2):
    sx, sy = pond_cx + 3 + dx, pond_cy
    if 0 <= sy < map_rows and 0 <= sx < map_cols:
        tile_map[sy][sx] = (0, 5)  # Sand
tile_map[pond_cy][pond_cx + 4] = (1, 5)  # Sand edge

# Another building (upper right) with stone
for dy in range(2):
    for dx in range(3):
        bx, by = 15 + dx, 3 + dy
        if 0 <= by < map_rows and 0 <= bx < map_cols:
            tile_map[by][bx] = (1, 2)  # Stone variant

# Add some grass with flowers randomly
for _ in range(8):
    fx = rng_mockup.randint(0, map_cols - 1)
    fy = rng_mockup.randint(0, map_rows - 1)
    if tile_map[fy][fx] == (0, 0):
        tile_map[fy][fx] = (1, 0)  # Grass with flowers

# Stone with moss near water
for dx in range(-1, 2):
    mx, my = pond_cx - 2 + dx, pond_cy - 2
    if 0 <= my < map_rows and 0 <= mx < map_cols and tile_map[my][mx] == (0, 0):
        tile_map[my][mx] = (3, 2)  # Stone with moss

# Render the map
for my in range(map_rows):
    for mx in range(map_cols):
        tile_key = tile_map[my][mx]
        src_x = tile_key[0] * TILE_SIZE
        src_y = tile_key[1] * TILE_SIZE
        tile = spritesheet.crop((src_x, src_y, src_x + TILE_SIZE, src_y + TILE_SIZE))
        mockup.paste(tile, (mx * TILE_SIZE, my * TILE_SIZE), tile)

mockup_path = "C:/Users/benhe/Desktop/RealmTale/previews/village_mockup.png"
mockup.save(mockup_path)
print(f"Village mockup saved: {mockup_path}")
print(f"  Size: {mockup.size[0]}x{mockup.size[1]} pixels")
print(f"  Grid: {map_cols}x{map_rows} tiles")

print("\n✅ All done!")
