extends Camera2D

## Smooth camera with WASD panning, zoom, middle-mouse drag, edge scrolling.

@export var pan_speed: float = 400.0
@export var zoom_speed: float = 0.1
@export var min_zoom: float = 0.5
@export var max_zoom: float = 3.0
@export var edge_scroll_speed: float = 20.0
@export var edge_scroll_margin: int = 20
@export var smooth_factor: float = 0.15

var _target_position: Vector2 = Vector2.ZERO
var _dragging: bool = false


func _ready() -> void:
	_target_position = global_position


func _unhandled_input(event: InputEvent) -> void:
	# Middle-mouse drag
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_MIDDLE:
			_dragging = event.pressed
			return
	# Zoom
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			_change_zoom(-zoom_speed)
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			_change_zoom(zoom_speed)


func _process(delta: float) -> void:
	var input_dir := Vector2.ZERO
	if Input.is_action_pressed("camera_move_up"):
		input_dir.y -= 1.0
	if Input.is_action_pressed("camera_move_down"):
		input_dir.y += 1.0
	if Input.is_action_pressed("camera_move_left"):
		input_dir.x -= 1.0
	if Input.is_action_pressed("camera_move_right"):
		input_dir.x += 1.0

	# Middle-mouse drag
	if _dragging:
		input_dir -= get_viewport().get_mouse_position() / get_viewport_rect().size * 2.0 - Vector2.ONE
		input_dir = -input_dir.normalized()

	# Edge scrolling
	var mouse_pos := get_viewport().get_mouse_position()
	var vp_size := get_viewport_rect().size
	if mouse_pos.x < edge_scroll_margin:
		input_dir.x -= 1.0
	elif mouse_pos.x > vp_size.x - edge_scroll_margin:
		input_dir.x += 1.0
	if mouse_pos.y < edge_scroll_margin:
		input_dir.y -= 1.0
	elif mouse_pos.y > vp_size.y - edge_scroll_margin:
		input_dir.y += 1.0

	if input_dir.length() > 0:
		_target_position += input_dir.normalized() * pan_speed * delta / zoom.x

	global_position = global_position.lerp(_target_position, smooth_factor)


func _change_zoom(delta: float) -> void:
	var new_zoom := zoom.x + delta
	new_zoom = clampf(new_zoom, min_zoom, max_zoom)
	zoom = Vector2(new_zoom, new_zoom)
