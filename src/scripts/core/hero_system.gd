extends Node

## Autoload singleton managing recruited heroes.

var _heroes: Dictionary = {}  # hero_id -> hero data


func recruit_hero(hero_data: Dictionary) -> bool:
	var hero_id: String = hero_data.get("id", "")
	if hero_id.is_empty() or _heroes.has(hero_id):
		return false
	_heroes[hero_id] = hero_data.duplicate()
	EventBus.hero_recruited.emit(hero_data)
	return true


func dismiss_hero(hero_id: String) -> bool:
	if not _heroes.has(hero_id):
		return false
	_heroes.erase(hero_id)
	return true


func get_heroes() -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for key in _heroes:
		result.append(_heroes[key])
	return result


func get_hero(hero_id: String) -> Dictionary:
	if _heroes.has(hero_id):
		return _heroes[hero_id]
	return {}
