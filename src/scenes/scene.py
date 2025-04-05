class Scene():
	def __init__(self):
		self._end_scene = False
		self._next_scene = None

	def input_key(self, key):
		pass
	
	def input_mouse(self, click, pos):
		pass

	def update(self, dt, mouse_pos):
		pass

	def draw(self, display):
		pass

	def is_done(self):
		return self._end_scene

	def get_next_scene(self):
		return self._next_scene
	
	def cleanup(self):
		pass