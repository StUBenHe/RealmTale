extends Node

## Autoload singleton managing all player resources.

var _resources: Dictionary = {}


func _ready() -> void:
	# Initialize with starting resources from Config
	for key in Config.STARTING_RESOURCES:
		_resources[key] = Config.STARTING_RESOURCES[key]


func add_resource(type: String, amount: int) -> void:
	if not _resources.has(type):
		_resources[type] = 0
	_resources[type] += amount
	EventBus.resource_changed.emit(type, _resources[type])


func spend_resource(type: String, amount: int) -> bool:
	if not _resources.has(type):
		return false
	if _resources[type] < amount:
		return false
	_resources[type] -= amount
	EventBus.resource_changed.emit(type, _resources[type])
	return true


func can_afford(cost_dict: Dictionary) -> bool:
	for key in cost_dict:
		var cost: int = cost_dict[key]
		var current: int = _resources.get(key, 0)
		if current < cost:
			return false
	return true


func get_resource(type: String) -> int:
	return _resources.get(type, 0)


func get_all_resources() -> Dictionary:
	return _resources.duplicate()
