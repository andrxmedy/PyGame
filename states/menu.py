# states/menu.py

import pygame
from settings import WHITE, BLACK, WINDOW_WIDTH, WINDOW_HEIGHT

class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 55)
        self.buttons = {
            "INICIAR": pygame.Rect(130, 160, 490, 120),
            "CRÉDITOS": pygame.Rect(130, 285, 490, 120),
            "SAIR": pygame.Rect(130, 410, 490, 120)
        }
        self.button_colors = {key: WHITE for key in self.buttons}

        # Carregar e redimensionar a imagem de fundo
        self.background_image = pygame.image.load('Bug eater.png')
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.buttons["INICIAR"].collidepoint(pos):
                    from states.level_select import LevelSelect
                    self.game.change_state(LevelSelect(self.game))
                elif self.buttons["CRÉDITOS"].collidepoint(pos):
                    from states.credits import Credits
                    self.game.change_state(Credits(self.game))
                elif self.buttons["SAIR"].collidepoint(pos):
                    self.game.running = False

    def update(self):
        pass

    def draw(self):
        # Desenhar a imagem de fundo
        self.game.screen.blit(self.background_image, (0, 0))

        # Desenhar os botões
        #for label, rect in self.buttons.items():
            #pygame.draw.rect(self.game.screen, self.button_colors[label], rect)
            #text = self.font.render(label, True, BLACK)
            #text_rect = text.get_rect(center=rect.center)
            #self.game.screen.blit(text, text_rect)

        pygame.display.flip()
