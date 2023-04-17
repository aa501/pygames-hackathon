import csv
import os
import random
import sys

import pygame
from pygame import mixer

import button

mixer.init()
pygame.init()
player_name = ""
width = 1300
height = 640
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
# pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# width, height = pygame.display.get_surface().get_size()
# screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Soldier\'s Odyssey')

clock = pygame.time.Clock()
fps = 60

name = ""
gravity = 0.75
scroll_th = 200
rows = 16
columns = 150
# tile_size = height // rows + 2
tile_types = 21
tile_size = 32
maximum_levels = 3
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False
score = 0

moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

jump_fx = pygame.mixer.Sound('assets/audio/jump.wav')
jump_fx.set_volume(0.5)
shot_fx = pygame.mixer.Sound('assets/audio/shot.wav')
shot_fx.set_volume(0.5)
grenade_fx = pygame.mixer.Sound('assets/audio/grenade.wav')
grenade_fx.set_volume(0.5)
game_end_fx = pygame.mixer.Sound('assets/audio/end.wav')
game_end_fx.set_volume(0.9)

start_img = pygame.image.load('assets/img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('assets/img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('assets/img/restart_btn.png').convert_alpha()
pine1_img = pygame.image.load('assets/img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('assets/img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('assets/img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('assets/img/Background/sky_cloud.png').convert_alpha()

img_list = []

for x in range(tile_types):
    img = pygame.image.load(f'assets/img/Tile/{x}.png')
    img = pygame.transform.scale(img, (tile_size, tile_size))
    img_list.append(img)
bullet_img = pygame.image.load('assets/img/icons/bullet.png').convert_alpha()
grenade_img = pygame.image.load('assets/img/icons/grenade.png').convert_alpha()
health_box_img = pygame.image.load('assets/img/icons/health_box.png').convert_alpha()
cartridge_box_image = pygame.image.load('assets/img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('assets/img/icons/grenade_box.png').convert_alpha()
item_boxes = {
    'Health': health_box_img,
    'Cartridge': cartridge_box_image,
    'Grenade': grenade_box_img,
    'keys': 'a: Fire Bullet'
}

background = (144, 201, 120)
red = (255, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
black = (0, 0, 0)
pink = (235, 65, 54)

font = pygame.font.SysFont('Futura', 30)


def update_score(self):
    self.score += 1


def get_player_name(screen):
    global player_name
    input_box = pygame.Rect(screen.get_width() // 2 - 150, screen.get_height() // 2 - 25, 300, 50)  # create input box rect
    font = pygame.font.Font(None, 32)
    player_name = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return player_name
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
        name_surface = font.render(player_name, True, (0, 0, 0))
        screen.blit(name_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def level_completed():
    # update_level()
    global player_name
    # global level
    # level += 1
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))

    font = pygame.font.Font(None, 50)
    text = font.render(f"Congratulations {player_name}! Level Completed!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    overlay.blit(text, text_rect)

    blast = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.circle(blast, (255, 255, 255, 128), (width // 2, height // 2), 100)

    screen.blit(overlay, (0, 0))
    screen.blit(blast, (0, 0))
    pygame.display.flip()

    pygame.time.wait(5000)


def draw_bg():
    screen.fill(background)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, height - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, height - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, height - pine2_img.get_height()))


def reset_level():

    # clearning all game groups
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    # level += 1

    # new empty data grid
    data = []
    for row in range(rows):
        r = [-1] * columns
        data.append(r)

    # for i in range(5):
    #     x = random.randint(0, columns - 1)
    #     y = random.randint(0, rows - 1)
    #     ItemBox((x * tile_size, y * tile_size), random.choice(['health', 'grenade']))
    #
    # for i in range(3):
    #     x = random.randint(0, columns - 1)
    #     y = random.randint(0, rows - 1)
    #     Soldier((x * tile_size, y * tile_size + 25), random.choice(['soldier', 'robot']))
    #
    # for i in range(10):
    #     x = random.randint(0, columns - 1)
    #     y = random.randint(0, rows - 1)
    #     Decoration((x * tile_size, y * tile_size), random.choice(['tree', 'rock', 'bush']))

    return data


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.score = 0
        self.cartridge = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.velocity_y = 0
        self.jump = False
        self.in_air = True
        # self.level = level
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0
        # update_score(self)

        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'assets/img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'assets/img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        scroll_screen = 0
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump and not self.in_air:
            self.velocity_y = -11
            self.jump = False
            self.in_air = True

        self.velocity_y += gravity
        if self.velocity_y > 10:
            self.velocity_y
        dy += self.velocity_y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.velocity_y < 0:
                    self.velocity_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.velocity_y >= 0:
                    self.velocity_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        complete_level = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            complete_level = True

        if self.rect.bottom > height:
            self.health = 0

        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > width:
                dx = 0

        self.rect.x += dx
        self.rect.y += dy

        if self.char_type == 'player':
            if (self.rect.right > width - scroll_th and bg_scroll <
                (world.level_length * tile_size) - width) \
                    or (self.rect.left < scroll_th and bg_scroll > abs(dx)):
                self.rect.x -= dx
                scroll_screen = -dx

        return scroll_screen, complete_level

    def shoot(self):
        if self.shoot_cooldown == 0 and self.cartridge > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery,
                            self.direction)
            bullet_group.add(bullet)
            self.cartridge -= 1
            shot_fx.play()
            update_score(self)

    def ai(self):
        if self.alive and player.alive:
            if not self.idling and random.randint(1, 200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50
            if self.vision.colliderect(player.rect):
                self.update_action(0)
                self.shoot()
            else:
                if not self.idling:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > tile_size:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        self.rect.x += screen_scroll

    def update_animation(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class World:
    def __init__(self):
        self.level_length = None
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * tile_size
                    img_rect.y = y * tile_size
                    tile_data = (img, img_rect)
                    if 0 <= tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif 9 <= tile <= 10:
                        water = Water(img, x * tile_size, y * tile_size)
                        water_group.add(water)
                    elif 11 <= tile <= 14:
                        decoration = Decoration(img, x * tile_size, y * tile_size)
                        decoration_group.add(decoration)
                    elif tile == 15:
                        player = Soldier('player', x * tile_size, y * tile_size, 1.65, 5, 20, 5)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 16:
                        enemy = Soldier('enemy', x * tile_size, y * tile_size, 1.65, 2, 20, 0)
                        enemy_group.add(enemy)
                    elif tile == 17:
                        item_box = ItemBox('Cartridge', x * tile_size, y * tile_size)
                        item_box_group.add(item_box)
                    elif tile == 18:
                        item_box = ItemBox('Grenade', x * tile_size, y * tile_size)
                        item_box_group.add(item_box)
                    elif tile == 19:
                        item_box = ItemBox('Health', x * tile_size, y * tile_size)
                        item_box_group.add(item_box)
                    elif tile == 20:
                        exit = Exit(img, x * tile_size, y * tile_size)
                        exit_group.add(exit)

        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Cartridge':
                player.cartridge += 15
            elif self.item_type == 'Grenade':
                player.grenades += 3
            self.kill()


class HealthBar:
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, black, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, blue, (self.x, self.y, 150 * ratio, 20))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed) + screen_scroll
        if self.rect.right < 0 or self.rect.left > width:
            self.kill()
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.velocity_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self):
        self.velocity_y += gravity
        dx = self.direction * self.speed
        dy = self.velocity_y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                if self.velocity_y < 0:
                    self.velocity_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.velocity_y >= 0:
                    self.velocity_y = 0
                    dy = tile[1].top - self.rect.bottom

        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            grenade_fx.play()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            if abs(self.rect.centerx - player.rect.centerx) < tile_size * 2 and \
                    abs(self.rect.centery - player.rect.centery) < tile_size * 2:
                player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < tile_size * 2 and \
                        abs(self.rect.centery - enemy.rect.centery) < tile_size * 2:
                    enemy.health -= 50


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f'assets/img/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.x += screen_scroll
        explosion_speed = 4
        self.counter += 1
        if self.counter >= explosion_speed:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]


class ScreenFade:
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, width // 2, height))
            pygame.draw.rect(screen, self.colour,
                             (width // 2 + self.fade_counter, 0, width, height))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, width, height // 2))
            pygame.draw.rect(screen, self.colour,
                             (0, height // 2 + self.fade_counter, width, height))
        if self.direction == 2:
            pygame.draw.rect(screen, self.colour, (0, 0, width, 0 + self.fade_counter))
        if self.fade_counter >= width:
            fade_complete = True
        return fade_complete


intro_fade = ScreenFade(1, black, 4)
death_fade = ScreenFade(2, red, 4)

start_btn = button.Button(width // 2 - 130, height // 2 - 150, start_img, 1)
exit_btn = button.Button(width // 2 - 110, height // 2 + 50, exit_img, 1)
restart_btn = button.Button(width // 2 - 110, height // 2 - 50, restart_img, 2)

enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

world_data = []
for row in range(rows):
    r = [-1] * columns
    world_data.append(r)

with open(f'assets/csv/level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data)

score_text = font.render(f"LEVEL: {player.score}", True, (255, 255, 255))
score_rect = score_text.get_rect(center=(width // 2, 50))
level_text = font.render(f"LEVEL: {level}", True, (255, 255, 255))
level_rect = level_text.get_rect(center=(width // 2, 60))

run = True
while run:
    clock.tick(fps)
    if not start_game:
        screen.fill((0,255,0))
        if start_btn.draw(screen):
            start_game = True
            start_intro = True
            get_player_name(screen)
        if exit_btn.draw(screen):
            run = False
    else:
        draw_bg()
        world.draw()
        health_bar.draw(player.health)
        draw_text('REFILLS: ', font, white, 10, 35)
        for x in range(player.cartridge):
            screen.blit(bullet_img, (90 + (x * 10), 40))
        draw_text('GRENADES: ', font, white, 10, 60)
        for x in range(player.grenades):
            screen.blit(grenade_img, (135 + (x * 15), 60))
        score_text = font.render(f"SCORE: {player.score}", True, (255, 255, 255))
        screen.blit(score_text, score_rect)

        level_text = font.render(f"LEVEL: {level}", True, (255, 255, 255))
        level_rect = level_text.get_rect(center=(width // 2, 70))
        screen.blit(level_text, level_rect)
        level_text = font.render(f"Player: {player_name} || Up: Jump | A: Grenade | <-: Move Left | -> Move Right | Spacebar: Fire", True, (255, 255, 255))
        level_rect = level_text.get_rect(center=(900, 20))
        screen.blit(level_text, level_rect)

        player.update()
        player.draw()
        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()
        bullet_group.update()
        grenade_group.update()
        explosion_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

        if start_intro:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        if player.alive:
            if shoot:
                player.shoot()
            elif grenade and not grenade_thrown and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), \
                                  player.rect.top, player.direction)
                grenade_group.add(grenade)
                player.grenades -= 1
                grenade_thrown = True
            if player.in_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1)
            else:
                player.update_action(0)
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            if level_complete:
                level_completed()
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= maximum_levels:
                    with open(f'assets/csv/level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)
        else:
            screen_scroll = 0
            if death_fade.fade():
                if restart_btn.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    world_data = reset_level()
                    with open(f'assets/csv/level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)
                if exit_btn.draw(screen):
                    # death_fade.fade_counter = 0
                    # start_intro = True
                    # bg_scroll = 0
                    exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_a:
                grenade = True
            if event.key == pygame.K_UP and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_a:
                grenade = False
                grenade_thrown = False

    pygame.display.update()

pygame.quit()
