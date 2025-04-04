import pygame

class GameLoop:
	def __init__(self, level, renderer, event_queue, clock, input):
		self._level = level
		self._renderer = renderer
		self._event_queue = event_queue
		self._clock = clock
		self._input = input

	def start(self):
		while True:
			if self._handle_events() == False:
				break

			self._handle_input()

			self._level.update(self._clock.get_dt(), self._input.get_mouse_pos())

			self._render()

			self._clock.tick(240)

	def _handle_events(self):
		for event in self._event_queue.get():
			# if event.type == pygame.KEYDOWN:
			# 	if event.key == pygame.K_LEFT or event.key == pygame.K_a:
			# 		self._level.input_key("left")
			# 	if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
			# 		self._level.input_key("right")
			# 	if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
			# 		self._level.input_key("jump")
			# 	if event.key == pygame.K_DOWN or event.key == pygame.K_s:
			# 		self._level.input_key("down")
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					self._level.input_mouse("left", event.pos)
				if event.button == 3:	
					self._level.input_mouse("right", event.pos)
			elif event.type == pygame.QUIT:
				return False
			
	def _handle_input(self):
		keys = self._input.get_pressed()
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self._level.input_key("left")
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self._level.input_key("right")
		if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
			self._level.input_key("jump")
		if keys[pygame.K_DOWN] or keys[pygame.K_s]:
			self._level.input_key("down")

	def _render(self):
		self._renderer.render()