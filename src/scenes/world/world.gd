extends Node2D

## World — manages the tile grid and populates terrain at startup.

const MAP_W := 20
const MAP_H := 15
const TILE := 64

# Tile source IDs (must match TileSetAtlasSource order in world.tscn)
const GRASS := 0
const DIRT  := 1
const STONE := 2
const WATER := 3

@onready var ground: TileMapLayer = $GroundLayer
@onready var camera: Camera2D = $Camera2D


func _ready() -> void:
	_populate_map()
	_center_camera()


## Convert world position → grid coords
func get_grid_pos(world_pos: Vector2) -> Vector2i:
	return Vector2i(floori(world_pos.x / TILE), floori(world_pos.y / TILE))


## Convert grid coords → world position (center of cell)
func get_world_pos(grid_pos: Vector2i) -> Vector2:
	return Vector2(grid_pos.x * TILE + TILE / 2.0, grid_pos.y * TILE + TILE / 2.0)


func _populate_map() -> void:
	# Fill entire map with grass
	for x in range(MAP_W):
		for y in range(MAP_H):
			ground.set_cell(Vector2i(x, y), GRASS, Vector2i.ZERO)

	# ── Dirt paths (cross shape) ──
	# Horizontal road at row 7, cols 2-17
	for x in range(2, 18):
		ground.set_cell(Vector2i(x, 7), DIRT, Vector2i.ZERO)
	# Vertical road at col 10, rows 2-12
	for y in range(2, 13):
		ground.set_cell(Vector2i(10, y), DIRT, Vector2i.ZERO)

	# ── Stone plaza 4×4 at center ──
	for x in range(8, 12):
		for y in range(5, 9):
			ground.set_cell(Vector2i(x, y), STONE, Vector2i.ZERO)

	# ── Water pond 3×3 bottom-right ──
	for x in range(15, 18):
		for y in range(11, 14):
			ground.set_cell(Vector2i(x, y), WATER, Vector2i.ZERO)

	# ── Water pond 2×2 top-left ──
	for x in range(1, 3):
		for y in range(1, 3):
			ground.set_cell(Vector2i(x, y), WATER, Vector2i.ZERO)


func _center_camera() -> void:
	if camera:
		camera.position = Vector2(MAP_W * TILE / 2.0, MAP_H * TILE / 2.0)
