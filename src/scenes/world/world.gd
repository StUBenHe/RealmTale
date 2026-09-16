extends Node2D

## Manages the game world grid.

@onready var tile_map: TileMapLayer = $TileMapLayer


func get_grid_pos(world_pos: Vector2) -> Vector2i:
	return Vector2i(
		floori(world_pos.x / Config.TILE_SIZE),
		floori(world_pos.y / Config.TILE_SIZE)
	)


func get_world_pos(grid_pos: Vector2i) -> Vector2:
	return Vector2(
		grid_pos.x * Config.TILE_SIZE,
		grid_pos.y * Config.TILE_SIZE
	)
