class Scene():
    def __init__(self):
        self._next_scene = None

    def input_key(self, key):
        pass

    def input_mouse(self, click, pos):
        pass

    def update(self, dt, mouse_pos):
        pass

    def input_raw(self, event):
        pass

    def draw(self, display):
        pass

    def is_done(self):
        return self._next_scene is not None

    def get_next_scene(self):
        return self._next_scene[0] if self._next_scene else None

    def get_next_scene_data(self):
        return self._next_scene[1] if self._next_scene else None

    def set_next_scene(self, scene, data=None):
        self._next_scene = (scene, data)

    def cleanup(self):
        pass
