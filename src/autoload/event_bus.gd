extends Node

## Centralized signal bus for decoupled communication.

signal building_placed(building_data: Dictionary, grid_position: Vector2i)
signal resource_changed(resource_type: String, new_amount: int)
signal hero_recruited(hero_data: Dictionary)
signal game_saved(slot: int)
signal game_loaded(slot: int)
