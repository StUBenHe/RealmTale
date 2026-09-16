extends Node2D

## World — populates the tile map with Kenney Tiny Town tiles.

const MAP_W := 40
const MAP_H := 30
const TILE := 16  # Kenney tiles are 16×16

# Atlas coordinates in kenney_tilemap.png (col, row) → Vector2i
const T_GRASS   := Vector2i(0, 0)   # tile_0000 — solid green
const T_GRASS2  := Vector2i(1, 0)   # tile_0001 — grass variant
const T_DIRT    := Vector2i(1, 1)   # tile_0013 — dirt/sand
const T_SAND    := Vector2i(1, 2)   # tile_0025 — sand path
const T_WATER   := Vector2i(5, 6)   # tile_0077 — water
const T_WATER2  := Vector2i(4, 6)   # tile_0076 — water edge
const T_STONE   := Vector2i(1, 9)   # tile_0109 — stone floor
const T_STONE2  := Vector2i(0, 9)   # tile_0108 — stone edge
const T_ROOF    := Vector2i(5, 5)   # tile_0065 — red roof
const T_PATH    := Vector2i(1, 3)   # tile_0037 — dirt path
const T_WOOD    := Vector2i(1, 6)   # tile_0073 — wood floor
const T_WATER_D := Vector2i(3, 10)  # tile_0123 — deep water

@onready var ground: TileMapLayer = $GroundLayer
@onready var camera: Camera2D = $Camera2D


func _ready() -> void:
	_populate_map()
	_center_camera()


func get_grid_pos(world_pos: Vector2) -> Vector2i:
	return Vector2i(floori(world_pos.x / TILE), floori(world_pos.y / TILE))


func get_world_pos(grid_pos: Vector2i) -> Vector2:
	return Vector2(grid_pos.x * TILE + TILE / 2.0, grid_pos.y * TILE + TILE / 2.0)


func _populate_map() -> void:
	# Fill base with grass
	for x in range(MAP_W):
		for y in range(MAP_H):
			# Varied grass
			var grass := T_GRASS if (x + y) % 3 != 0 else T_GRASS2
			ground.set_cell(Vector2i(x, y), 0, grass)

	# ── Dirt cross-path ──
	# Horizontal road at row 15
	for x in range(3, 37):
		ground.set_cell(Vector2i(x, 15), 0, T_PATH)
		ground.set_cell(Vector2i(x, 16), 0, T_DIRT)
	# Vertical road at col 20
	for y in range(3, 27):
		ground.set_cell(Vector2i(20, y), 0, T_PATH)
		ground.set_cell(Vector2i(21, y), 0, T_DIRT)

	# ── Stone plaza 6×4 at center ──
	for x in range(18, 24):
		for y in range(13, 17):
			var st := T_STONE if (x + y) % 2 == 0 else T_STONE2
			ground.set_cell(Vector2i(x, y), 0, st)

	# ── Water pond 5×4 bottom-right ──
	for x in range(30, 35):
		for y in range(22, 26):
			var wt := T_WATER if (x + y) % 2 == 0 else T_WATER2
			ground.set_cell(Vector2i(x, y), 0, wt)

	# ── Water pond 3×3 top-left ──
	for x in range(2, 5):
		for y in range(2, 5):
			ground.set_cell(Vector2i(x, y), 0, T_WATER)

	# ── Wood floor area (future building site) ──
	for x in range(8, 13):
		for y in range(6, 10):
			ground.set_cell(Vector2i(x, y), 0, T_WOOD)

	# ── Small sand patches ──
	for x in range(25, 28):
		for y in range(8, 10):
			ground.set_cell(Vector2i(x, y), 0, T_SAND)

	# ── Roof tiles for demo buildings ──
	for x in range(9, 12):
		for y in range(7, 9):
			ground.set_cell(Vector2i(x, y), 0, T_ROOF)


func _center_camera() -> void:
	if camera:
		camera.position = Vector2(MAP_W * TILE / 2.0, MAP_H * TILE / 2.0)
