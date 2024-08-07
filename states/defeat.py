# states/defeat.py

import pygame
from settings import WHITE, WINDOW_WIDTH, WINDOW_HEIGHT

class Defeat:
    def __init__(self, game, level):
        self.game = game
        self.level = level

        # Configuração da fonte
        self.font = pygame.font.SysFont(None, 55)
        self.small_font = pygame.font.SysFont(None, 30)
        
        # Definição da imagem de fundo com base no nível
        if level == 1:
            self.background_image = pygame.image.load('Fundo Fases/swamp.jpg')
        elif level == 2:
            self.background_image = pygame.image.load('Fundo Fases/esgoto.jpg')
        elif level == 3:
            self.background_image = pygame.image.load('Fundo Fases/floresta.jpg')

        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Definição do botão de voltar
        self.return_button = pygame.Rect(WINDOW_WIDTH / 2 - 75, WINDOW_HEIGHT / 2 + 60, 150, 40)
        self.return_button_color = (0, 0, 0)
        self.return_button_hover_color = (100, 100, 100)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    from states.level_select import LevelSelect
                    self.game.change_state(LevelSelect(self.game))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.return_button.collidepoint(pygame.mouse.get_pos()):
                    from states.level_select import LevelSelect
                    self.game.change_state(LevelSelect(self.game))
    
    def update(self):
        pass

    def draw(self):
        self.game.screen.blit(self.background_image, (0, 0))
        
        # Desenhar o texto de derrota
        text_color = (255, 0, 0)  # Vermelho
        defeat_text = self.font.render(f'VOCÊ PERDEU O NÍVEL {self.level}', True, text_color)
        text_rect = defeat_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 20))
        self.game.screen.blit(defeat_text, text_rect)
        
        # Desenhar o botão de voltar
        mouse_pos = pygame.mouse.get_pos()
        if self.return_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.game.screen, self.return_button_hover_color, self.return_button)
        else:
            pygame.draw.rect(self.game.screen, self.return_button_color, self.return_button)
        
        return_button_text = self.small_font.render('Voltar', True, WHITE)
        return_button_text_rect = return_button_text.get_rect(center=self.return_button.center)
        self.game.screen.blit(return_button_text, return_button_text_rect)

        pygame.display.flip()
