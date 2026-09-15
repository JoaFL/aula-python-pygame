import pygame

SW = 800
SH = 600
FPS = 60

clock = pygame.time.Clock()
tela = pygame.display.set_mode((SW, SH))
pygame.init()

running = True
while running:
    dt = clock.tick(FPS) / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    