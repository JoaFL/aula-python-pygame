import pygame

cor_fundo = (25, 25, 35)
sol = True

SW = 700
SH = 400

pygame.init()
tela = pygame.display.set_mode((SW, SH))

rodando = True
while rodando:
    tela.fill(cor_fundo)
    
    for evento in pygame.event.get():
        print(evento)
        
        if evento.type == pygame.QUIT:
            rodando = False
            
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False
                
            if evento.key == pygame.K_SPACE:
                sol = not sol
    
    if sol:
        pygame.draw.circle(tela, (255, 255, 0), (0, 0), 100)
        pygame.draw.circle(tela, (255, 165, 0), (0, 0), 110, 25)
        cor_fundo = (173, 216, 230)
    else:
        pygame.draw.circle(tela, (200, 200, 200), (SW, 0), 75)
        pygame.draw.circle(tela, (255, 255, 255), (SW, 0), 80, 10)
        cor_fundo = (0, 0, 0)
    
    
    pygame.draw.rect(tela, (60, 180, 90), (0, 330, 800, 120))
    pygame.draw.rect(tela, (70, 130, 255), (360, 260, 80, 60))
    pygame.draw.circle(tela, (255, 230, 200), (400, 245), 28)
    pygame.draw.line(tela, (20, 20, 20), (375, 245), (390, 245), 4)
    pygame.draw.line(tela, (20, 20, 20), (410, 245), (425, 245), 4)
    
    pygame.display.flip()
pygame.quit()