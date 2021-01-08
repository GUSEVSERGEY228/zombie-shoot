import os
import sys
from random import choice

import pygame

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 60
WIDTH = 1000
HEIGHT = 1000
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
STEP = 1
ZSTEP = 4

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()


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
                Tile('wall', x, y)
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
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('character1.png', color_key='white')
zombie_image = load_image('zombie.png', color_key='white')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'wall':
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


class Zombie(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(zombie_group, all_sprites)
        self.image = zombie_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.direction = 'up'

    def go(self, direction):
        if direction:
            self.direction = direction
        if self.direction == 'up':
            self.image = load_image('zombie.png', color_key='white')
            i.rect.y -= ZSTEP
            if pygame.sprite.spritecollideany(self, wall_group):
                i.rect.y += ZSTEP
        if self.direction == 'down':
            self.image = load_image('zombie2.png', color_key='white')
            i.rect.y += ZSTEP
            if pygame.sprite.spritecollideany(self, wall_group):
                i.rect.y -= ZSTEP
        if self.direction == 'left':
            self.image = load_image('zombie3.png', color_key='white')
            i.rect.x -= ZSTEP
            if pygame.sprite.spritecollideany(self, wall_group):
                i.rect.x += ZSTEP
        if self.direction == 'right':
            self.image = load_image('zombie1.png', color_key='white')
            i.rect.x += ZSTEP
            if pygame.sprite.spritecollideany(self, wall_group):
                i.rect.x -= ZSTEP


def start_screen():
    intro_text = ["нажмите на мышку, чтобы начать"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 33)
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
zombie_dir = 0
direct = choice(directions)

while running:
    zombie_dir += 1  # эта переменная нужна для "искусственного интелекта" зомби
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
    for i in zombies:
        if zombie_dir % 100 == 0:
            direct = choice(directions)
            i.go(direct)
        else:
            i.go(None)
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill('black')
    tiles_group.draw(screen)
    player_group.draw(screen)
    zombie_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
