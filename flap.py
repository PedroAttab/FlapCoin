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

# Função para gerar obstáculos
def generate_obstacle():
    gap_y = random.randint(100, 200)  # Ajuste do intervalo entre os obstáculos de cima e de baixo
    top_obstacle = Obstacle(SCREEN_WIDTH, gap_y - 100, inverted=True)  # Ajuste do espaço entre os obstáculos
    bottom_obstacle = Obstacle(SCREEN_WIDTH, gap_y + 150)  # Ajuste para o obstáculo de baixo ficar abaixo do chão
    obstacles.add(top_obstacle)
    obstacles.add(bottom_obstacle)

# Função para reiniciar o jogo
def reset_game():
    player.rect.center = (100, SCREEN_HEIGHT // 2)
    player.velocity = 0
    player.jumping = False
    obstacles.empty()
    score = 0

# Inicializando a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FlapCoin")

# Carregando imagens
background = pygame.image.load(BACKGROUND_IMAGE).convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
ground = pygame.image.load(GROUND_IMAGE).convert_alpha()
chao_altura = SCREEN_HEIGHT // 6
ground = pygame.transform.scale(ground, (SCREEN_WIDTH, chao_altura))

# Criando grupos de sprites
players = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Carregando imagens das moedas
coin_images_resized = [pygame.transform.scale(pygame.image.load(image), (COIN_HEIGHT, COIN_HEIGHT)).convert_alpha() for image in COIN_IMAGES]

# Criando o jogador
player = Player(100, SCREEN_HEIGHT // 2, coin_images_resized)
players.add(player)

# Definindo variáveis do jogo
clock = pygame.time.Clock()
score = 0
high_score = 0
game_active = True

# Temporizador para gerar obstáculos
obstacle_timer = pygame.time.get_ticks()

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                player.flap()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                reset_game()
                score = 0
            if event.key == pygame.K_c:  # Altera o personagem ao pressionar "C"
                player.change_coin()

    screen.blit(background, (0, 0))  

    if game_active:
        player.update()
        players.draw(screen)

        if pygame.sprite.spritecollide(player, obstacles, False):
            game_active = False  

        if player.rect.bottom >= SCREEN_HEIGHT - chao_altura:
            game_active = False  

        obstacles.update()
        obstacles.draw(screen)

        score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        if score > high_score:
            high_score = score

        high_score_text = FONT.render(f"High Score: {high_score}", True, (255, 255, 255))
        screen.blit(high_score_text, (20, 60))

        for obstacle in obstacles:
            if obstacle.rect.right < player.rect.left and not obstacle.passed:
                obstacle.passed = True
                score += 1

        if pygame.time.get_ticks() - obstacle_timer > 2000:
            generate_obstacle()
            obstacle_timer = pygame.time.get_ticks()

    screen.blit(ground, (0, SCREEN_HEIGHT - chao_altura))  

    pygame.display.flip()
    clock.tick(60)