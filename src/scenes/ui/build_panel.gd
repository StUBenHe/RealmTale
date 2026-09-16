extends PanelContainer

## Side panel listing buildable buildings with cost and build button.

@onready var building_list: VBoxContainer = %BuildingList
@onready var close_button: Button = %CloseButton

var _buildings_data: Array = []


func _ready() -> void:
	visible = false
	close_button.pressed.connect(_on_close_pressed)
	_load_buildings_data()


func show_panel() -> void:
	visible = true


func hide_panel() -> void:
	visible = false


func _load_buildings_data() -> void:
	var file := FileAccess.open("res://data/buildings.json", FileAccess.READ)
	if file == null:
		return
	var json := JSON.new()
	var error := json.parse(file.get_as_text())
	if error != OK:
		return
	var data: Dictionary = json.data
	_buildings_data = data.get("buildings", [])
	_populate_list()


func _populate_list() -> void:
	# Clear existing entries
	for child in building_list.get_children():
		child.queue_free()

	for bdata in _buildings_data:
		var entry := PanelContainer.new()
		var hbox := HBoxContainer.new()
		hbox.add_theme_constant_override("separation", 10)

		# Icon placeholder
		var icon_rect := ColorRect.new()
		icon_rect.custom_minimum_size = Vector2(48, 48)
		icon_rect.color = Color.DARK_GRAY
		hbox.add_child(icon_rect)

		# Info column
		var info_vbox := VBoxContainer.new()
		var name_label := Label.new()
		name_label.text = bdata.get("name", "Unknown")
		info_vbox.add_child(name_label)
		var cost_label := Label.new()
		cost_label.text = _format_cost(bdata.get("base_cost", {}))
		cost_label.add_theme_font_size_override("font_size", 12)
		info_vbox.add_child(cost_label)
		hbox.add_child(info_vbox)

		# Build button
		var btn := Button.new()
		btn.text = "Build"
		btn.pressed.connect(_on_build_pressed.bind(bdata))
		hbox.add_child(btn)

		entry.add_child(hbox)
		building_list.add_child(entry)


func _format_cost(cost_dict: Dictionary) -> String:
	var parts: Array[String] = []
	for key in cost_dict:
		parts.append("%s: %d" % [key.capitalize(), cost_dict[key]])
	return " | ".join(parts)


func _on_build_pressed(building_data: Dictionary) -> void:
	var grid_pos := Vector2i(0, 0)  # Default; actual placement handled by World
	EventBus.building_placed.emit(building_data, grid_pos)


func _on_close_pressed() -> void:
	hide_panel()
