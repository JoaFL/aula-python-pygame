import pygame
import random
import math

cor_fundo = (25, 25, 35)
sol = True

SW = 700
SH = 400

chuva = False
agua = 330
estrelas = []

pygame.init()
tela = pygame.display.set_mode((SW, SH))


for i in range(1000):
    cor = 255 - max(0, min(i *5, 255))
    estrelas.append([tela, (cor, cor, cor), (random.randint(0, SW), random.randint(0, SH)), random.randint(1, 3)])

rodando = True
while rodando:
    tela.fill(cor_fundo)
    
    for evento in pygame.event.get():
        #print(evento)
        
        if evento.type == pygame.QUIT:
            rodando = False
            
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False
                
            if evento.key == pygame.K_SPACE:
                sol = not sol
            
            if evento.key == pygame.K_c:
                chuva = not chuva
            
    
    if sol:
        pygame.draw.circle(tela, (255, 255, 0), (0, 0), 100)
        pygame.draw.circle(tela, (255, 165, 0), (0, 0), 110, 25)
        cor_fundo = (173, 216, 230)
        
    
    else:
        for i in estrelas:
            pygame.draw.circle(i[0], i[1], i[2], i[3])
            
        pygame.draw.circle(tela, (200, 200, 200), (SW, 0), 75)
        pygame.draw.circle(tela, (255, 255, 255), (SW, 0), 80, 10)
        cor_fundo = (0, 0, 0)
        
    if chuva:
        for i in range(10):
            pos = random.randint(1, 700)
            curva = 50
            agua -= 0.001
            pygame.draw.line(tela, (0, 0, 255), (pos + curva, 0), (pos - curva, 400), 5)
    
    pygame.draw.rect(tela, (60, 180, 90), (0, 330, 800, 120))
    pygame.draw.rect(tela, (70, 130, 255), (360, 260, 80, 60))
    pygame.draw.circle(tela, (255, 230, 200), (400, 245), 28)
    pygame.draw.line(tela, (20, 20, 20), (375, 245), (390, 245), 4)
    pygame.draw.line(tela, (20, 20, 20), (410, 245), (425, 245), 4)
    
    pontos = [(0, 330), (SW, 330), (SW, agua), (0, agua)] 
    pygame.draw.polygon(tela, (0, 0, 255), pontos, 0)
    
    agua += 0.001
    
    pygame.display.flip()
pygame.quit()