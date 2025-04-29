from dataclasses import dataclass
from ui.button import Button
from constants import SceneName


@dataclass
class ButtonInfo:
    button: Button
    next_scene: SceneName
    next_scene_data: any
    scrollable: bool = False
