extends Node

## Autoload singleton managing all placed buildings.

var _buildings: Array[Dictionary] = []  # {instance, grid_pos, id, data}


func place_building(building_scene: PackedScene, grid_pos: Vector2i, data: Dictionary = {}) -> bool:
	if get_buildings_at(grid_pos).size() > 0:
		return false
	var instance := building_scene.instantiate()
	var entry := {
		"instance": instance,
		"grid_pos": grid_pos,
		"id": data.get("id", "unknown"),
		"data": data,
	}
	_buildings.append(entry)
	EventBus.building_placed.emit(data, grid_pos)
	return true


func remove_building(building_id: String) -> bool:
	for i in _buildings.size():
		if _buildings[i]["id"] == building_id:
			_buildings[i]["instance"].queue_free()
			_buildings.remove_at(i)
			return true
	return false


func get_buildings_at(pos: Vector2i) -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for b in _buildings:
		if b["grid_pos"] == pos:
			result.append(b)
	return result


func get_all_buildings() -> Array[Dictionary]:
	return _buildings
