import pygame

class Character:
    def __init__(self, x, y, width, height, image_path):
        self.image = pygame.image.load(image_path)
        self.rect = pygame.Rect(x, y, width, height)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

    def draw(self, screen):
        screen.blit(self.image, (self.position.x, self.position.y))

    def update(self):
        self.position += self.velocity
        self.rect.topleft = (self.position.x, self.position.y)

class Player(Character):
    def __init__(self, x, y, width, height):
        # Define o caminho das imagens
        self.default_image_path = 'sprites_sapo/sapo.png'
        self.attack_image_path = 'sprites_sapo/sapo_ataque.png'
        self.jump_image_path = 'sprites_sapo/sapo_pulo.png'
        self.fall_image_path = 'sprites_sapo/sapo_queda.png'
        
        # Chama a superclasse com a imagem padrão
        super().__init__(x, y, width, height, self.default_image_path)
        
        self.status = 'parado'
        self.direcao = 'direita'
        self.atacando = False
        self.vida = 100
        self.capturados = {'Moscas': 0, 'Vespas': 0, 'Besouros': 0}

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.velocity.x = 5
            self.direcao = 'direita'
        elif keys[pygame.K_LEFT]:
            self.velocity.x = -5
            self.direcao = 'esquerda'
        else:
            self.velocity.x = 0

        if keys[pygame.K_UP] and self.status != 'caindo':
            self.velocity.y = -5
        else:
            if self.status == 'pulando':
                self.velocity.y = 5
                self.status = 'caindo'

        if self.velocity.x != 0 and self.velocity.y == 0:
            self.status = 'andando'
        elif self.velocity.y < 0:
            self.status = 'pulando'
        elif self.velocity.y > 0:
            self.status = 'caindo'
        else:
            self.status = 'parado'

        if keys[pygame.K_SPACE]:
            self.atacando = True
        else:
            self.atacando = False

    def sprite_player(self):
        # Carrega a imagem padrão
        image_path = self.default_image_path
        
        # Muda o caminho da imagem baseado no status
        if self.atacando:
            image_path = self.attack_image_path
        elif self.status == 'pulando':
            image_path = self.jump_image_path
        elif self.status == 'caindo':
            image_path = self.fall_image_path
        
        self.image = pygame.image.load(image_path)
        
        # Espelha horizontalmente se a direção for esquerda
        if self.direcao == 'esquerda':
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.handle_input()
        self.sprite_player()
        super().update()

class Enemy(Character):
    def __init__(self, x, y, width, height, tipo, dificuldade=1):
        # Define os caminhos das imagens baseados no tipo
        if tipo == 'vespa':
            image_path = 'sprites_vespa/vespa.png'
        elif tipo == 'mosca':
            image_path = 'sprites_mosca/mosca.png'
        elif tipo == 'besouro':
            image_path = 'sprites_besouro/besouro.png'
        else:
            raise ValueError(f'Tipo de inimigo desconhecido: {tipo}')
        
        super().__init__(x, y, width, height, image_path)
        self.tipo = tipo
        self.dificuldade = dificuldade
        self.orientation = 'horizontal' if tipo in ['vespa', 'besouro'] else 'vertical'
        self.velocity = pygame.Vector2(2, 0) if self.orientation == 'horizontal' else pygame.Vector2(0, 2)
        self.player = None  # Só virá a existir jogador instanciado nos níveis

    def set_player(self, player):
        self.player = player #define onde está o player

    def move_horizontal(self):
        if self.position.x <= 0 or self.position.x + self.rect.width >= pygame.display.get_surface().get_width():
            self.velocity.x = -self.velocity.x
            self.image = pygame.transform.flip(self.image, True, False) #Espelha quadno muda a direcao
        self.position += self.velocity
        self.rect.topleft = (self.position.x, self.position.y)

    def move_vertical(self):
        if self.position.y <= 0 or self.position.y + self.rect.height >= pygame.display.get_surface().get_height():
            self.velocity.y = -self.velocity.y
        self.position += self.velocity
        self.rect.topleft = (self.position.x, self.position.y)

    def move_towards_player(self, speed):
        if self.player:
            direction = pygame.Vector2(self.player.position.x - self.position.x, self.player.position.y - self.position.y)
            distance = direction.length()
            if distance != 0:
                direction.normalize_ip()
                self.velocity = direction * speed  # Velocidade ajustada conforme a dificuldade
                self.position += self.velocity
                self.rect.topleft = (self.position.x, self.position.y)

    def update(self):
        if self.dificuldade == 1:
            if self.orientation == 'horizontal':
                self.move_horizontal()
            else:
                self.move_vertical()
        elif self.dificuldade == 2:
            self.move_towards_player(1)
        else:
            self.move_towards_player(2)
        super().update()
