import pygame

SW = 700
SH = 400

a = False
w = False
s = False

pygame.init()
tela = pygame.display.set_mode((SW, SH))
cor_fundo = (25, 25, 35)

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
                cor_fundo = (255, 0, 255)
                
            if evento.key == pygame.K_a:
                a = not a
                
            if evento.key == pygame.K_w:
                w = not w
                
            if evento.key == pygame.K_s:
                s = not s
                            
    if a:
        pygame.draw.circle(tela, (255, 0, 0), (SW // 2, SH // 2), 10)
    if w:
        pygame.draw.circle(tela, (255, 0, 0), (1, SH // 2), 10)
    if s:
        pygame.draw.circle(tela, (255, 0, 0), (SW // 2, 1), 10)
                
    pygame.display.flip()
    
pygame.quit()