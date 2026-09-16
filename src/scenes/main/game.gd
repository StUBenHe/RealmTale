extends Node2D

## Root game scene — initializes systems and handles global input.

@onready var world: Node2D = $World
@onready var hud: CanvasLayer = $HUD


func _ready() -> void:
	GameManager.change_state(GameManager.State.PLAYING)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		if GameManager.current_state == GameManager.State.PLAYING:
			GameManager.change_state(GameManager.State.PAUSED)
			get_tree().paused = true
		elif GameManager.current_state == GameManager.State.PAUSED:
			GameManager.change_state(GameManager.State.PLAYING)
			get_tree().paused = false
