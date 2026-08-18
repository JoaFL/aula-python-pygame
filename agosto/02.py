import pygame
import random
import math

LARGURA = 1200
ALTURA = 600

AZUL_ESCURO = (20, 35, 70)
ROXO = (160, 32, 240)
VEREMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
CIANO = (0, 255, 255)
BRANCO = (255, 255, 255)
COR_ALEATORIA = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def quadrado():
    pygame.draw.circle(tela, VEREMELHO, (100, 100), 10)
    pygame.draw.circle(tela, VEREMELHO, (150, 100), 10)
    pygame.draw.circle(tela, VEREMELHO, (200, 100), 10)
    pygame.draw.circle(tela, VEREMELHO, (250, 100), 10)
    pygame.draw.circle(tela, VEREMELHO, (300, 100), 10)
    
    pygame.draw.circle(tela, VEREMELHO, (100, 150), 10)
    pygame.draw.circle(tela, VEREMELHO, (100, 200), 10)
    pygame.draw.circle(tela, VEREMELHO, (100, 250), 10)
    
    pygame.draw.circle(tela, VEREMELHO, (300, 150), 10)
    pygame.draw.circle(tela, VEREMELHO, (300, 200), 10)
    pygame.draw.circle(tela, VEREMELHO, (300, 250), 10)
    
    pygame.draw.circle(tela, VEREMELHO, (100, 300), 10)
    pygame.draw.circle(tela, VEREMELHO, (150, 300), 10)
    pygame.draw.circle(tela, VEREMELHO, (200, 300), 10)
    pygame.draw.circle(tela, VEREMELHO, (250, 300), 10)
    pygame.draw.circle(tela, VEREMELHO, (300, 300), 10)


def losangulo():
    pygame.draw.circle(tela, VERDE, (650, 100), 10)
    pygame.draw.circle(tela, VERDE, (600, 150), 10)
    pygame.draw.circle(tela, VERDE, (550, 200), 10)
    pygame.draw.circle(tela, VERDE, (500, 250), 10)
    
    pygame.draw.circle(tela, VERDE, (700, 150), 10)
    pygame.draw.circle(tela, VERDE, (750, 200), 10)
    
    pygame.draw.circle(tela, VERDE, (600, 350), 10)
    pygame.draw.circle(tela, VERDE, (550, 300), 10)
    
        
    pygame.draw.circle(tela, VERDE, (650, 400), 10)
    pygame.draw.circle(tela, VERDE, (700, 350), 10)
    pygame.draw.circle(tela, VERDE, (750, 300), 10)
    pygame.draw.circle(tela, VERDE, (800, 250), 10)
    
def circulo():
    # tive que usar matemática

    posX = 1000
    posY = 300

    for i in range(10):
       angulo = (i / 10) * math.pi * 2
       x = posX + math.cos(angulo) * 100
       y = posY + math.sin(angulo) * 100

       pygame.draw.circle(tela, AMARELO, (x, y), 10)

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Coordenadas e cores")

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
    tela.fill(AZUL_ESCURO)
    
    pygame.draw.circle(tela, VEREMELHO, (0, 0), 10)
    pygame.draw.circle(tela, VEREMELHO, (LARGURA // 2, ALTURA // 2), 8)
    
    quadrado()
    losangulo()
    circulo()

    pygame.display.flip()

pygame.quit()