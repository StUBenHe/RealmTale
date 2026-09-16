extends Node

## Autoload singleton for save/load via JSON files.

const SAVE_DIR: String = "user://saves/"


func save_game(slot: int = 0) -> bool:
	var dir := DirAccess.open(SAVE_DIR)
	if dir == null:
		DirAccess.make_dir_recursive_absolute(SAVE_DIR)
	dir = DirAccess.open(SAVE_DIR)
	if dir == null:
		return false

	var save_data := {
		"buildings": _serialize_buildings(),
		"heroes": HeroSystem.get_heroes(),
		"resources": ResourceManager.get_all_resources(),
		"camera_position": _get_camera_position(),
	}
	var path := SAVE_DIR + "slot_%d.json" % slot
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		return false
	file.store_string(JSON.stringify(save_data, "	"))
	file.close()
	EventBus.game_saved.emit(slot)
	return true


func load_game(slot: int = 0) -> bool:
	var path := SAVE_DIR + "slot_%d.json" % slot
	if not FileAccess.file_exists(path):
		return false
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return false
	var text := file.get_as_text()
	file.close()
	var json := JSON.new()
	var error := json.parse(text)
	if error != OK:
		return false
	var data: Dictionary = json.data
	# Restore resources
	var resources: Dictionary = data.get("resources", {})
	for key in resources:
		ResourceManager.add_resource(key, resources[key])
	# Restore heroes
	var heroes: Array = data.get("heroes", [])
	for hero in heroes:
		HeroSystem.recruit_hero(hero)
	# Restore camera
	var cam_pos: Vector2 = Vector2.ZERO
	var cam_data = data.get("camera_position", null)
	if cam_data is Vector2:
		cam_pos = cam_data
	elif cam_data is Dictionary:
		cam_pos = Vector2(cam_data.get("x", 0), cam_data.get("y", 0))
	EventBus.game_loaded.emit(slot)
	return true


func has_save(slot: int = 0) -> bool:
	var path := SAVE_DIR + "slot_%d.json" % slot
	return FileAccess.file_exists(path)


func _serialize_buildings() -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for b in BuildingSystem.get_all_buildings():
		result.append({
			"id": b["id"],
			"grid_pos": {"x": b["grid_pos"].x, "y": b["grid_pos"].y},
			"data": b["data"],
		})
	return result


func _get_camera_position() -> Vector2:
	var cam := get_viewport().get_camera_2d()
	if cam:
		return cam.global_position
	return Vector2.ZERO
