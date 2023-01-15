import os
import sys
import pygame
import random


class Tile(pygame.sprite.Sprite):
    spisok = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        Tile.spisok[pos_y][pos_x] = [pos_y, pos_x]

    def update(self):
        pos_x = Tile.spisok[self.y][self.x][1]
        pos_y = Tile.spisok[self.y][self.x][0]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def test(lst):
    o = lst[-1:]+lst[:-1]
    return o


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.cords = [pos_y, pos_x] #сначала у, потом x
        self.rect.x = tile_width * pos_x + 15
        self.rect.y = tile_height * pos_y + 5
        self.y_up = False

    def update(self):
        for i in range(len(Tile.spisok)):
            Tile.spisok[i] = test(Tile.spisok[i])

    def jump(self):
        self.cords = [self.cords[0] - 1, self.cords[1]]
        self.rect = self.image.get_rect().move(
            tile_width * self.cords[1], tile_height * self.cords[0])
        if self.cords[0] == 0:
            self.y_up = False

    def fall(self):
        if self.cords[0] != 4:
           self.cords = [self.cords[0] + 1, self.cords[1]]
           self.rect = self.image.get_rect().move(tile_width * self.cords[1], tile_height * self.cords[0])


def load_image(name, colorkey=None):
    fullname = name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def generate(map):
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == 'empty':
                Tile('empty', x, y)
            elif map[y][x] == 'wall':
                Tile('wall', x, y)
            elif map[y][x] == 'player':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player


def proverka(velikieschitovodi):
    running = True
    if player.y_up:
        player.jump()
    else:
        player.fall()
    if velikieschitovodi[0][1] != 0:
        velikieschitovodi[0][1] -= 1
        velikieschitovodi[1][1] -= 1
    else:
        velikieschitovodi[0][1] = 11
        velikieschitovodi[1][1] = 11
    if velikieschitovodi[2][1] != 0:
        velikieschitovodi[2][1] -= 1
    else:
        velikieschitovodi[2][1] == 11
    if velikieschitovodi[0] == player.cords or velikieschitovodi[1] == player.cords or velikieschitovodi[2] == player.cords:
        running = False
    return running


def start_screen():
    fon = pygame.transform.scale(load_image('fon.png'), (1200, 500))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(50)


def end_screen():
    fon = pygame.transform.scale(load_image('fon.png'), (1200, 500))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(50)


def terminate():
    pygame.quit()
    sys.exit()






if __name__ == '__main__':
    pygame.init()
    size = width, height = 1200, 500
    screen = pygame.display.set_mode(size)
    FPS = 8
    clock = pygame.time.Clock()
    tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
    player_image = load_image('mario.png')
    tile_width = tile_height = 50
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    map = [['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
           ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
           ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
           ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'wall', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'wall', 'empty'],
           ['empty', 'empty', 'player', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'wall', 'wall', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'wall', 'empty'],
           ['wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall'],
           ['wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall'],
           ['wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall'],
           ['wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall'],
           ['wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall']]
    maps_size = (10, 12)
    player = generate(map)
    start_screen()
    running = True
    velikieschitovodi = [[3, 10], [4, 10], [4, 11]]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    player.y_up = True
        running = proverka(velikieschitovodi)
        player.update()
        tiles_group.update()
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
    pygame.init()
    size = width, height = 1200, 500
    screen = pygame.display.set_mode(size)
    end_screen()