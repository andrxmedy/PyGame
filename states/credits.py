# states/credits.py

import pygame
from settings import WHITE, BLACK, WINDOW_WIDTH, WINDOW_HEIGHT

class Credits:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 55)
        
        # Carregar a imagem de fundo
        self.background_image = pygame.image.load('creditos/creditos.png')
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Carregar a imagem do botão "VOLTAR"
        self.botao_voltar_image = pygame.image.load('botoes/wood_return.png')
        self.botao_voltar_image = pygame.transform.scale(self.botao_voltar_image, (50, 50))
        self.botao_voltar_rect = self.botao_voltar_image.get_rect(topleft=(10, 10))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.botao_voltar_rect.collidepoint(pos):
                    from states.menu import Menu
                    self.game.change_state(Menu(self.game))

    def update(self):
        pass

    def draw(self):
        self.game.screen.blit(self.background_image, (0, 0))

        # Desenhar o botão "VOLTAR"
        self.game.screen.blit(self.botao_voltar_image, self.botao_voltar_rect.topleft)

        pygame.display.flip()
