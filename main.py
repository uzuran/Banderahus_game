import pygame 
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT
import random
from os import listdir


pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 800, 600

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0


font = pygame.font.SysFont("Verdana", 20)

main_surface = pygame.display.set_mode(screen)
bg = pygame.transform.scale(pygame.image.load("background.png").convert(), screen)
bgx = 0
bgx2 = bg.get_width()
bg_speed = 3


# ball = pygame.Surface((20, 20))
# ball.fill(white)
img_path = "gus"

player_imgs = [pygame.image.load(img_path + "/" + file).convert_alpha() for file in listdir(img_path)]
player = player_imgs[0]
player_rect = player.get_rect()
player_speed = 5


CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)


def create_bonus():
    bonus = pygame.image.load("bonus.png").convert_alpha()
    bonus = pygame.transform.scale(bonus, (120, 150))
    bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())
    bonus_speed = random.randint(4, 6)
    return [bonus, bonus_rect, bonus_speed]


CREATE_BONUSES = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUSES, 3000)


def create_enemy():
    enemy = pygame.image.load("enemy.png").convert_alpha()
    enemy = pygame.transform.scale(enemy, (70, 30))
    enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())
    enemy_speed = random.randint(4, 6)
    return [enemy, enemy_rect, enemy_speed]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

is_working = True
img_index = 0
bonuses = []
enemies = []
scores = 0

while is_working:
    FPS.tick(80)
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUSES:
            bonuses.append(create_bonus())

        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]

    bgx -= bg_speed
    bgx2 -= bg_speed

    if bgx < - bg.get_width():
        bgx = bg.get_width()
    
    if bgx2 < - bg.get_width():
        bgx2 = bg.get_width()

    main_surface.blit(bg, (bgx, 0))
    main_surface.blit(bg, (bgx2, 0))
    main_surface.blit(player, player_rect)
    main_surface.blit(font.render(str(scores), True, green), (width - 30, 0))

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])
        
        if bonus[1].bottom > height:
            bonuses.pop(bonuses.index(bonus))
        
        if bonus[1].right > width:
            bonuses.pop(bonuses.index(bonus))
        
        if bonus[1].left < 0:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    for enemy in enemies:
        enemy[1] = enemy[1].move(- enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
        # TEST
        if enemy[1].bottom > height:
            enemies.pop(enemies.index(enemy))
        if enemy[1].top > height:
            enemies.pop(enemies.index(enemy))
        
        if player_rect.colliderect(enemy[1]):
            is_working = False
    # Pressed keys

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move(0, player_speed)

    if pressed_keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(0, - player_speed)

    if pressed_keys[K_RIGHT] and not player_rect.right > width:
        player_rect = player_rect.move(player_speed, 0)

    if pressed_keys[K_LEFT] and not player_rect.left < 0:
        player_rect = player_rect.move(- player_speed, 0)

    pygame.display.flip()
