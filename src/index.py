import pygame
import constants

from level import Level

def main():
	display = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
	pygame.display.set_caption("Game")
		
	level = Level(constants.TEST_LEVEL, constants.TILE_SIZE)

	pygame.init()
	level.all_sprites.draw(display)
      
	running = True
    
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		
		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
    main()