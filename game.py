import pygame
import os
import random

SCREEN_WIDTH=500
SCREEN_HEIGHT=800

PIPE_SPRITE=pygame.transform.scale2x(pygame.image.load(os.path.join('sprites','pipe.png')))
GROUND_SPRITE=pygame.transform.scale2x(pygame.image.load(os.path.join('sprites','base.png')))
BG_SPRITE=pygame.transform.scale2x(pygame.image.load(os.path.join('sprites','bg.png')))
BIRD_SPRITES=[
    pygame.transform.scale2x(pygame.image.load(os.path.join('sprites','bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('sprites','bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('sprites','bird3.png'))),
]
pygame.font.init()
FONT=pygame.font.SysFont('arial',50)