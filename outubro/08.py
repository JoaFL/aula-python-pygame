# SPACESHIPS - AULA 20
# Versao cumulativa: inclui tudo o que foi trabalhado ate esta aula.
# Execute: python aula_20.py
import pygame
import random

pygame.init()
# 1. CONFIGURACOES
LARGURA, ALTURA = 800, 500
FPS = 60
COR_FUNDO = (10, 15, 35)
COR_NAVE = (80, 220, 255)
COR_TEXTO = (255, 255, 255)
COR_TIRO = (255, 230, 100)
VELOCIDADE_NAVE = 6

# 9. PREPARAR A JANELA E OBJETOS
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("SPACESHIPS - aulas cumulativas")
relogio = pygame.time.Clock()
fonte = pygame.font.Font(None, 30)
fonte_grande = pygame.font.Font(None, 55)
nave = pygame.Rect(380, 425, 40, 40)

objeto_massa = pygame.Rect(LARGURA // 2 - 150, 20, 300, 30)
cor_objeto = (255, 255, 255)

tiros = []
# 10. LOOP PRINCIPAL
rodando = True
while rodando:
    relogio.tick(FPS)
    # EVENTOS: so aqui lemos KEYDOWN
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                tiro = pygame.Rect(nave.centerx - 3, nave.top, 6, 16)
                tiros.append(tiro)

    # ATUALIZAR O JOGO
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        nave.x -= VELOCIDADE_NAVE
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        nave.x += VELOCIDADE_NAVE
    nave.x = max(0, min(nave.x, LARGURA - nave.width))
    for tiro in tiros:
        tiro.y -= 9

    # DESENHAR: limpar a tela antes de redesenhar os objetos
    tela.fill(COR_FUNDO)
    pygame.draw.polygon(tela, COR_NAVE, [
        (nave.centerx, nave.top),
        (nave.left, nave.bottom),
        (nave.right, nave.bottom)
    ])
    for tiro in tiros:
        if objeto_massa and tiro.colliderect(objeto_massa):
            cor_objeto = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
            tiros.remove(tiro)
        
        if tiro:    
            pygame.draw.rect(tela, COR_TIRO, tiro)
        
    if objeto_massa:
        pygame.draw.rect(tela, cor_objeto, objeto_massa)
    
    mensagem = ""
    if nave.left == 0:
        mensagem = "Limite esquerdo!"
    elif nave.right == LARGURA:
        mensagem = "Limite direito!"
    if mensagem:
        texto = fonte.render(mensagem, True, COR_TEXTO)
        tela.blit(texto, (20, 465))
    
    pygame.display.flip()
pygame.quit()