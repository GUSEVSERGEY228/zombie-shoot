import os
import sys
from random import choice, randint
from time import sleep

import pygame

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 60
WIDTH = 1000
HEIGHT = 1000
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
STEP = 1

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()
cursor_group = pygame.sprite.Group()
shoot_group = pygame.sprite.Group()
ammo_group = pygame.sprite.Group()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y, zombies = None, None, None, []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('box', x, y)
            elif level[y][x] == 'b':
                Tile('brick', x, y)
            elif level[y][x] == 'w':
                Tile('woodwall', x, y)
            elif level[y][x] == 'f':
                Tile('woodbg', x, y)
            elif level[y][x] == 'p':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'z':
                Tile('empty', x, y)
                cur_zombie = Zombie(x, y)
                zombies.append(cur_zombie)
    return new_player, zombies, x, y


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


tile_images = {
    'woodwall': load_image('woodwall.png'),
    'woodbg': load_image('woodbg.png'),
    'brick': load_image('brick.png'),
    'box': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('character1.png', color_key='white')
zombie_image = load_image('zombie.png', color_key='white')
shoot_image = load_image('shoot.png', color_key='black')
vzriv_image = load_image('vzriv.png', color_key='white')
ammo_image = load_image('ammo.png', color_key='white')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'brick':
            wall_group.add(self)
        if tile_type == 'woodwall':
            wall_group.add(self)
        if tile_type == 'box':
            wall_group.add(self)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def go(self, direction):
        if direction == 'up':
            self.image = load_image('character.png', color_key='white')
            player.rect.y -= STEP
            if pygame.sprite.spritecollideany(self, wall_group):
                player.rect.y += STEP
        if direction == 'down':
            self.image = load_image('character2.png', color_key='white')
            player.rect.y += STEP
            if pygame.sprite.spritecollideany(self, wall_group):
                player.rect.y -= STEP
        if direction == 'left':
            self.image = load_image('character3.png', color_key='white')
            player.rect.x -= STEP
            if pygame.sprite.spritecollideany(self, wall_group):
                player.rect.x += STEP
        if direction == 'right':
            self.image = load_image('character1.png', color_key='white')
            player.rect.x += STEP
            if pygame.sprite.spritecollideany(self, wall_group):
                player.rect.x -= STEP

    def shoot(self, coords1, coords2):
        global shooted
        shooted = [delay, True, True]
        shoot.rect.topleft = coords1
        vzriv.rect.topleft = coords2


class Zombie(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(zombie_group, all_sprites)
        self.image = zombie_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.direction = 'up'

    def go(self, direction):
        step = randint(0, 10)
        if direction:
            self.direction = direction
        if self.direction == 'up':
            self.image = load_image('zombie.png', color_key='white')
            zombies[i].rect.y -= step
            if pygame.sprite.spritecollideany(self, wall_group):
                zombies[i].rect.y += step
        if self.direction == 'down':
            self.image = load_image('zombie2.png', color_key='white')
            zombies[i].rect.y += step
            if pygame.sprite.spritecollideany(self, wall_group):
                zombies[i].rect.y -= step
        if self.direction == 'left':
            self.image = load_image('zombie3.png', color_key='white')
            zombies[i].rect.x -= step
            if pygame.sprite.spritecollideany(self, wall_group):
                zombies[i].rect.x += step
        if self.direction == 'right':
            self.image = load_image('zombie1.png', color_key='white')
            zombies[i].rect.x += step
            if pygame.sprite.spritecollideany(self, wall_group):
                zombies[i].rect.x -= step


def start_screen():
    intro_text = ["нажмите на мышку, чтобы начать ОСТОРОЖНО СКРИМЕРЫ"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


start_screen()
player, zombies, level_x, level_y = generate_level(load_level('map.txt'))
running = True
camera = Camera()
pygame.key.set_repeat(6)
directions = ('up', 'right', 'down', 'left')
delay = 0
direct = choice(directions)
screemers = ('screemer.jpg', 'screemer2.jpg', 'screemer3.jpg')
kriks = ('data/krik.mp3', 'data/krik2.mp3', 'data/krik3.mp3')
cursor = pygame.sprite.Sprite()
cursor.image = load_image("cursor.png", color_key='white')
cursor.rect = cursor.image.get_rect()
all_sprites.add(cursor)
cursor_group.add(cursor)
pygame.mouse.set_visible(False)
shooted = [delay, False, False]
shoot = pygame.sprite.Sprite()
shoot.image = shoot_image
shoot.rect = shoot.image.get_rect()
all_sprites.add(shoot)
shoot_group.add(shoot)
vzriv = pygame.sprite.Sprite()
vzriv.image = vzriv_image
vzriv.rect = vzriv.image.get_rect()
all_sprites.add(vzriv)
shoot_group.add(vzriv)
kill_zombie = None
admin_mode = False
reloral_time = 150

while running:
    delay += 1  # эта переменная нужна для "искусственного интелекта" зомби и для выстрела
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.go('left')
            if event.key == pygame.K_d:
                player.go('right')
            if event.key == pygame.K_w:
                player.go('up')
            if event.key == pygame.K_s:
                player.go('down')
            if event.key == pygame.K_COMMA:
                if admin_mode:
                    STEP = 1
                    admin_mode = False
                    reloral_time = 250
                else:
                    STEP = 10
                    admin_mode = True
                    reloral_time = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if shooted[2]:
                if delay - shooted[0] >= reloral_time:
                    player.shoot(player.rect[:2], pygame.mouse.get_pos())
            else:
                player.shoot(player.rect[:2], pygame.mouse.get_pos())
        cursor.rect.topleft = pygame.mouse.get_pos()
    if shooted[1]:
        if delay - shooted[0] == 30:
            shooted[1] = False

    for i in range(len(zombies)):
        if pygame.sprite.spritecollideany(zombies[i], shoot_group):
            kill_zombie = i + 1
        if delay % randint(20, 200) == 0:
            direct = choice(directions)
            zombies[i].go(direct)
        else:
            zombies[i].go(None)
    if kill_zombie:
        all_sprites.remove(zombies[kill_zombie - 1])
        zombie_group.remove(zombies[kill_zombie - 1])
        del zombies[kill_zombie - 1]
        kill_zombie = None
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill('black')
    tiles_group.draw(screen)
    ammo_group.draw(screen)
    zombie_group.draw(screen)
    if shooted[1]:
        shoot_group.draw(screen)
    player_group.draw(screen)
    cursor_group.draw(screen)
    clock.tick(FPS)
    if pygame.sprite.spritecollideany(player, zombie_group):
        imgname = choice(screemers)
        zvukname = choice(kriks)
        fon = pygame.transform.scale(load_image(imgname), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        pygame.mixer.music.load(zvukname)
        pygame.mixer.music.play()
        pygame.display.flip()
        sleep(1)

    pygame.display.flip()
pygame.quit()
