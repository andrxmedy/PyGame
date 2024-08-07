# states/level_select.py

import pygame
from settings import WHITE, BLACK, WINDOW_WIDTH, WINDOW_HEIGHT
from perfil_jogador import PerfilJogador

class LevelSelect:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 55)
        self.medium_font = pygame.font.SysFont(None, 40)
        self.small_font = pygame.font.SysFont(None, 24)
        self.buttons = {
            "NÍVEL 1": pygame.Rect(130, 160, 490, 120),
            "NÍVEL 2": pygame.Rect(130, 285, 490, 120),
            "NÍVEL 3": pygame.Rect(130, 410, 490, 120)
        }
        self.background_image = pygame.image.load('níveis.png')
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.perfil_jogador = PerfilJogador()

        # Botão de Voltar com imagem
        self.botao_voltar_image = pygame.image.load('botoes/wood_return.png')
        self.botao_voltar_image = pygame.transform.scale(self.botao_voltar_image, (50, 50))
        self.botao_voltar_rect = self.botao_voltar_image.get_rect(topleft=(10, 10))

        # Botões adicionais (menores)
        self.botao_salvar = pygame.Rect(10, WINDOW_HEIGHT - 40, 150, 30)
        self.botao_excluir = pygame.Rect(WINDOW_WIDTH - 160, WINDOW_HEIGHT - 40, 150, 30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.botao_voltar_rect.collidepoint(pos):
                    from states.menu import Menu
                    self.game.change_state(Menu(self.game))
                elif self.botao_salvar.collidepoint(pos):
                    self.perfil_jogador.salvar_progresso()
                elif self.botao_excluir.collidepoint(pos):
                    self.perfil_jogador.apagar_perfil()
                elif self.buttons["NÍVEL 1"].collidepoint(pos):
                    from states.level1 import Level1
                    self.game.change_state(Level1(self.game))
                elif self.buttons["NÍVEL 2"].collidepoint(pos) and self.perfil_jogador.niveis_completados['nivel1']:
                    from states.level2 import Level2
                    self.game.change_state(Level2(self.game))
                elif self.buttons["NÍVEL 3"].collidepoint(pos) and self.perfil_jogador.niveis_completados['nivel2']:
                    from states.level3 import Level3
                    self.game.change_state(Level3(self.game))

    def update(self):
        pass

    def draw(self):
        self.game.screen.blit(self.background_image, (0, 0))

        self.game.screen.blit(self.botao_voltar_image, self.botao_voltar_rect.topleft)

        pygame.draw.rect(self.game.screen, WHITE, self.botao_salvar)
        salvar_text = self.small_font.render('salvar', True, BLACK)
        salvar_text_rect = salvar_text.get_rect(center=self.botao_salvar.center)
        self.game.screen.blit(salvar_text, salvar_text_rect)

        pygame.draw.rect(self.game.screen, WHITE, self.botao_excluir)
        excluir_text = self.small_font.render('excluir perfil', True, BLACK)
        excluir_text_rect = excluir_text.get_rect(center=self.botao_excluir.center)
        self.game.screen.blit(excluir_text, excluir_text_rect)

        niveis_completados = sum(self.perfil_jogador.niveis_completados.values())
        niveis_text = self.medium_font.render(f'NÍVEIS: {niveis_completados}/3', True, WHITE)
        niveis_text_rect = niveis_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 30))
        self.game.screen.blit(niveis_text, niveis_text_rect)

        pygame.display.flip()
