import pygame

pygame.init()
tela = pygame.display.set_mode((700, 400))
cor_fundo = (25, 25, 35)

rodando = True
while rodando:
    for evento in pygame.event.get():
        print(evento)
        
        if evento.type == pygame.QUIT:
            rodando = False
            
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False
                
            if evento.key == pygame.K_SPACE:
                cor_fundo = (60, 30, 90)
                
    tela.fill(cor_fundo)
    pygame.display.flip()
    
pygame.quit()