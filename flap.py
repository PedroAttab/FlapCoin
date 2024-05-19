import pygame
import random
import sys

# Inicializando o Pygame
pygame.init()

# Definindo constantes
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BACKGROUND_IMAGE = "background.jpeg"
GROUND_IMAGE = "chao.jpeg"
OBSTACLE_IMAGE = "obstaculo.png"
COIN_IMAGES = ["bitcoin.png", "saga.png", "ethereum.png"]
FONT = pygame.font.Font(None, 40)
GRAVITY = 0.4
FLAP_STRENGTH = 9
MAX_JUMP_HEIGHT = 150
COIN_HEIGHT = 40

# Classe para representar o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, coins):
        super().__init__()
        self.coins = coins
        self.index = 0
        self.image = self.coins[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = 0
        self.jumping = False

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= SCREEN_HEIGHT - 50:  # Limitar ao topo do chão
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.velocity = 0
            self.jumping = False

    def flap(self):
        if not self.jumping:
            self.velocity = -FLAP_STRENGTH

    def change_coin(self):
        self.index = (self.index + 1) % len(self.coins)
        self.image = self.coins[self.index]

# Classe para representar os obstáculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, inverted=False):
        super().__init__()
        self.image = pygame.image.load(OBSTACLE_IMAGE)
        self.rect = self.image.get_rect()
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y)
        else:
            self.rect.topleft = (x, y)
        self.velocity = -3
        self.passed = False  # Flag para verificar se o jogador já passou por esse obstáculo

    def update(self):
        self.rect.x += self.velocity
