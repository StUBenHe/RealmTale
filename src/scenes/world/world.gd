extends Node2D

## World — builds tileset and organic village map at runtime.
## Tileset: custom 32x32 spritesheet (4 cols × 6 rows)

const MAP_W := 30
const MAP_H := 20
const TILE := 32

# Atlas coordinates (col, row) in tileset_32.png
const T_GRASS   := Vector2i(0, 0)  # solid grass
const T_GRASS_F := Vector2i(1, 0)  # grass with flowers
const T_GRASS_D := Vector2i(2, 0)  # grass with dirt
const T_GRASS_E := Vector2i(3, 0)  # grass-dirt edge
const T_DIRT    := Vector2i(0, 1)  # solid dirt
const T_DIRT_H  := Vector2i(1, 1)  # dirt horizontal
const T_DIRT_V  := Vector2i(2, 1)  # dirt vertical
const T_DIRT_X  := Vector2i(3, 1)  # dirt intersection
const T_STONE   := Vector2i(0, 2)  # stone floor
const T_STONE_V := Vector2i(1, 2)  # stone variant
const T_STONE_E := Vector2i(2, 2)  # stone edge
const T_STONE_M := Vector2i(3, 2)  # stone with moss
const T_WATER   := Vector2i(0, 3)  # water
const T_WATER_S := Vector2i(1, 3)  # water shore
const T_WATER_L := Vector2i(2, 3)  # shallow water
const T_WATER_D := Vector2i(3, 3)  # deep water
const T_WOOD    := Vector2i(0, 4)  # wood planks
const T_WOOD_V  := Vector2i(1, 4)  # wood variant
const T_SAND    := Vector2i(0, 5)  # sand
const T_SAND_E  := Vector2i(1, 5)  # sand edge

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
	src.texture = load("res://assets/terrain/tileset_32.png")
	src.texture_region_size = Vector2i(TILE, TILE)

	# Register all tiles in the 4×6 grid
	for col in range(4):
		for row in range(6):
			src.create_tile(Vector2i(col, row))

	ts.add_source(src, 0)
	ground.tile_set = ts


func get_grid_pos(world_pos: Vector2) -> Vector2i:
	return Vector2i(floori(world_pos.x / TILE), floori(world_pos.y / TILE))


func get_world_pos(grid_pos: Vector2i) -> Vector2:
	return Vector2(grid_pos.x * TILE + TILE / 2.0, grid_pos.y * TILE + TILE / 2.0)


func _fill(from: Vector2i, to: Vector2i, tile: Vector2i) -> void:
	for x in range(from.x, to.x + 1):
		for y in range(from.y, to.y + 1):
			ground.set_cell(Vector2i(x, y), 0, tile)


def _populate_map() -> void:
	# ── Base: all grass with random flower variation ──
	for x in range(MAP_W):
		for y in range(MAP_H):
			var g := T_GRASS if randf() > 0.15 else T_GRASS_F
			ground.set_cell(Vector2i(x, y), 0, g)

	# ── Winding dirt path (organic curve, not cross) ──
	# Main path: left to right with gentle curves
	var path_points := [
		[0,10], [1,10], [2,10], [3,10], [4,10], [5,10], [6,11],
		[7,11], [8,11], [9,11], [10,11], [11,10], [12,10], [13,10],
		[14,10], [15,9], [16,9], [17,9], [18,9], [19,9], [20,9],
		[21,10], [22,10], [23,10], [24,10], [25,10], [26,10],
		[27,10], [28,10], [29,10]
	]
	for p in path_points:
		ground.set_cell(Vector2i(p[0], p[1]), 0, T_DIRT)
		ground.set_cell(Vector2i(p[0], p[1] + 1), 0, T_DIRT_H)

	# Branch path: upward to village center
	var branch := [
		[12,10], [12,9], [12,8], [13,7], [13,6], [14,5], [14,4],
		[15,4], [15,3], [15,2]
	]
	for p in branch:
		ground.set_cell(Vector2i(p[0], p[1]), 0, T_DIRT_V)

	# Branch path: downward to pond
	var branch2 := [
		[20,9], [20,10], [20,11], [21,12], [21,13], [22,14], [22,15]
	]
	for p in branch2:
		ground.set_cell(Vector2i(p[0], p[1]), 0, T_DIRT_V)

	# ── Stone plaza (village center, organic shape) ──
	for x in range(12, 18):
		for y in range(5, 9):
			var s := T_STONE if (x + y) % 2 == 0 else T_STONE_V
			ground.set_cell(Vector2i(x, y), 0, s)
	# Stone edges
	for x in range(11, 19):
		ground.set_cell(Vector2i(x, 4), 0, T_STONE_E)
		ground.set_cell(Vector2i(x, 9), 0, T_STONE_E)

	# ── Water pond (organic shape, bottom-right) ──
	var pond := [
		[23,14], [24,14], [25,14], [26,14],
		[22,15], [23,15], [24,15], [25,15], [26,15], [27,15],
		[22,16], [23,16], [24,16], [25,16], [26,16], [27,16],
		[23,17], [24,17], [25,17], [26,17],
		[24,18], [25,18]
	]
	for p in pond:
		ground.set_cell(Vector2i(p[0], p[1]), 0, T_WATER)
	# Shore edges
	var shore := [
		[21,13], [22,13], [23,13], [24,13], [25,13], [26,13], [27,13], [28,13],
		[21,14], [28,14],
		[21,15], [28,15],
		[21,16], [28,16],
		[22,17], [27,17],
		[23,18], [26,18],
		[24,19], [25,19]
	]
	for p in shore:
		ground.set_cell(Vector2i(p[0], p[1]), 0, T_WATER_S)

	# ── Wood floor areas (building sites) ──
	# House cluster top-left
	_fill(Vector2i(3, 2), Vector2i(6, 4), T_WOOD)
	# Blacksmith area
	_fill(Vector2i(8, 5), Vector2i(10, 7), T_WOOD_V)
	# Library area
	_fill(Vector2i(20, 3), Vector2i(23, 5), T_WOOD)
	# Farm area
	_fill(Vector2i(5, 13), Vector2i(9, 16), T_SAND)
	_fill(Vector2i(6, 13), Vector2i(8, 15), T_SAND_E)

	# ── Grass-dirt transitions along paths ──
	for p in path_points + branch + branch2:
		for dx in [-1, 1]:
			var nx := Vector2i(p[0] + dx, p[1])
			if ground.get_cell_source_id(nx) == 0:
				var current := ground.get_cell_atlas_coords(nx)
				if current == T_GRASS or current == T_GRASS_F:
					ground.set_cell(nx, 0, T_GRASS_E)


func _center_camera() -> void:
	if camera:
		camera.position = Vector2(MAP_W * TILE / 2.0, MAP_H * TILE / 2.0)
