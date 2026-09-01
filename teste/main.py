import pygame

SW = 800
SH = 600
SW2 = SW // 2
SH2 = SH // 2

pygame.init()
screen = pygame.display.set_mode((SW, SH))

update = True
while update:
    for event in pygame.event.get():
        if event.type == event.