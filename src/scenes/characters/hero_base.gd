extends CharacterBody2D

## Base hero node with stats and combat methods.

enum HeroClass { KNIGHT, WIZARD, ROGUE, CLERIC }

@export var hero_id: String = ""
@export var hero_name: String = ""
@export var hero_class: HeroClass = HeroClass.KNIGHT
@export var level: int = 1
@export var max_hp: int = 100
@export var hp: int = 100
@export var attack: int = 10
@export var defense: int = 10

@onready var sprite: Sprite2D = $Sprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D


func _ready() -> void:
	_update_texture()


func take_damage(amount: int) -> void:
	var actual_damage := maxi(amount - defense, 1)
	hp -= actual_damage
	hp = maxi(hp, 0)
	if hp <= 0:
		_on_death()


func heal(amount: int) -> void:
	hp = mini(hp + amount, max_hp)


func level_up() -> void:
	level += 1
	max_hp += 10
	hp = max_hp
	attack += 2
	defense += 1


func _on_death() -> void:
	queue_free()


func _update_texture() -> void:
	if not sprite:
		return
	var class_names := {
		HeroClass.KNIGHT: "knight",
		HeroClass.WIZARD: "wizard",
		HeroClass.ROGUE: "rogue",
		HeroClass.CLERIC: "cleric",
	}
	var path := "res://assets/characters/%s.png" % class_names.get(hero_class, "knight")
	if ResourceLoader.exists(path):
		sprite.texture = load(path)
