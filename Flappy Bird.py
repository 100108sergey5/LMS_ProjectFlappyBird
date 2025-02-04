import pygame
import random
from pygame.locals import *
import os.path

pygame.init()
# SFX
clickfx = pygame.mixer.Sound("jump_3.wav")
HurtFX = pygame.mixer.Sound("Hurt_1.wav")  #
coinfx = pygame.mixer.Sound("pickupCoin1.wav")
deathSFX = pygame.mixer.Sound('explosion.wav')
gameoverTrigger = False
# SFX
pos = ()
clicked = False
height = 400
width = 800
screen = pygame.display.set_mode((width, height))
font = pygame.font.Font("font_1.otf", 50)
# Цвета
black = (23, 22, 25)
blackVariant = (24, 28, 26)
# Цвета

game_score = 0  # Счёт

bird_fly_through = False

flying_through = 60
Tube_create_time = 2000
time_tube = pygame.time.get_ticks() - Tube_create_time
powerUpCreateTime = 19500
powerUpTime = pygame.time.get_ticks() - powerUpCreateTime
game_over = False
flying = False
skins_tab = False

skins_i = 4
skins_j = 7

floor_coordinate = 0
floor_coordinate_new = 3
bg_coordinate = 0
bg_coordinate_new = 0.5

clock = pygame.time.Clock()
FPS = 120
icon = pygame.image.load("Sprite-icon.png")

pygame.display.set_caption("Flappy Bird")
pygame.display.set_icon(icon)

bg = pygame.image.load("Background7.png")
floor = pygame.image.load("Floor1.png")

Game_start_sprite = pygame.image.load('Sprite-start.png')
Game_over_Lose_img = pygame.image.load("Sprite-retry.png")
Game_start_skins_sprite = pygame.image.load("Sprite-skins.png")
Game_start_skins_sprite1 = pygame.image.load('Sprite-standard.png')
Game_start_skins_sprite2 = pygame.image.load('Sprite-special.png')
Game_start_skins_sprite3 = pygame.image.load('Sprite-bigbird.png')
Game_sequence_ghost_powerup = pygame.image.load('Sprite-ghost.png')
rect_button = Rect(300, 200, 200, 50)  # Хитбокс кнопки перезапуска


def draw_text(game_score, font, black, x, y):
    game_score_numbers = font.render(str(game_score), True, black)
    screen.blit(game_score_numbers, (x, y))


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.powerUp = False
        self.index = 0
        self.counter = 0
        for q in range(skins_i, skins_j):
            img = pygame.image.load(f"Sprite-0{q}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.vel = 0
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.clicked = False
        self.animation_again = 25
        self.stopped_mid_flight = False
        self.game_end_vel = 10

    def update(self):
        # Полёт
        if flying is True and game_over is False:
            if self.vel <= 1:
                self.vel += 0.1
            if self.rect.bottom < 350:
                self.rect.y += int(self.vel)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                self.vel = -4
                pygame.mixer.Sound.play(clickfx)
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            # Анимация
        if game_over is False:
            self.counter += 1
            if self.counter > self.animation_again:
                self.counter = 0
                self.index = self.index + 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -5)
        elif flying is False and game_over is True:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
        if game_over is True:
            self.rect.y -= int(self.game_end_vel)
            self.game_end_vel += -0.5



class Tube(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Sprite-Tube1.png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - flying_through]
        if position == -1:
            self.rect.topleft = [x, y + flying_through]

    def update(self):
        self.rect.x = self.rect.x - floor_coordinate_new
        if self.rect.x == 50:
            pygame.mixer.Sound.play(coinfx)
        if self.rect.x <= -300 or self.rect.x >= 1100:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Sprite-ghost.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.rect.x = self.rect.x - floor_coordinate_new
        if self.rect.x <= -300:
            self.kill()


tube_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
powerUp_group = pygame.sprite.Group()
bird = Bird(60, 180)
bird_group.add(bird)

def draw_game_over():
    global game_over
    game_over = True
    global flying
    flying = False
    font.render("Играть заново?", True, blackVariant)
    screen.blit(Game_over_Lose_img, (300, 180))

rect_start = Rect(300, 100, 200, 100)
rect_skins = Rect(300, 250, 200, 100)

def draw_main_menu():
    screen.blit(Game_start_sprite, (300, 100))
    screen.blit(Game_start_skins_sprite, (300, 250))

rect_skins1 = Rect(100, 100, 150, 200)
rect_skins3 = Rect(500, 100, 150, 200)
rect_skins2 = Rect(300, 100, 150, 200)

def draw_skins_tab():
    screen.blit(Game_start_skins_sprite1, (100, 100))
    screen.blit(Game_start_skins_sprite2, (300, 100))
    screen.blit(Game_start_skins_sprite3, (500, 100))


a = True
while a:

    clock.tick(FPS)
    screen.blit(bg, (bg_coordinate, 0))
    bird_group.draw(screen)
    bird_group.update()
    tube_group.draw(screen)
    powerUp_group.draw(screen)
    screen.blit(floor, (floor_coordinate, 350))

    if len(tube_group) > 0:
        if bird_group.sprites()[0].rect.left > tube_group.sprites()[0].rect.left and bird_fly_through is False and \
                bird_group.sprites()[0].rect.right < tube_group.sprites()[0].rect.right:
            bird_fly_through = True
        if bird_fly_through is True:
            if bird_group.sprites()[0].rect.left > tube_group.sprites()[0].rect.right:
                game_score += 1
                print(game_score)
                bird_fly_through = False
    if pygame.sprite.groupcollide(bird_group, tube_group, False, False) and bird.powerUp is False:
        game_over = True

    if pygame.sprite.groupcollide(bird_group, powerUp_group, False, True):
        bird.powerUp = True
        powerUp_group.empty()
        powerTime = get_ticks

    if flying is True and bird.powerUp is True:
        draw_text(game_score, font, black, 300, 300)
        screen.blit(Game_sequence_ghost_powerup, (400, 300))
        powerUpTime_seconds = (pygame.time.get_ticks() - powerTime) // 1000
        draw_text(10 - powerUpTime_seconds, font, black, 410, 305)
        if 10 - powerUpTime_seconds <= 0:
            bird.powerUp = False
            print('a')
    elif flying is True:
        draw_text(game_score, font, black, 400, 300)

    if skins_tab == True:
        draw_skins_tab()

    if game_over is False:
        floor_coordinate = floor_coordinate - floor_coordinate_new
        if abs(floor_coordinate) >= 275:
            floor_coordinate = 0
        bg_coordinate = bg_coordinate - bg_coordinate_new
        if abs(bg_coordinate) >= 800:
            bg_coordinate = 0
        tube_group.update()
        powerUp_group.update()

    if flying is False and game_over is False and skins_tab != True:
        draw_main_menu()


    if flying is True:
        get_ticks = pygame.time.get_ticks()
        if get_ticks - time_tube >= Tube_create_time:
            tube_height_rng = random.randint(-80, 30)
            tube_bottom = Tube(800, height / 2 + tube_height_rng, 1)
            tube_top = Tube(800, height / 2 + tube_height_rng, -1)
            tube_group.add(tube_bottom)
            tube_group.add(tube_top)
            time_tube = get_ticks
        if get_ticks - powerUpTime >= powerUpCreateTime:
            powerUp_rng = random.randint(50, 300)
            powerUp = PowerUp(1200, powerUp_rng)
            powerUp_group.add(powerUp)
            powerUpTime = pygame.time.get_ticks()

    if bird.rect.bottom >= 350:
        game_over = True

    if bird.rect.top <= 0:
        game_over = True

    if game_over is True:
        draw_game_over()
        if gameoverTrigger == False:
            pygame.mixer.Sound.play(deathSFX)
            gameoverTrigger = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            a = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying is False and game_over is False:
            pos = pygame.mouse.get_pos()
            if rect_start.collidepoint(pos) and skins_tab != True:
                flying = True
            elif rect_skins.collidepoint(pos) and skins_tab != True:
                skins_tab = True
            elif rect_skins1.collidepoint(pos) and skins_tab is True:
                skins_i = 4
                skins_j = 7
                bird_group.empty()
                bird = Bird(60, 180)
                bird_group.add(bird)
                skins_tab = False
                flying = True
            elif rect_skins2.collidepoint(pos) and skins_tab is True:
                with open('score.txt', "r") as f:
                    data = f.read()
                if int(data) >= 200:
                    skins_i = 7
                    skins_j = 10
                    bird_group.empty()
                    bird = Bird(60, 180)
                    bird_group.add(bird)
                    skins_tab = False
                    flying = True
                else:
                    skins_i = 4
                    skins_j = 7
                    bird_group.empty()
                    bird = Bird(60, 180)
                    bird_group.add(bird)
                    skins_tab = False
                    flying = True
            elif rect_skins3.collidepoint(pos) and skins_tab is True:
                with open('score.txt', "r") as f:
                    data = f.read()
                if int(data) >= 1000:
                    skins_i = 1
                    skins_j = 4
                    bird_group.empty()
                    bird = Bird(60, 180)
                    bird_group.add(bird)
                    skins_tab = False
                    flying = True
                else:
                    skins_i = 4
                    skins_j = 7
                    bird_group.empty()
                    bird = Bird(60, 180)
                    bird_group.add(bird)
                    skins_tab = False
                    flying = True
        if event.type == pygame.MOUSEBUTTONDOWN and game_over is True:
            pos = pygame.mouse.get_pos()
            if rect_button.collidepoint(pos):
                game_over = False
                flying = False
                tube_group.empty()
                bird_group.empty()
                powerUp_group.empty()
                bird = Bird(60, 180)
                bird_group.add(bird)
                if os.path.exists('score.txt') and os.path.getsize('score.txt') > 0:
                    with open('score.txt', "r") as f:
                        data = f.read()

                    with open('score.txt', "w") as f:
                        f.write(f'{int(data) + game_score}')
                else:
                    f = open('score.txt', 'w')
                    f.write(f'{game_score}')
                    f.close()
                game_score = 0
                gameoverTrigger = False


    pygame.display.flip()
pygame.quit()
