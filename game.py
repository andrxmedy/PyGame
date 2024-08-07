# game.py

import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from states.menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = Menu(self)
        
    def change_state(self, new_state):
        self.state = new_state
    
    def run(self):
        while self.running:
            self.state.handle_events()
            self.state.update()
            self.state.draw()
            self.clock.tick(60)

    def quit(self):
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
