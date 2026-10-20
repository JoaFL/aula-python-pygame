import pygame
#nota
# Iniciar o Pygame
pygame.init()

# -----------------------------
# CONSTANTES
# -----------------------------

LARGURA = 800
ALTURA = 500
FPS = 60
COR_FUNDO = (10, 15, 35)
COR_NAVE = (80, 220, 255)
COR_NAVE2 = (255, 80, 80)
VELOCIDADE_NAVE = 6

# -----------------------------
# CRIAR A JANELA
# -----------------------------

tela = pygame.display.set_mode(
    (LARGURA, ALTURA)
)

pygame.display.set_caption("Spaceships")

relogio = pygame.time.Clock()

# Fonte das mensagens
fonte = pygame.font.Font(None, 30)

# -----------------------------
# CRIAR A NAVE
# -----------------------------

nave1 = pygame.Rect(
    380,
    ALTURA - 50,
    40,
    40
)

nave2 = pygame.Rect(
    380, 10, 40, 40
)

# -----------------------------
# LOOP PRINCIPAL
# -----------------------------

rodando = True

while rodando:

    relogio.tick(FPS)

    # Verificar eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

    # -------------------------
    # MOVIMENTO
    # -------------------------

    teclas = pygame.key.get_pressed()

    # Esquerda
    if teclas[pygame.K_LEFT]:
        nave1.x -= VELOCIDADE_NAVE

    # Direita
    if teclas[pygame.K_RIGHT]:
        nave1.x += VELOCIDADE_NAVE
        
    # Esquerda
    if teclas[pygame.K_a]:
        nave2.x -= VELOCIDADE_NAVE
    
    # Direita
    if teclas[pygame.K_d]:
        nave2.x += VELOCIDADE_NAVE

    # -------------------------
    # LIMITES DA TELA
    # -------------------------

    nave1.x = max(
        0,
        min(nave1.x, LARGURA - nave1.width)
    )
    nave2.x = max(
       0,
        min(nave2.x, LARGURA - nave2.width)
    )

    # -------------------------
    # VERIFICAR AS BORDAS
    # -------------------------

    mensagem = ""
    if nave1.left == 0:
        mensagem = "Limite esquerdo!"
    elif nave1.right == LARGURA:
        mensagem = "Limite direito!"
        
    mensagem2 = ""
    if nave2.left == 0:
        mensagem2 = "Limite esquerdo!"
    elif nave2.right == LARGURA:
        mensagem2 = "Limite direito!"

    # -------------------------
    # DESENHAR
    # -------------------------

    tela.fill(COR_FUNDO)

    # Desenhar a nave
    pygame.draw.polygon(
        tela,
        COR_NAVE,
        [
            (nave1.centerx, nave1.top),
            (nave1.left, nave1.bottom),
            (nave1.right, nave1.bottom)
        ]
    )
    
    pygame.draw.polygon(
        tela,
        COR_NAVE2,
        [
           (nave2.centerx, nave2.bottom),
            (nave2.left, nave2.top),
           (nave2.right, nave2.top)
        ]
    )

    # Mostrar mensagem na tela
    if mensagem != "":
        texto = fonte.render(
            mensagem,
            True,
            COR_NAVE
        )
        tela.blit(texto, (20, 20))
        
    if mensagem2 != "":
        texto = fonte.render(
            mensagem2,
            True,
            COR_NAVE2
        )
        tela.blit(texto, (LARGURA - 170, ALTURA - 50))

    # Atualizar a janela
    pygame.display.flip()

# Encerrar o Pygame
pygame.quit()