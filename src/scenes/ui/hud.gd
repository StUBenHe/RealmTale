extends CanvasLayer

## Heads-up display — resource bar, action buttons.

@onready var gold_label: Label = %GoldLabel
@onready var iron_label: Label = %IronLabel
@onready var herbs_label: Label = %HerbsLabel
@onready var scrolls_label: Label = %ScrollsLabel
@onready var build_panel: PanelContainer = %BuildPanel


func _ready() -> void:
	_refresh_resources()
	EventBus.resource_changed.connect(_on_resource_changed)
	# Connect action buttons
	%BuildButton.pressed.connect(_on_build_pressed)
	%HeroesButton.pressed.connect(_on_heroes_pressed)
	%MapButton.pressed.connect(_on_map_pressed)
	%MenuButton.pressed.connect(_on_menu_pressed)


func _on_resource_changed(_type: String, _amount: int) -> void:
	_refresh_resources()


func _refresh_resources() -> void:
	gold_label.text = "Gold: %d" % ResourceManager.get_resource("gold")
	iron_label.text = "Iron: %d" % ResourceManager.get_resource("iron")
	herbs_label.text = "Herbs: %d" % ResourceManager.get_resource("herbs")
	scrolls_label.text = "Scrolls: %d" % ResourceManager.get_resource("scrolls")


func _on_build_pressed() -> void:
	build_panel.show_panel()


func _on_heroes_pressed() -> void:
	pass  # TODO: hero panel


func _on_map_pressed() -> void:
	pass  # TODO: map overlay


func _on_menu_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/ui/main_menu.tscn")
