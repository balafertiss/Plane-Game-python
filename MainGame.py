import random
import pygame
import os

from pygame.locals import(RLEACCEL,K_w,K_s,K_a,K_d,K_ESCAPE,KEYDOWN,QUIT,K_RETURN)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("explosion.mp3")
pygame.mixer.music.set_volume(0.7)

a = 0



class CrPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super(CrPlayer,self).__init__()
        self.surf = pygame.image.load("plane.png").convert_alpha()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(center =(0,500))


    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0,-2)
        if pressed_keys[K_s]:
            self.rect.move_ip(0,2)
        if pressed_keys[K_a]:
            self.rect.move_ip(-2,0)
        if pressed_keys[K_d]:
            self.rect.move_ip(2,0)

        if self.rect.left <0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top <=0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

class CrEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super(CrEnemy, self).__init__()
        self.surf = pygame.image.load("alien.png").convert_alpha()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect(center=(random.randint(screen_width+20,screen_width + 100),random.randint(0,screen_height),))

        self.speed = random.randint(1,4)

    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right <0:
            self.kill()

class CrBlackHoles(pygame.sprite.Sprite):
    def __init__(self):
        super(CrBlackHoles,self).__init__()
        self.surf = pygame.image.load("BlackHole.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.dice = random.randint(0,2)
        if self.dice == 1:
            self.rect = self.surf.get_rect(center=(random.randint(screen_width+20,screen_width + 100),random.randint(0,screen_height - 20)))
        else:
            self.rect = self.surf.get_rect(center=(random.randint(screen_width+20,screen_width + 100),random.randint(0, screen_height + 20)))

        self.speed = random.randint(1, 4)

        if self.dice == 1:
            global a
            a = 1.5
        elif self.dice == 2:
            a = -1.5

    def update(self):
        global a
        self.rect.move_ip(-self.speed, a)
        if self.rect.right < 0: 
            self.kill()

class CrFinish(pygame.sprite.Sprite):
    def __init__(self):
        super(CrFinish,self).__init__()
        self.surf = pygame.image.load("finish.png").convert_alpha()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.x = screen_width + 4000
        self.rect.y =0

        self.speed = 1

    def update(self):
        self.rect.move_ip(-self.speed,0)
        print("test")


AddEnemy = pygame.USEREVENT + 1
pygame.time.set_timer(AddEnemy,800)

AddBlackHole = pygame.USEREVENT + 2
pygame.time.set_timer(AddBlackHole,10000)

screen_width = 1920
screen_height = 1080


screen = pygame.display.set_mode((screen_width,screen_height))

bg = pygame.image.load("bg.png")

Player = CrPlayer()
Finish = CrFinish()


all_S = pygame.sprite.Group()
all_S.add(Player)
all_S.add(Finish)
GrFinish = pygame.sprite.Group()
GrFinish.add(Finish)
enemies = pygame.sprite.Group()
BlackHoles = pygame.sprite.Group()
run = True

h3 = pygame.image.load("3hearts.png").convert_alpha()
l = 3
flag1 = 1

while run:

    pressed_keys = pygame.key.get_pressed()


    if pressed_keys[pygame.K_ESCAPE]:
        run = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        elif event.type == AddEnemy:
            Enemy = CrEnemy()
            enemies.add(Enemy)
            all_S.add(Enemy)

        elif event.type == AddBlackHole:
            BlackHole = CrBlackHoles()
            BlackHoles.add(BlackHole)
            all_S.add(BlackHole)

    if flag1 == 1:

        screen.blit(bg, (0, 0))

        Player.update(pressed_keys)

        enemies.update()
        BlackHoles.update()
        GrFinish.update()

        Fpos = Finish.rect.x
        Ppos = Player.rect.x

        Distance = Fpos - Ppos


        text = pygame.font.SysFont("cosmicsansms", 50, True, True)
        txt = text.render("Finish line:"+ str(Distance), True, (255, 255, 255))
        screen.blit(txt, (0,0))


        for entity in all_S:
            screen.blit(entity.surf, entity.rect)

        if pygame.sprite.spritecollideany(Player,enemies):
            en = pygame.sprite.spritecollideany(Player,enemies)
            en.kill()
            l = l-1
            pygame.mixer.music.play()


        if pygame.sprite.spritecollideany(Player,BlackHoles):
            bl = pygame.sprite.spritecollideany(Player,BlackHoles)
            bl.kill()
            l = l - 1
            pygame.mixer.music.play()

        if pygame.sprite.spritecollideany(Player,GrFinish):
            flag1 = 2

        if l == 3:
            h3 = pygame.image.load("3hearts.png").convert_alpha()
            h3.set_colorkey((255, 255, 255), RLEACCEL)
            screen.blit(h3,(1650,-70))
        elif l == 2:
            h3 = pygame.image.load("2hearts.png").convert_alpha()
            h3.set_colorkey((255, 255, 255), RLEACCEL)
            screen.blit(h3, (1683, -46))
        elif l == 1:
            h3 = pygame.image.load("1hearts.png").convert_alpha()
            h3.set_colorkey((255, 255, 255), RLEACCEL)
            screen.blit(h3, (1683, -46))

        elif l == 0:
            flag1 = 0
    elif flag1 == 2:
        if pressed_keys[pygame.K_RETURN]:

            for s in all_S:
                s.kill()
            for e in enemies:
                e.kill()
            for b in BlackHoles:
                b.kill()
            for h in GrFinish:
                h.kill()
            all_S.add(Player)
            all_S.add(Finish)
            GrFinish.add(Finish)
            Finish.rect.x = screen_width + 4000
            Player.rect.x = 0
            Player.rect.y = 500
            l = 3
            flag1 = 1
        else:
            text = pygame.font.SysFont("cosmicsansms", 50, True, True)
            txt = text.render("You won!!! press enter to play again", True, (255, 255, 255))
            screen.blit(txt, (600, 400))

    else:

        if pressed_keys[pygame.K_RETURN]:

            for s in all_S:
                s.kill()
            for e in enemies:
                e.kill()
            for b in BlackHoles:
                b.kill()
            for h in GrFinish:
                h.kill()
            all_S.add(Player)
            all_S.add(Finish)
            GrFinish.add(Finish)

            Finish.rect.x = screen_width + 4000
            Player.rect.x = 0
            Player.rect.y = 500
            l = 3
            flag1 = 1
        else:
            screen.fill((0,0,0))
            text = pygame.font.SysFont("cosmicsansms", 50, True, True)
            txt = text.render("Game Over press enter to play again", True, (255, 255, 255))
            screen.blit(txt, (600, 400))




    pygame.display.flip()

