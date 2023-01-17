import os
import sys
import pygame

WIDTH, HEIGHT = 1200, 500


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
        self.cords = [pos_y, pos_x]
        self.nachalo = self.cords[:]
        self.rect.x = tile_width * pos_x
        self.rect.y = tile_height * pos_y
        self.y_up = False

    def update(self):
        for i in range(len(Tile.spisok)):
            Tile.spisok[i] = Tile.spisok[i][-1:] + Tile.spisok[i][:-1]

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


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def generate(map):
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == '.':
                Tile('empty', x, y)
            elif map[y][x] == '&':
                Tile('ice', x, y)
            elif map[y][x] == '+':
                Tile('snow', x, y)
            elif map[y][x] == '#':
                Tile('wall', x, y)
            elif map[y][x] == '@':
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
        velikieschitovodi[2][1] = 11
    if velikieschitovodi[0] == player.cords or velikieschitovodi[1] == player.cords or velikieschitovodi[2] == player.cords:
        running = False
    return running


def rule():
    file_path = r'data/rules.txt'
    os.system("start " + file_path)
    return False


def start_screen():
    intro_text = "Правила игры"
    fon = pygame.transform.scale(load_image('fon.png'), (1200, 500))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    string_rendered = font.render(intro_text, 1, pygame.Color('blue'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 1025
    pygame.draw.rect(screen, (0, 0, 255), (1015, 40, 160, 40), 1)
    screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] > 1015) and (event.pos[0] < 1175) and (event.pos[1] > 40) and (event.pos[1] < 80):
                    rule()
                else:
                    return
        pygame.display.flip()
        clock.tick(50)


class Game_over(pygame.sprite.Sprite):
    def __init__(self, image, *group):
        super().__init__(*group)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = -1200
        self.rect.y = 0

    def update(self):
        x = self.rect.x
        if x < 0:
            self.rect.x += 15


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1200, 500
    screen = pygame.display.set_mode(size)
    FPS = 8
    clock = pygame.time.Clock()
    tile_images = {'wall': load_image('box.png'), 'empty': load_image('empty.png'), 'ice': load_image('ice.png'),
                   'snow': load_image('snow.png')}
    player_image = load_image('hero.png')
    tile_width = tile_height = 50
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player = generate(load_level('map.txt'))
    start_screen()
    running = True
    velikieschitovodi = [[3, 9], [4, 9], [4, 10]]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    if player.cords == player.nachalo:
                        player.y_up = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.cords == player.nachalo:
                    player.y_up = True
        running = proverka(velikieschitovodi)
        player.update()
        tiles_group.update()
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    game_over = Game_over('data\gameover.png', all_sprites)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
