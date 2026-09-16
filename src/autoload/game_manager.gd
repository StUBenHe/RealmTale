extends Node

## Game state machine — manages MENU, PLAYING, PAUSED states.

enum State { MENU, PLAYING, PAUSED }

signal state_changed(old_state: State, new_state: State)

var current_state: State = State.MENU


func change_state(new_state: State) -> void:
	if new_state == current_state:
		return
	var old := current_state
	current_state = new_state
	match new_state:
		State.PLAYING:
			get_tree().paused = false
		State.PAUSED:
			get_tree().paused = true
		State.MENU:
			get_tree().paused = false
	state_changed.emit(old, new_state)


func is_playing() -> bool:
	return current_state == State.PLAYING
