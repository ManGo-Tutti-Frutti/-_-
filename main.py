import os
import sys
import pygame

WIDTH, HEIGHT = 1250, 500


class Tile(pygame.sprite.Sprite):
    spisok = [[0 for j in range(WIDTH // 50)] for i in range(HEIGHT // 50)]

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


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = tile_width * pos_x + 15
        self.rect.y = tile_height * pos_y + 5
        self.nachalo = tile_height * pos_y + 5

    def update(self):
        for i in range(len(Tile.spisok)):
            Tile.spisok[i] = Tile.spisok[i][-1:] + Tile.spisok[i][:-1]

    def jump(self):
        if self.rect.y == self.nachalo:
            self.FPS = 15
            self.rect.y -= 100
            player.update()
            tiles_group.update()
            screen.fill((0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)
            clock.tick(self.FPS)
            self.rect.y += 100
            player.update()
            tiles_group.update()
            screen.fill((0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)
            clock.tick(self.FPS)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate(map):
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == '.':
                Tile('empty', x, y)
            elif map[y][x] == '#':
                Tile('wall', x, y)
            elif map[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player


if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT = 1000, 500
    screen = pygame.display.set_mode(size)
    FPS = 15
    clock = pygame.time.Clock()
    tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
    player_image = load_image('mar.png')
    tile_width = tile_height = 50
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    maps_size = (10, 12)
    player = generate(load_level('map.txt'))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    player.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.jump()
        player.update()
        tiles_group.update()
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()