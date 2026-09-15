import pygame

FPS = 60

pygame.init()
tela = pygame.display.set_mode((800, 450)) 

relogio = pygame.time.Clock()
velocidade = 250
jogador = pygame.Rect(100, 180, 45, 45)
obstaculo = pygame.Rect(420, 130, 100, 170)
area_tela = tela.get_rect()

rodando = True
while rodando:
    dt = relogio.tick(FPS) / 1000

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
        jogador.x += velocidade * dt

    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
        jogador.x -= velocidade * dt

    if teclas[pygame.K_w] or teclas[pygame.K_UP]:
        jogador.y -= velocidade * dt

    if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
        jogador.y += velocidade * dt

    jogador.clamp_ip(area_tela)

    if obstaculo and jogador.colliderect(obstaculo):
        cor_jogador = (255, 90, 90)
        obstaculo = None
    else:
        cor_jogador = (70, 150, 255)

    tela.fill((30, 30, 30))
    pygame.draw.rect(tela, cor_jogador, jogador)

    if obstaculo:
        pygame.draw.rect(tela, (110, 110, 125), obstaculo)

    pygame.display.flip()

pygame.quit()