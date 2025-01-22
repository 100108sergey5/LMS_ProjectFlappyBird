import pygame
import random
from pygame.locals import *

pygame.init()
# SFX
clickfx = pygame.mixer.Sound("jump_3.wav")
HurtFX = pygame.mixer.Sound("Hurt_1.wav")  #
coinfx = pygame.mixer.Sound("pickupCoin1.wav")
# SFX
pos = ()
clicked = False
height = 400
width = 800
screen = pygame.display.set_mode((width, height))
font = pygame.font.Font("font_1.otf", 50)
# Цвета
black = (23, 22, 25)
purple = (123, 20, 232)
blue = (22, 25, 204)
cyan = (65, 242, 228)
blackVariant = (24, 28, 26)
# Цвета

game_score = 0  # Счёт

bird_fly_through = False

rect_button = Rect(50, 170, 200, 50)
flying_through = 60
Tube_create_time = 2000
time_tube = pygame.time.get_ticks() - Tube_create_time
game_over = False
flying = False

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
# Птица

Game_over_retry_img = pygame.image.load("Button_Retry.png")  # Кнопка перезапуска
Game_over_Lose_img = pygame.image.load("Button_Lose.png")  # Кнопка проигрыша
rect_button = Rect(300, 200, 200, 50)  # Хитбокс кнопки перезапуска


def draw_text(game_score, font, black, x, y):
    game_score_numbers = font.render(str(game_score), True, black)
    screen.blit(game_score_numbers, (x, y))


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for q in range(4, 7):
            img = pygame.image.load(f"Sprite-0{q}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.vel = 0
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.clicked = False
        self.animation_again = 25
        self.stopped_mid_flight = False

    def update(self):
        # Полёт
        if flying is True and game_over is False:
            if self.vel <= 1:
                self.vel += 0.1
            if self.rect.bottom < 350:
                self.rect.y += int(self.vel)
        if game_over is False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                self.vel = -4
                pygame.mixer.Sound.play(clickfx)
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            # Анимация
            self.counter += 1
            if self.counter > self.animation_again:
                self.counter = 0
                self.index = self.index + 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -5)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
        if game_over is True:
            if self.rect.y > 140:
                self.rect.y = 280
            elif self.rect.y < 280:
                self.rect.y += 3


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


tube_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
bird = Bird(60, 180)
bird_group.add(bird)


def draw_game_over():
    global game_over
    game_over = True
    global flying
    flying = False
    font.render("Играть заново?", True, blackVariant)
    pygame.draw.rect(screen, cyan, rect_button)
    screen.blit(Game_over_Lose_img, (250, 180))


a = True
while a:

    clock.tick(FPS)
    screen.blit(bg, (bg_coordinate, 0))
    bird_group.draw(screen)
    bird_group.update()
    tube_group.draw(screen)
    # tube_group.update()
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
    if pygame.sprite.groupcollide(bird_group, tube_group, False, False):
        game_over = True

    draw_text(game_score, font, black, 400, 300)

    if game_over is False:
        floor_coordinate = floor_coordinate - floor_coordinate_new
        if abs(floor_coordinate) >= 275:
            floor_coordinate = 0
        bg_coordinate = bg_coordinate - bg_coordinate_new
        if abs(bg_coordinate) >= 800:
            bg_coordinate = 0
        tube_group.update()

    if flying is True:
        get_ticks = pygame.time.get_ticks()
        if get_ticks - time_tube >= Tube_create_time:
            tube_height_rng = random.randint(-80, 30)
            tube_bottom = Tube(800, height / 2 + tube_height_rng, 1)
            tube_top = Tube(800, height / 2 + tube_height_rng, -1)
            tube_group.add(tube_bottom)
            tube_group.add(tube_top)
            time_tube = get_ticks

    if bird.rect.bottom >= 350:
        game_over = True

    if game_over is True:
        draw_game_over()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            a = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying is False and game_over is False:
            flying = True
        if event.type == pygame.MOUSEBUTTONDOWN and game_over is True:
            pos = pygame.mouse.get_pos()
            if rect_button.collidepoint(pos):
                game_over = False
                tube_group.empty()
                bird_group.empty()
                bird = Bird(60, 180)
                bird_group.add(bird)
                game_score = 0
                flying = False
    pygame.display.flip()
pygame.quit()
