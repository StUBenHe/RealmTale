"""Generate a 20x15 grass map with a dirt path, stone plaza, and water pond."""
W, H = 20, 15

# Default: all grass (source 0)
grid = [[0]*H for _ in range(W)]

# Dirt path: horizontal road at row 7, cols 2-17
for x in range(2, 18):
    grid[x][7] = 1

# Dirt path: vertical road at col 10, rows 2-12
for y in range(2, 13):
    grid[10][y] = 1

# Stone plaza: 4x4 at center (cols 8-11, rows 5-8)
for x in range(8, 12):
    for y in range(5, 9):
        grid[x][y] = 2

# Water pond: 3x3 at bottom-right (cols 15-17, rows 11-13)
for x in range(15, 18):
    for y in range(11, 14):
        grid[x][y] = 3

# Water pond 2: small 2x2 at top-left (cols 1-2, rows 1-2)
for x in range(1, 3):
    for y in range(1, 3):
        grid[x][y] = 3

lines = []
lines.append('[gd_scene load_steps=7 format=3]')
lines.append('')
lines.append('[ext_resource type="Script" path="res://scenes/world/world.gd" id="1_script"]')
lines.append('[ext_resource type="Script" path="res://scenes/world/camera.gd" id="2_script"]')
lines.append('[ext_resource type="Texture2D" path="res://assets/terrain/grass.png" id="3_grass"]')
lines.append('[ext_resource type="Texture2D" path="res://assets/terrain/dirt.png" id="4_dirt"]')
lines.append('[ext_resource type="Texture2D" path="res://assets/terrain/stone.png" id="5_stone"]')
lines.append('[ext_resource type="Texture2D" path="res://assets/terrain/water.png" id="6_water"]')
lines.append('')
lines.append('[sub_resource type="TileSetAtlasSource" id="TileSetAtlasSource_grass"]')
lines.append('texture = ExtResource("3_grass")')
lines.append('texture_region_size = Vector2i(64, 64)')
lines.append('0:0/0 = 0')
lines.append('')
lines.append('[sub_resource type="TileSetAtlasSource" id="TileSetAtlasSource_dirt"]')
lines.append('texture = ExtResource("4_dirt")')
lines.append('texture_region_size = Vector2i(64, 64)')
lines.append('0:0/0 = 0')
lines.append('')
lines.append('[sub_resource type="TileSetAtlasSource" id="TileSetAtlasSource_stone"]')
lines.append('texture = ExtResource("5_stone")')
lines.append('texture_region_size = Vector2i(64, 64)')
lines.append('0:0/0 = 0')
lines.append('')
lines.append('[sub_resource type="TileSetAtlasSource" id="TileSetAtlasSource_water"]')
lines.append('texture = ExtResource("6_water")')
lines.append('texture_region_size = Vector2i(64, 64)')
lines.append('0:0/0 = 0')
lines.append('')
lines.append('[sub_resource type="TileSet" id="TileSet_terrain"]')
lines.append('tile_size = Vector2i(64, 64)')
lines.append('sources/0 = SubResource("TileSetAtlasSource_grass")')
lines.append('sources/1 = SubResource("TileSetAtlasSource_dirt")')
lines.append('sources/2 = SubResource("TileSetAtlasSource_stone")')
lines.append('sources/3 = SubResource("TileSetAtlasSource_water")')
lines.append('')
lines.append('[node name="World" type="Node2D"]')
lines.append('script = ExtResource("1_script")')
lines.append('')
lines.append('[node name="Camera2D" type="Camera2D" parent="."]')
lines.append('position = Vector2(640, 480)')
lines.append('script = ExtResource("2_script")')
lines.append('')
lines.append('[node name="TileMapLayer" type="TileMapLayer" parent="."]')
lines.append('tile_set = SubResource("TileSet_terrain")')

# Emit cells dictionary
lines.append('cells = {')
for x in range(W):
    for y in range(H):
        src = grid[x][y]
        lines.append('Vector2i(%d, %d): [Array[Variant]([%d, Vector2i(0, 0), 0])],' % (x, y, src))
lines.append('}')

with open('C:/Users/benhe/Desktop/RealmTale/src/scenes/world/world.tscn', 'w') as f:
    f.write('\n'.join(lines) + '\n')

print(f"world.tscn written with {W*H} tiles")
