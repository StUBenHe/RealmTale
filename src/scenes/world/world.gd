extends Node2D

## World — builds tileset and map entirely at runtime.

const MAP_W := 40
const MAP_H := 30
const TILE := 16

# Atlas coordinates in kenney_tilemap.png (12 cols × 11 rows)
const T_GRASS  := Vector2i(0, 0)
const T_GRASS2 := Vector2i(1, 0)
const T_DIRT   := Vector2i(1, 1)
const T_PATH   := Vector2i(1, 3)
const T_WATER  := Vector2i(5, 6)
const T_WATER2 := Vector2i(4, 6)
const T_STONE  := Vector2i(1, 9)
const T_STONE2 := Vector2i(0, 9)
const T_WOOD   := Vector2i(1, 6)
const T_SAND   := Vector2i(1, 2)
const T_ROOF   := Vector2i(5, 5)

@onready var ground: TileMapLayer = $GroundLayer
@onready var camera: Camera2D = $Camera2D


func _ready() -> void:
	_build_tileset()
	_populate_map()
	_center_camera()


func _build_tileset() -> void:
	var ts := TileSet.new()
	ts.tile_size = Vector2i(TILE, TILE)

	var src := TileSetAtlasSource.new()
	src.texture = load("res://assets/terrain/kenney_tilemap.png")
	src.texture_region_size = Vector2i(TILE, TILE)

	# Tell Godot which tiles exist in the atlas (12×11 grid)
	for col in range(12):
		for row in range(11):
			src.create_tile(Vector2i(col, row))

	ts.add_source(src, 0)
	ground.tile_set = ts


func get_grid_pos(world_pos: Vector2) -> Vector2i:
	return Vector2i(floori(world_pos.x / TILE), floori(world_pos.y / TILE))


func get_world_pos(grid_pos: Vector2i) -> Vector2:
	return Vector2(grid_pos.x * TILE + TILE / 2.0, grid_pos.y * TILE + TILE / 2.0)


func _populate_map() -> void:
	# Fill base with grass
	for x in range(MAP_W):
		for y in range(MAP_H):
			var g := T_GRASS if (x + y) % 3 != 0 else T_GRASS2
			ground.set_cell(Vector2i(x, y), 0, g)

	# Horizontal road at row 15
	for x in range(3, 37):
		ground.set_cell(Vector2i(x, 15), 0, T_PATH)
		ground.set_cell(Vector2i(x, 16), 0, T_DIRT)

	# Vertical road at col 20
	for y in range(3, 27):
		ground.set_cell(Vector2i(20, y), 0, T_PATH)
		ground.set_cell(Vector2i(21, y), 0, T_DIRT)

	# Stone plaza 6×4
	for x in range(18, 24):
		for y in range(13, 17):
			var s := T_STONE if (x + y) % 2 == 0 else T_STONE2
			ground.set_cell(Vector2i(x, y), 0, s)

	# Water pond 5×4 bottom-right
	for x in range(30, 35):
		for y in range(22, 26):
			var w := T_WATER if (x + y) % 2 == 0 else T_WATER2
			ground.set_cell(Vector2i(x, y), 0, w)

	# Water pond 3×3 top-left
	for x in range(2, 5):
		for y in range(2, 5):
			ground.set_cell(Vector2i(x, y), 0, T_WATER)

	# Wood floor area
	for x in range(8, 13):
		for y in range(6, 10):
			ground.set_cell(Vector2i(x, y), 0, T_WOOD)

	# Sand patches
	for x in range(25, 28):
		for y in range(8, 10):
			ground.set_cell(Vector2i(x, y), 0, T_SAND)

	# Demo roof tiles
	for x in range(9, 12):
		for y in range(7, 9):
			ground.set_cell(Vector2i(x, y), 0, T_ROOF)


func _center_camera() -> void:
	if camera:
		camera.position = Vector2(MAP_W * TILE / 2.0, MAP_H * TILE / 2.0)
