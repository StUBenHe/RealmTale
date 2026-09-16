extends Area2D

## Base building node — placed on the grid, produces resources.

@export var building_id: String = ""
@export var building_name: String = ""
@export var level: int = 1
@export var max_level: int = 5
@export var production_rate: Dictionary = {}
@export var cost: Dictionary = {}

@onready var sprite: Sprite2D = $Sprite2D
@onready var label: Label = $Label


func _ready() -> void:
	_update_label()
	_update_texture()


func upgrade() -> void:
	if level >= max_level:
		return
	level += 1
	_update_label()
	_update_texture()


func get_info() -> Dictionary:
	return {
		"id": building_id,
		"name": building_name,
		"level": level,
		"max_level": max_level,
		"production": production_rate,
		"cost": cost,
	}


func _update_label() -> void:
	if label:
		label.text = "%s Lv.%d" % [building_name, level]


func _update_texture() -> void:
	if not sprite or building_id.is_empty():
		return
	var path := "res://assets/buildings/%s_lv%d.png" % [building_id, level]
	if ResourceLoader.exists(path):
		sprite.texture = load(path)
