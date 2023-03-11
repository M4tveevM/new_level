import sys

import pygame
from pygame.sprite import Sprite

from settings import size, load_image, tile_width, tile_height, width, height

pygame.init()
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
FPS = 60

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.flipped = False
        self.image = player_image
        self.pos = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.control = {
            'w': (0, -tile_height),
            'a': (-tile_width, 0),
            's': (0, tile_height),
            'd': (tile_width, 0)
        }

    def move(self, movement):
        if movement in self.control:
            if not self.flipped and movement == 'd':
                self.flipped = True
                self.image = pygame.transform.flip(self.image, True, False)
            elif self.flipped and movement == 'a':
                self.flipped = False
                self.image = pygame.transform.flip(self.image, True, False)
            dx, dy = self.control[movement]
            self.rect.x += dx
            self.rect.y += dy

    def in_borders(self, dx, dy):
        x, y = self.pos
        return


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


# основной персонаж
player = None
camera = Camera()
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    bg = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(bg, (0, 0))
    screen.fill('paleturquoise')
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('slategray'))
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


player, level_x, level_y = generate_level(load_level('map.txt'))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            player.move(event.unicode)
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
