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

class Bird:
    SPRITES=BIRD_SPRITES
    MAX_ROTATION=25
    ROTATION_SPEED=20
    ANIMATION_SPEED=5

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.angle=0
        self.speed=0
        self.height=self.y
        self.time=0
        self.sprite_count=0
        self.sprite=self.SPRITES[0]

    def jump(self):
        self.speed=-10.5
        self.time=0
        self.height=self.y
    
    def move(self):
        self.time+=1
        movement=1.5*(self.time**2)+self.speed*self.time

        if movement>16:
            movement=16
        elif movement <0:
            movement-=2

        self.y+=movement

        if movement<0 or self.y<(self.height+50):
            if self.angle<self.MAX_ROTATION:
                self.angle=self.MAX_ROTATION
        else:
            if self.angle>-90:
                self.angle-=self.ROTATION_SPEED

    def draw(self,screen):
        self.sprite_count+=1

        if self.sprite_count<self.ANIMATION_SPEED:
            self.sprite=self.SPRITES[0]
        elif self.sprite_count>self.ANIMATION_SPEED*2:
            self.sprite=self.SPRITES[1]
        elif self.sprite_count>self.ANIMATION_SPEED*3:
            self.sprite=self.SPRITES[2]
        elif self.sprite_count>self.ANIMATION_SPEED*4:
            self.sprite=self.SPRITES[1]
        elif self.sprite_count>self.ANIMATION_SPEED*4+1:
            self.sprite=self.SPRITES[0]
            self.sprite_count=0

        if self.angle<=-80:
            self.sprite=self.SPRITES[1]
            self.sprite_count=self.ANIMATION_SPEED*2

        rotated_sprite=pygame.transform.rotate(self.sprite,self.angle)
        sprite_center=self.sprite.get_rect(topleft=(self.x,self.y))
        rectangle=rotated_sprite.get_rect(center=sprite_center)
        screen.blit(rotated_sprite,rectangle.topleft)

    def get_mask(self):
        pygame.mask.from_surface(self.sprite)
