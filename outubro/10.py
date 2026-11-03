# SPACESHIPS - AULA 22
# Versao cumulativa: inclui tudo o que foi trabalhado ate esta aula.
# Execute: python aula_22.py
import pygame

pygame.init()
# 1. CONFIGURACOES
LARGURA, ALTURA = 800, 500
FPS = 60
COR_FUNDO = (10, 15, 35)
COR_NAVE = (80, 220, 255)
COR_TEXTO = (255, 255, 255)
COR_TIRO = (255, 230, 100)
VELOCIDADE_NAVE = 6
ROXO = (188, 100, 247)
ROXO_ESCURO = (188 - 50, 100 - 50, 247 - 50)
VERDE = (105, 250, 206)

# 2. MATRIZ DE PIXEL ART (0=vazio, 1=corpo, 2=olhos)
DESENHO_1 = [
    "0001100011000",
    "0011111111100",
    "0111111111110",
    "1122111112211",
    "1111111111111",
    "1111111111111",
    "0011111111100",
    "0011011101100",
    "0110000000110",
    "1100000000011",
    "1000000000001",
]

ARTE = [
    "000033333330000",
    "000033333330000",
    "000033333330000",
    "000033333330000",
    "000033333330000",
    "333333333333333",
    "000111111111000",
    "001222222222100",
    "012211222112210",
    "012122121221210",
    "012123121321210",
    "012211222112210",
    "012222222222210",
    "012212222212210",
    "012221111122210",
    "012222111222210",
    "001222222222100",
    "000111111111000",
    "000000111000000",
    "000001111100000",
    "000011010110000",
    "000110010011000",
    "001100010001100",
    "011000010000110",
    "110000010000011",
    "000000111000000",
    "000001111100000",
    "000011000110000",
    "000110000011000",
    "000110000011000",
    "000110000011000",
    "001110000011100",
    "001100000001100",
]

# 9. PREPARAR A JANELA E OBJETOS
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("SPACESHIPS - aulas cumulativas")
relogio = pygame.time.Clock()
fonte = pygame.font.Font(None, 30)
fonte_grande = pygame.font.Font(None, 55)
nave = pygame.Rect(380, 425, 40, 40)
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
    for tiro in tiros[:]:
        tiro.y -= 9
        if tiro.bottom < 0:
            tiros.remove(tiro)

    # DESENHAR: limpar a tela antes de redesenhar os objetos
    tela.fill(COR_FUNDO)
    pygame.draw.polygon(tela, COR_NAVE, [
        (nave.centerx, nave.top),
        (nave.left, nave.bottom),
        (nave.right, nave.bottom)
    ])
    # Nesta aula desenhamos diretamente os quadradinhos (preview).
    for linha, texto in enumerate(DESENHO_1):
        for coluna, simbolo in enumerate(texto):
            if simbolo != "0":
                cor = VERDE if simbolo == "2" else ROXO
                pygame.draw.rect(tela, cor, (
                    380 + coluna * 3, 90 + linha * 3, 3, 3
                ))
                
    for linha, texto in enumerate(ARTE):
        for coluna, simbolo in enumerate(texto):
            if simbolo != "0":
                cor = ROXO_ESCURO
                if simbolo == "2":
                    cor = COR_TEXTO
                elif simbolo == "3":
                    cor = VERDE
                pygame.draw.rect(tela, cor, (
                    100 + coluna * 3, 90 + linha * 3, 3, 3
                ))
    for tiro in tiros:
        pygame.draw.rect(tela, COR_TIRO, tiro)
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