import pygame

pygame.init()
tela = pygame.display.set_mode((800, 450))

quadrado = {
    "x": 280,
    "y": 205,
    "velocidade": 0.5,
    "tamanho": 40,
    "cor": (60, 150, 255)
}
circulo = {
    "x": 300,
    "y": 205,
    "velocidade": 0.6,
    "tamanho": 20,
    "cor": (60, 150, 0)
}

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
    teclas = pygame.key.get_pressed()
    
    if teclas[pygame.K_a]:
        quadrado["x"] -= quadrado["velocidade"]
        
    if teclas[pygame.K_d]:
       quadrado["x"] += quadrado["velocidade"]
        
    if teclas[pygame.K_w]:
        quadrado["y"] -= quadrado["velocidade"]
        
    if teclas[pygame.K_s]:
        quadrado["y"] += quadrado["velocidade"]
        
    #-------------------------------------------------------
        
    if teclas[pygame.K_LEFT]:
        circulo["x"] -= circulo["velocidade"]
            
    if teclas[pygame.K_RIGHT]:
       circulo["x"] += circulo["velocidade"]
        
    if teclas[pygame.K_UP]:
        circulo["y"] -= circulo["velocidade"]
        
    if teclas[pygame.K_DOWN]:
        circulo["y"] += circulo["velocidade"]
        
    tela.fill((25, 25, 40))
    
    pygame.draw.rect(
        tela, 
        quadrado["cor"],
        (
            quadrado["x"],
            quadrado["y"],
            quadrado["tamanho"],
            quadrado["tamanho"]
        )
    )
    pygame.draw.circle(
        tela,
        circulo["cor"],
        (
            circulo["x"],
            circulo["y"]),
            circulo["tamanho"]
        )
    
    pygame.display.flip()
    
pygame.quit()