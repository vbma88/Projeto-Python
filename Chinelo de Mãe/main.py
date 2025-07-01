import pygame
import random
import sys

# === INICIALIZAÇÃO ===
pygame.init()
pygame.mixer.init()

# TELA
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Chinelo da Mãe")

# CORES
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

# ASSETS
img_mae = pygame.image.load("img/mae.png")
img_filho = pygame.image.load("img/filho.png")
img_chinelo = pygame.image.load("img/chinelo.png")

som_atira = pygame.mixer.Sound("som/atira.wav")
som_acerto = pygame.mixer.Sound("som/acerto.wav")

# FONTES
fonte = pygame.font.SysFont(None, 36)

# CLASSES
class Mae(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(img_mae, (70, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 300  # mesma linha do filho
        self.vel_x = 2

    def update(self):
        self.rect.x += self.vel_x
        if self.rect.right > LARGURA or self.rect.left < 0:
            self.vel_x *= -1  # inverte a direção


class Chinelo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(img_chinelo, (40, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = 10

    def update(self):
        self.rect.x += self.vel
        if self.rect.left > LARGURA:
            self.kill()

class Filho(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(img_filho, (60, 90))
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA - 100
        self.rect.y = 300  # mesma linha da mãe
        self.vel_x = -3
        self.vidas = 3

    def update(self):
        self.rect.x += self.vel_x
        if self.rect.right < 0:
            self.rect.x = LARGURA + 50  # volta pro final da tela
            self.vidas -= 1

       

    def resetar(self):
        self.rect.x = random.randint(LARGURA + 20, LARGURA + 100)
        self.rect.y = random.randint(100, ALTURA - 100)
        self.vel_x = random.randint(3, 6)


# TELAS
def tela_inicio():
    tela.fill(BRANCO)
    titulo = fonte.render("CHINELO DA MÃE", True, PRETO)
    instrucoes = fonte.render("Pressione qualquer tecla para jogar", True, PRETO)
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 200))
    tela.blit(instrucoes, (LARGURA // 2 - instrucoes.get_width() // 2, 300))
    pygame.display.flip()
    esperar_tecla()

def tela_fim(msg):
    tela.fill(BRANCO)
    texto = fonte.render(msg, True, PRETO)
    tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 300))
    pygame.display.flip()
    pygame.time.wait(3000)

def esperar_tecla():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                return

# INÍCIO
tela_inicio()

# GRUPOS
grupo_todos = pygame.sprite.Group()
grupo_chinelos = pygame.sprite.Group()

mae = Mae()
filho = Filho()

grupo_todos.add(mae)
grupo_todos.add(filho)

# LOOP
pontuacao = 0
rodando = True
clock = pygame.time.Clock()

while rodando:
    clock.tick(60)
    tela.fill(BRANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            chinelo = Chinelo(mae.rect.right, mae.rect.centery)
            grupo_todos.add(chinelo)
            grupo_chinelos.add(chinelo)
            som_atira.play()

    keys = pygame.key.get_pressed()
    mae.update(keys)
    grupo_chinelos.update()
    filho.update()

        # atualiza os personagens
    mae.update()
    filho.update()

    if filho.vidas <= 0:
        tela_fim("O filho escapou demais! Fim de jogo.")
        rodando = False

    # desenhar os elementos
    tela.blit(img_fundo, (0, 0))
    grupo_todos.draw(tela)

    pygame.display.flip()
    relogio.tick(60)


    # Colisão
    if pygame.sprite.spritecollide(filho, grupo_chinelos, True):
        filho.vidas -= 1
        som_acerto.play()
        filho.rect.center = (700, random.randint(100, 500))

    # Fim de jogo
    if filho.vidas <= 0:
        tela_fim("Você acertou o filho! Vitória da mãe!")
        rodando = False

    # Desenho
    grupo_todos.draw(tela)

    # Vidas
    pygame.draw.rect(tela, VERMELHO, (650, 20, 100, 20))
    pygame.draw.rect(tela, VERDE, (650, 20, 100 * (filho.vidas / 3), 20))

    vidas_txt = fonte.render(f"Filho: {filho.vidas} vidas", True, PRETO)
    tela.blit(vidas_txt, (650, 45))

    pygame.display.flip()

pygame.quit()
sys.exit()

