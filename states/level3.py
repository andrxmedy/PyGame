import pygame
from settings import WHITE, BLACK, WINDOW_WIDTH, WINDOW_HEIGHT
from characters import Player, Enemy
from perfil_jogador import PerfilJogador

class Level3:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 55)
        self.small_font = pygame.font.SysFont(None, 30)
        self.botao_voltar_image = pygame.image.load('botoes/wood_return.png')
        self.botao_voltar_image = pygame.transform.scale(self.botao_voltar_image, (50, 50))
        self.botao_voltar_rect = self.botao_voltar_image.get_rect(topleft=(10, 10))

        self.background_image = pygame.image.load('Fundo Fases/floresta.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.ground_height = 100
        self.ground_top = WINDOW_HEIGHT - self.ground_height

        self.player = Player(100, self.ground_top, 50, 50)
        
        self.enemies = [
            Enemy(300, 300, 50, 50, 'vespa', dificuldade=1),
            Enemy(400, 200, 50, 50, 'vespa', dificuldade=1),
            Enemy(300, 150, 50, 50, 'vespa', dificuldade=1),
            Enemy(500, 200, 50, 50, 'mosca', dificuldade=1),
            Enemy(540, 120, 50, 50, 'besouro', dificuldade=2),
            Enemy(300, 320, 50, 50, 'vespa', dificuldade=2),
            Enemy(380, 90, 50, 50, 'mosca', dificuldade=3),
            Enemy(100, 100, 50, 50, 'besouro', dificuldade=3),
            Enemy(255, 390, 50, 50, 'vespa', dificuldade=3),
        ]
        
        for enemy in self.enemies:
            enemy.set_player(self.player)
        
        self.perfil_jogador = PerfilJogador()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.botao_voltar_rect.collidepoint(pos):
                    from states.level_select import LevelSelect
                    self.game.change_state(LevelSelect(self.game))

    def verificar_colisao(self):
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                ponto_de_colisao = self.player.rect.clip(enemy.rect)
                rel_x = ponto_de_colisao.x - self.player.rect.x
                if self.player.atacando:
                    if self.player.direcao == 'direita' and rel_x > self.player.rect.width / 2:
                        self.enemies.remove(enemy)
                        if enemy.tipo == 'vespa':
                            self.player.capturados['Vespas'] += 1
                        elif enemy.tipo == 'mosca':
                            self.player.capturados['Moscas'] += 1
                        elif enemy.tipo == 'besouro':
                            self.player.capturados['Besouros'] += 1
                    elif self.player.direcao == 'esquerda' and rel_x < self.player.rect.width / 2:
                        self.enemies.remove(enemy)
                        if enemy.tipo == 'vespa':
                            self.player.capturados['Vespas'] += 1
                        elif enemy.tipo == 'mosca':
                            self.player.capturados['Moscas'] += 1
                        elif enemy.tipo == 'besouro':
                            self.player.capturados['Besouros'] += 1
                    else:
                        self.player.vida -= 1
                else:
                    self.player.vida -= 1

    def impedir_atravessar_chao(self, character):
        if character.position.y + character.rect.height > self.ground_top:
            character.position.y = self.ground_top - character.rect.height
            if isinstance(character, Player):
                character.velocity.y = 0
            else:
                character.velocity.y = -character.velocity.y

    def update(self):
        self.player.handle_input()
        self.player.update()

        if self.player.position.y < self.ground_top and self.player.velocity.y == 0:
            if self.player.status == 'pulando':
                self.player.status = 'caindo'
                self.player.velocity.y = 5

        if self.player.status == 'caindo':
            if self.player.position.y >= self.ground_top:
                self.player.position.y = self.ground_top
                self.player.velocity.y = 0
                self.player.status = 'parado'

        self.impedir_atravessar_chao(self.player)

        for enemy in self.enemies:
            enemy.update()
            self.impedir_atravessar_chao(enemy)

        self.verificar_colisao()

        if self.player.vida <= 0:
            from states.defeat import Defeat
            self.game.change_state(Defeat(self.game, 3))  # Ajuste o nível conforme necessário

        if not self.enemies:
            from states.victory import Victory
            self.perfil_jogador.niveis_completados['nivel3'] = True
            self.perfil_jogador.salvar_progresso()
            self.game.change_state(Victory(self.game, 3))

    def draw(self):
        self.game.screen.blit(self.background_image, (0, 0))

        # Renderizar o botão "VOLTAR"
        self.game.screen.blit(self.botao_voltar_image, self.botao_voltar_rect.topleft)

        # Definir a posição inicial para a exibição das informações
        info_y_start = self.botao_voltar_rect.bottom + 10

        # Renderizar a vida do jogador com porcentagem abaixo do botão
        vida_text = self.small_font.render(f'Vida: {self.player.vida}%', True, WHITE)
        vida_text_rect = vida_text.get_rect(topleft=(10, info_y_start))
        self.game.screen.blit(vida_text, vida_text_rect)

        # Espaçamento vertical para cada linha de informação
        info_spacing = 25

        # Renderizar informações sobre as capturas
        vespas_capturadas = self.player.capturados['Vespas']
        vespa_text = self.small_font.render(f'Vespas: {vespas_capturadas}', True, WHITE)
        vespa_text_rect = vida_text.get_rect(topleft=(10, info_y_start + info_spacing))
        self.game.screen.blit(vespa_text, vespa_text_rect)

        besouros_capturados = self.player.capturados['Besouros']
        besouro_text = self.small_font.render(f'Besouros: {besouros_capturados}', True, WHITE)
        besouro_text_rect = vida_text.get_rect(topleft=(10, info_y_start + 2 * info_spacing))
        self.game.screen.blit(besouro_text, besouro_text_rect)

        moscas_capturadas = self.player.capturados['Moscas']
        mosca_text = self.small_font.render(f'Moscas: {moscas_capturadas}', True, WHITE)
        mosca_text_rect = vida_text.get_rect(topleft=(10, info_y_start + 3 * info_spacing))
        self.game.screen.blit(mosca_text, mosca_text_rect)

        # Renderizar o jogador e os inimigos
        self.player.draw(self.game.screen)
        for enemy in self.enemies:
            enemy.draw(self.game.screen)

        pygame.display.flip()
