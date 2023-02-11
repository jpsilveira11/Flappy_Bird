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
        sprite_center=self.sprite.get_rect(topleft=(self.x,self.y)).center
        rectangle=rotated_sprite.get_rect(center=sprite_center)
        screen.blit(rotated_sprite,rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.sprite)

class Pipe:
    DISTANCE=200
    SPEED=5

    def __init__(self,x):
        self.x=x
        self.height=0
        self.top=0
        self.base=0
        self.TOP_PIPE=pygame.transform.flip(PIPE_SPRITE,False,True)
        self.BASE_PIPE=PIPE_SPRITE
        self.passed=False
        self.def_height()

    def def_height(self):
        self.height=random.randrange(50,450)
        self.top=self.height-self.TOP_PIPE.get_height()
        self.base=self.height+self.DISTANCE

    def move(self):
        self.x-=self.SPEED

    def draw(self,screen):
        screen.blit(self.TOP_PIPE,(self.x,self.top))
        screen.blit(self.BASE_PIPE,(self.x,self.base))

    def colide(self,bird):
        bird_mask=bird.get_mask()
        top_pipe_mask=pygame.mask.from_surface(self.TOP_PIPE)
        base_pipe_mask=pygame.mask.from_surface(self.BASE_PIPE)

        top_distance=(self.x-bird.x,self.top-round(bird.y))
        base_distance=(self.x-bird.x,self.base-round(bird.y))

        top_point=bird_mask.overlap(top_pipe_mask,top_distance)
        base_point=bird_mask.overlap(base_pipe_mask,base_distance)
        
        if base_point or top_point:
            return True
        else:
            return False

class Ground:
    SPEED=5
    WIDTH=GROUND_SPRITE.get_width()
    SPRITE=GROUND_SPRITE

    def __init__(self,y):
        self.y=y
        self.x0=0
        self.x1=self.WIDTH

    def move(self):
        self.x0-=self.SPEED
        self.x1-=self.SPEED

        if self.x0+self.WIDTH<0:
            self.x0=self.x1+self.WIDTH
        if self.x1+self.WIDTH<0:
            self.x1=self.x0+self.WIDTH

    def draw(self,screen):
        screen.blit(self.SPRITE,(self.x0,self.y))
        screen.blit(self.SPRITE,(self.x1,self.y))

def draw_screen(screen,birds,pipes,ground,score):
    screen.blit(BG_SPRITE,(0,0))
    for bird in birds:
        bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)
    
    text=FONT.render(f'Score: {score}',1,(255,255,255))
    screen.blit(text,(SCREEN_WIDTH-10-text.get_width(),10))
    ground.draw(screen)
    pygame.display.update()

def main():
    birds=[Bird(230,350)]
    ground=Ground(730)
    pipes=[Pipe(700)]
    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    score=0
    clock=pygame.time.Clock()

    running=True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()

        for bird in birds:
            bird.move()
        ground.move()
        
        add_pipe=False
        remove_pipes=[]
    
        for pipe in pipes:
            for counter, bird in enumerate(birds):
                if pipe.colide(bird):
                    birds.pop(counter)
                if not pipe.passed and bird.x>pipe.x:
                    pipe.passed=True
                    add_pipe=True
            pipe.move()
            if pipe.x+pipe.TOP_PIPE.get_width()<0:
                remove_pipes.append(pipe)

        if add_pipe:
            score+=1
            pipes.append(Pipe(600))
        for pipe in remove_pipes:
            pipes.remove(pipe)

        for counter,bird in enumerate(birds):
            if(bird.y+bird.sprite.get_height())>ground.y or bird.y<0:
                birds.pop(counter)

        draw_screen(screen,birds,pipes,ground,score)
        
if __name__ == '__main__':
    main()   


