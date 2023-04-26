import os
import sys
import pygame
from random import choice

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


def load_image(name):
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


def obstacles():
    velikieschitovodi = []
    for i in range(len(spisochek)):
        if "@" in spisochek[i]:
            sp = [i]
            for j in range(len(spisochek[i])):
                if spisochek[i][j] == "&":
                    sp.append(j)
                    velikieschitovodi.append(sp)
                    sp = [i]
            sp = [i - 1]
            for j in range(len(spisochek[i - 1])):
                if spisochek[i - 1][j] == "&":
                    sp.append(j)
                    velikieschitovodi.append(sp)
                    sp = [i - 1]
            sp = [i - 2]
            for j in range(len(spisochek[i - 2])):
                if spisochek[i - 2][j] == "&":
                    sp.append(j)
                    velikieschitovodi.append(sp)
                    sp = [i - 2]
    return velikieschitovodi


def proverka(velikieschitovodi):
    running = True
    if player.y_up:
        player.jump()
    else:
        player.fall()
    for i in range(len(velikieschitovodi)):
        if velikieschitovodi[i][1] != 0:
            velikieschitovodi[i][1] -= 1
        else:
            velikieschitovodi[i][1] = 23
    for j in velikieschitovodi:
        if j == [player.cords[0], player.cords[1] + 1]:
            running = False
            break
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
    string_rendered = font.render(intro_text, 1, pygame.Color(0, 118, 118))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 50
    intro_rect.x = 1025
    pygame.draw.rect(screen, (0, 118, 118), (1015, 40, 160, 40), 1)
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


def counted(smg):
    smg += 1
    return smg


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
    map_names = ['map.txt', 'map1.txt', 'map2.txt', 'map3.txt']
    spisochek = load_level(choice(map_names))
    velikieschitovodi = obstacles()
    player = generate(spisochek)
    sound = pygame.mixer.Sound('data\jump.wav')
    count = 0
    v = 0
    k = 100
    start_screen()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    if player.cords == player.nachalo:
                        player.y_up = True
                    sound.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.cords == player.nachalo:
                    player.y_up = True
                    sound.play()
        running = proverka(velikieschitovodi)
        player.update()
        tiles_group.update()
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        count = counted(count)
        if count // k > v:
            FPS += 1
            k *= 2
        font = pygame.font.Font(None, 30)
        string_rendered = font.render(f'Your points: {count}', 1, pygame.Color(0, 118, 118))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 50
        intro_rect.x = 1000
        screen.blit(string_rendered, intro_rect)
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] > 537) and (event.pos[0] < 697) and (event.pos[1] > 435) and (event.pos[1] < 475):
                    os.execl(sys.executable, sys.executable, *sys.argv)
        all_sprites.update()
        all_sprites.draw(screen)
        if game_over.rect.x == 0:
            font = pygame.font.Font(None, 30)
            string_rendered = font.render(f'Your points: {count}', 1, pygame.Color(0, 118, 118))
            end_rect = string_rendered.get_rect()
            end_rect.top = 395
            end_rect.x = 550
            screen.blit(string_rendered, end_rect)
            end_text = "Играть снова"
            string_rendered = font.render(end_text, 1, pygame.Color(0, 118, 118))
            restart = string_rendered.get_rect()
            restart.top = 445
            restart.x = 550
            pygame.draw.rect(screen, (0, 118, 118), (537, 435, 160, 40), 1)
            screen.blit(string_rendered, restart)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
