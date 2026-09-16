extends Control

## Main menu — New Game, Continue, Settings, Quit.

@onready var continue_button: Button = %ContinueButton


func _ready() -> void:
	continue_button.disabled = not SaveSystem.has_save()


func _on_new_game_button_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/main/game.tscn")


func _on_continue_button_pressed() -> void:
	if SaveSystem.has_save():
		get_tree().change_scene_to_file("res://scenes/main/game.tscn")
		SaveSystem.load_game()


func _on_settings_button_pressed() -> void:
	pass  # TODO: settings screen


func _on_quit_button_pressed() -> void:
	get_tree().quit()
