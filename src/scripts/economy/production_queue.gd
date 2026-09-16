extends Node

## Ticks every second — each building produces resources.

@onready var _timer: Timer = Timer.new()


func _ready() -> void:
	add_child(_timer)
	_timer.wait_time = 1.0
	_timer.timeout.connect(_on_timer_tick)
	_timer.start()


func _on_timer_tick() -> void:
	for b in BuildingSystem.get_all_buildings():
		var prod: Dictionary = b["data"].get("production", {})
		var level: int = b["data"].get("level", 1)
		for resource_type in prod:
			var amount: int = prod[resource_type] * level
			if amount > 0:
				ResourceManager.add_resource(resource_type, amount)
