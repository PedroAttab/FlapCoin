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
NEW_BACKGROUND_IMAGE = "new_background.jpeg"  # Novo fundo
NEW_GROUND_IMAGE = "new_chao.jpeg"  # Novo chão
NEW_OBSTACLE_IMAGE = "new_obstaculo.png"  # Novo obstáculo
COIN_IMAGES = ["bitcoin.png", "saga.png", "ethereum.png"]
FONT = pygame.font.Font(None, 40)
GRAVITY = 0.4
FLAP_STRENGTH = 9
MAX_JUMP_HEIGHT = 150
COIN_HEIGHT = 40
FLAP_SOUND = "flap.wav"  # Som de pulo
DEATH_SOUND = "death.wav"  # Som de morte
BACKGROUND_MUSIC = "background.wav"  # Música de fundo

# Inicializando o mixer de som do Pygame
pygame.mixer.init()

# Carregando sons
flap_sound = pygame.mixer.Sound(FLAP_SOUND)
death_sound = pygame.mixer.Sound(DEATH_SOUND)
pygame.mixer.music.load(BACKGROUND_MUSIC)

# Inicializando a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FlapCoin")

# Variáveis globais
score = 0

# Função para carregar imagens
def load_images():
    global background, ground, obstacle_image
    if score >= 50:
        background = pygame.image.load(NEW_BACKGROUND_IMAGE).convert()
        ground = pygame.image.load(NEW_GROUND_IMAGE).convert_alpha()
        obstacle_image = pygame.image.load(NEW_OBSTACLE_IMAGE).convert_alpha()
    else:
        background = pygame.image.load(BACKGROUND_IMAGE).convert()
        ground = pygame.image.load(GROUND_IMAGE).convert_alpha()
        obstacle_image = pygame.image.load(OBSTACLE_IMAGE).convert_alpha()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    ground = pygame.transform.scale(ground, (SCREEN_WIDTH, SCREEN_HEIGHT // 6))

# Carregando imagens iniciais
load_images()

# Classe para representar o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, coins):
        super().__init__()
        self.coins = coins
        self.index = 0
        self.image = self.coins[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = 0
        self.jumping = False

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0.4
        if self.rect.bottom >= SCREEN_HEIGHT - 50:  # Limitar ao topo do chão 
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.velocity = 0.4
            self.jumping = False

    def flap(self):
        if not self.jumping:
            self.velocity = -FLAP_STRENGTH
            flap_sound.play()  # Tocar som do pulo

    def change_coin(self):
        self.index = (self.index + 1) % len(self.coins)
        self.image = self.coins[self.index]
        self.mask = pygame.mask.from_surface(self.image)

# Classe para representar os obstáculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, inverted=False):
        super().__init__()
        self.image = obstacle_image
        self.rect = self.image.get_rect()
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y)
        else:
            self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
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
    return 0

# Função para exibir a tela inicial
def show_start_screen():
    screen.blit(background, (0, 0))
    title_text = FONT.render("FlapCoin", True, (255, 255, 255))
    start_text = FONT.render("Pressione espaço para iniciar", True, (255, 255, 255))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

# Função para aplicar filtro vermelho
def apply_red_filter():
    red_filter = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    red_filter.set_alpha(128)  # Valor de transparência
    red_filter.fill((255, 0, 0))
    screen.blit(red_filter, (0, 0))

# Carregando imagens das moedas
coin_images_resized = [pygame.transform.scale(pygame.image.load(image), (COIN_HEIGHT, COIN_HEIGHT)).convert_alpha() for image in COIN_IMAGES]

# Criando grupos de sprites
players = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Criando o jogador
player = Player(100, SCREEN_HEIGHT // 2, coin_images_resized)
players.add(player)

# Definindo variáveis do jogo
clock = pygame.time.Clock()
high_score = 0
game_active = False
show_start_screen_flag = True

# Temporizador para gerar obstáculos
obstacle_timer = pygame.time.get_ticks()

# Iniciar a música de fundo
pygame.mixer.music.play(-1)

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if show_start_screen_flag:
                    show_start_screen_flag = False
                    game_active = True
                    score = reset_game()
                elif not game_active:
                    game_active = True
                    score = reset_game()
                    pygame.mixer.music.play(-1)  # Reiniciar a música de fundo
                else:
                    player.flap()
            if event.key == pygame.K_c and game_active:  # Altera o personagem ao pressionar "C"
                player.change_coin()

    if show_start_screen_flag:
        show_start_screen()
    else:
        load_images()
        screen.blit(background, (0, 0))

        if game_active:
            player.update()
            players.draw(screen)

            if pygame.sprite.spritecollide(player, obstacles, False, pygame.sprite.collide_mask):
                game_active = False
                death_sound.play()  # Tocar som de morte
                pygame.mixer.music.stop()  # Parar música de fundo

            if player.rect.bottom >= SCREEN_HEIGHT - SCREEN_HEIGHT // 6:
                game_active = False
                death_sound.play()  # Tocar som de morte
                pygame.mixer.music.stop()  # Parar música de fundo

            obstacles.update()
            obstacles.draw(screen)

            score_text = FONT.render(f"Score: {int(score)}", True, (255, 255, 255))
            screen.blit(score_text, (20, 20))

            if score > high_score:
                high_score = score

            high_score_text = FONT.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
            screen.blit(high_score_text, (20, 60))

            for obstacle in obstacles:
                if obstacle.rect.right < player.rect.left and not obstacle.passed:
                    obstacle.passed = True
                    score += 0.5

            if pygame.time.get_ticks() - obstacle_timer > 2000:
                generate_obstacle()
                obstacle_timer = pygame.time.get_ticks()

        else:
            apply_red_filter()
            game_over_text = FONT.render("Game Over", True, (255, 255, 255))
            restart_text = FONT.render("Pressione espaço para jogar", True, (255, 255, 255))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

        screen.blit(ground, (0, SCREEN_HEIGHT - SCREEN_HEIGHT // 6))

        pygame.display.flip()
        clock.tick(60)
