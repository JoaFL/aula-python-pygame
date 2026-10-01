import pygame
import random

pygame.init()

tela = pygame.display.set_mode((800, 450))
pygame.display.set_caption("Jogo do Alvo")

rodando = True
pontos = 0

alvo = pygame.Rect(300, 180, 60, 60)

# Fontes
fonte = pygame.font.Font(None, 24)
fonte_titulo = pygame.font.Font(None, 64)

while rodando:

    # +---------+
    # | EVENTOS |
    # +---------+

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

            if alvo.collidepoint(evento.pos):
                pontos += 1

                alvo.x = random.randint(0, 740)
                alvo.y = random.randint(0, 390)

    # +---------+
    # | CENÁRIO |
    # +---------+

    tela.fill((30, 30, 30))

    pygame.draw.rect(tela, (255, 110, 90), alvo)

    # +-----------+
    # | INTERFACE |
    # +-----------+

    # Placar
    texto_pontos = fonte.render(
        f"Pontos: {pontos}",
        True,
        (255, 255, 255)
    )

    tela.blit(texto_pontos, (15, 15))

    # Título
    titulo = fonte_titulo.render(
        "CAÇA AO QUADRADO",
        True,
        (80, 170, 255)
    )

    rect_titulo = titulo.get_rect(center=(400, 55))

    tela.blit(titulo, rect_titulo)

    # Instrução
    instrucoes = fonte.render(
        "Clique no quadrado para ganhar pontos!",
        True,
        (200, 200, 200)
    )

    tela.blit(instrucoes, (15, 410))

    if pontos >= 5 and pontos < 10:
        mensagem = fonte.render(
            "PARABÉNS! VOCÊ CHEGOU A 5 PONTOS! - Chegue a 10 pontos",
            True,
            (255, 220, 80)
        )

        rect_mensagem = mensagem.get_rect(center=(400, 100))

        tela.blit(mensagem, rect_mensagem)

    # Mensagem ao chegar em 10 pontos
    if pontos >= 10:

        mensagem = fonte.render(
            "PARABÉNS! VOCÊ CHEGOU A 10 PONTOS! - Chegue a 15 pontos para finalizar",
            True,
            (255, 220, 80)
        )

        rect_mensagem = mensagem.get_rect(center=(400, 100))

        tela.blit(mensagem, rect_mensagem)
        
    if pontos >= 15:
        rodando = False

    # Atualiza a tela
    pygame.display.flip()

pygame.quit()