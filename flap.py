import pygame
import random
import sys

# Inicializando o Pygame
pygame.init()

# Definindo constantes
LARGURA_TELA = 400
ALTURA_TELA = 600
IMAGEM_FUNDO = "background.jpeg"
IMAGEM_CHAO = "chao.jpeg"
IMAGEM_OBSTACULO = "obstaculo.png"
NOVA_IMAGEM_FUNDO = "new_background.jpeg"  # Novo fundo
NOVA_IMAGEM_CHAO = "new_chao.jpeg"  # Novo chão
NOVA_IMAGEM_OBSTACULO = "new_obstaculo.png"  # Novo obstáculo
IMAGENS_MOEDAS = ["bitcoin.png", "saga.png", "ethereum.png"]
FONTE = pygame.font.Font(None, 40)
GRAVIDADE = 0.4
FORCA_DO_PULO = 9
ALTURA_MAXIMA_DO_PULO = 150
ALTURA_MOEDA = 40
SOM_PULO = "flap.wav"  # Som de pulo
SOM_MORTE = "death.wav"  # Som de morte
MUSICA_DE_FUNDO = "background.wav"  # Música de fundo

# Inicializando o mixer de som do Pygame
pygame.mixer.init()

# Carregando sons
som_pulo = pygame.mixer.Sound(SOM_PULO)
som_morte = pygame.mixer.Sound(SOM_MORTE)
pygame.mixer.music.load(MUSICA_DE_FUNDO)

# Inicializando a tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("FlapCoin")

# Variáveis globais
pontuacao = 0

# Função para carregar imagens
def carregar_imagens():
    global fundo, chao, imagem_obstaculo #Troca imagens quando atingir determinada pontuação, simulando uma troca de fase
    if pontuacao >= 50: 
        fundo = pygame.image.load(NOVA_IMAGEM_FUNDO).convert() #Uso do convert para colocar no formato do pygame
        chao = pygame.image.load(NOVA_IMAGEM_CHAO).convert_alpha()
        imagem_obstaculo = pygame.image.load(NOVA_IMAGEM_OBSTACULO).convert_alpha()
    else:
        fundo = pygame.image.load(IMAGEM_FUNDO).convert() 
        chao = pygame.image.load(IMAGEM_CHAO).convert_alpha()
        imagem_obstaculo = pygame.image.load(IMAGEM_OBSTACULO).convert_alpha()
    fundo = pygame.transform.scale(fundo, (LARGURA_TELA, ALTURA_TELA))
    chao = pygame.transform.scale(chao, (LARGURA_TELA, ALTURA_TELA // 6))

# Carregando imagens iniciais
carregar_imagens()

# Classe para representar o jogador + Sprite
class Jogador(pygame.sprite.Sprite): 
    def __init__(self, x, y, moedas):
        super().__init__()
        self.moedas = moedas 
        self.indice = 0
        self.image = self.moedas[self.indice] #Definindo as skins que o jogador pode assumir
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) 
        self.mask = pygame.mask.from_surface(self.image) #Método para verificar colisões
        self.velocidade = 0 #Determinada velocidade inicial (começa parado)
        self.pulando = False

    def update(self):
        self.velocidade += GRAVIDADE #Uso do parâmetro para simulação da gravidade
        self.rect.y += self.velocidade #Atualização da posição (eixo y) a partir da velocidade
        if self.rect.top <= 0: #Verificação de posição do jogador no mapa
            self.rect.top = 0
            self.velocidade = 0.4
        if self.rect.bottom >= ALTURA_TELA - 50:  # Limitar ao topo do chão 
            self.rect.bottom = ALTURA_TELA - 50
            self.velocidade = 0.4 #Impede que o jogador saia do mapa
            self.pulando = False

    def pular(self):
        if not self.pulando:
            self.velocidade = -FORCA_DO_PULO
            som_pulo.play()  # Tocar som do pulo

    def trocar_moeda(self): #Trocar moeda utilizada e garantia de rodar todas as skins
        self.indice = (self.indice + 1) % len(self.moedas)
        self.image = self.moedas[self.indice]
        self.mask = pygame.mask.from_surface(self.image)

# Classe para representar os obstáculos
class Obstaculo(pygame.sprite.Sprite): #Utilização do Sprite para detecção dessas colisões
    def __init__(self, x, y, invertido=False):
        super().__init__()
        self.image = imagem_obstaculo #Definição da imagem do obstáculo
        self.rect = self.image.get_rect() #Definição do retângulo para localização e tamanho do Sprite
        if invertido:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y)
        else:
            self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.velocidade = -3
        self.passado = False  # Flag para verificar se o jogador já passou por esse obstáculo

    def update(self):
        self.rect.x += self.velocidade #Atualização frame por frame

# Função para gerar obstáculos
def gerar_obstaculo():
    y_gap = random.randint(100, 200)  # Ajuste do intervalo entre os obstáculos de cima e de baixo
    obstaculo_cima = Obstaculo(LARGURA_TELA, y_gap - 100, invertido=True)  # Ajuste do espaço entre os obstáculos
    obstaculo_baixo = Obstaculo(LARGURA_TELA, y_gap + 150)  # Ajuste para o obstáculo de baixo ficar abaixo do chão
    obstaculos.add(obstaculo_cima)
    obstaculos.add(obstaculo_baixo)

# Função para reiniciar o jogo
def reiniciar_jogo():
    jogador.rect.center = (100, ALTURA_TELA // 2) #Devolve o "Jogador" para sua posição inicial
    jogador.velocidade = 0 #Reseta velocidade
    jogador.pulando = False #"Jogador" para de pular
    obstaculos.empty() #Ausencia de obstáculos no começo
    return 0

# Função para exibir a tela inicial e fornecer o info de instruções
def mostrar_tela_inicial():
    tela.blit(fundo, (0, 0))
    texto_titulo = FONTE.render("FlapCoin", True, (255, 255, 255))
    texto_inicio = FONTE.render("Pressione espaço para iniciar", True, (255, 255, 255))
    tela.blit(texto_titulo, (LARGURA_TELA // 2 - texto_titulo.get_width() // 2, ALTURA_TELA // 3))
    tela.blit(texto_inicio, (LARGURA_TELA // 2 - texto_inicio.get_width() // 2, ALTURA_TELA // 2))
    pygame.display.flip()

# Função para aplicar filtro vermelho
def aplicar_filtro_vermelho():
    filtro_vermelho = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
    filtro_vermelho.set_alpha(128)  # Valor de transparência
    filtro_vermelho.fill((255, 0, 0))
    tela.blit(filtro_vermelho, (0, 0))

# Carregando imagens das moedas
imagens_moedas_redimensionadas = [pygame.transform.scale(pygame.image.load(imagem), (ALTURA_MOEDA, ALTURA_MOEDA)).convert_alpha() for imagem in IMAGENS_MOEDAS]

# Criando grupos de sprites
jogadores = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()

# Criando o jogador
jogador = Jogador(100, ALTURA_TELA // 2, imagens_moedas_redimensionadas)
jogadores.add(jogador)

# Definindo variáveis do jogo
relógio = pygame.time.Clock()
pontuacao_maxima = 0
jogo_ativo = False
mostrar_tela_inicial_flag = True

# Temporizador para gerar obstáculos
temporizador_obstaculo = pygame.time.get_ticks()

# Iniciar a música de fundo
pygame.mixer.music.play(-1)

# Loop principal do jogo
while True: #Loop que mantém o jogo em execução 
    for evento in pygame.event.get(): #Atualiza sobre os eventos do pygame
        if evento.type == pygame.QUIT: #Encerramento do programa
            pygame.quit() 
            sys.exit() 
        if evento.type == pygame.KEYDOWN: #Verificação de teclas
            if evento.key == pygame.K_SPACE: #Itera sobre a atividade do jogo (está acontecendo ou não)
                if mostrar_tela_inicial_flag:
                    mostrar_tela_inicial_flag = False
                    jogo_ativo = True
                    pontuacao = reiniciar_jogo()
                elif not jogo_ativo:
                    jogo_ativo = True
                    pontuacao = reiniciar_jogo()
                    pygame.mixer.music.play(-1)  # Reiniciar a música de fundo
                else:
                    jogador.pular()
            if evento.key == pygame.K_c and jogo_ativo:  # Altera o personagem ao pressionar "C"
                jogador.trocar_moeda()

    if mostrar_tela_inicial_flag:
        mostrar_tela_inicial()
    else:
        carregar_imagens()
        tela.blit(fundo, (0, 0))

        if jogo_ativo:
            jogador.update()
            jogadores.draw(tela)

            if pygame.sprite.spritecollide(jogador, obstaculos, False, pygame.sprite.collide_mask): #Vericação das colisões para iteração do loop
                jogo_ativo = False
                som_morte.play()  # Tocar som de morte
                pygame.mixer.music.stop()  # Parar música de fundo

            if jogador.rect.bottom >= ALTURA_TELA - ALTURA_TELA // 6:
                jogo_ativo = False
                som_morte.play()  # Tocar som de morte
                pygame.mixer.music.stop()  # Parar música de fundo

            obstaculos.update() #Determinação dos obstáculos 
            obstaculos.draw(tela)

            texto_pontuacao = FONTE.render(f"Pontuação: {int(pontuacao)}", True, (255, 255, 255)) #Desenho da pontuação (caixa de texto é criada)
            tela.blit(texto_pontuacao, (20, 20))

            if pontuacao > pontuacao_maxima: 
                pontuacao_maxima = pontuacao

            texto_pontuacao_maxima = FONTE.render(f"Pontuação Máxima: {int(pontuacao_maxima)}", True, (255, 255, 255))
            tela.blit(texto_pontuacao_maxima, (20, 60))

            for obstaculo in obstaculos: #Análise da passagem dos obstáculos
                if obstaculo.rect.right < jogador.rect.left and not obstaculo.passado:
                    obstaculo.passado = True
                    pontuacao += 0.5

            if pygame.time.get_ticks() - temporizador_obstaculo > 2000: #Permite definição do intervalo de obstáculos (2 em 2 seg)
                gerar_obstaculo()
                temporizador_obstaculo = pygame.time.get_ticks() #Atualiza o temporizador 

        else: #Iterações no caso de colisões ("Game Over" definido)
            aplicar_filtro_vermelho()
            texto_fim_de_jogo = FONTE.render("Fim de Jogo", True, (255, 255, 255))
            texto_reiniciar = FONTE.render("Pressione espaço para jogar", True, (255, 255, 255))
            tela.blit(texto_fim_de_jogo, (LARGURA_TELA // 2 - texto_fim_de_jogo.get_width() // 2, ALTURA_TELA // 3))
            tela.blit(texto_reiniciar, (LARGURA_TELA // 2 - texto_reiniciar.get_width() // 2, ALTURA_TELA // 2))

        tela.blit(chao, (0, ALTURA_TELA - ALTURA_TELA // 6)) #Atualização do chão

        pygame.display.flip()
        relógio.tick(60)
