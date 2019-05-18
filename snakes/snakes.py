"""Module snakes."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from snakes.bullets import Bullet
from snakes.colors import Color
from snakes import constants as consts
from snakes.experience_points import ExperiencePoints
from snakes import resources
from snakes.settings import Settings


SNAKE_LIVES_DEFAULT = 3
SNAKE_HEALTH = 100
SNAKE_HEALTH_DEFAULT = 100
SNAKE_POWER = 100
SNAKE_POWER_DEFAULT = 100
SNAKE_MAX_BODY_LENGTH = 500
SNAKE_DEFAULT_ATTACK_POWER = 7

SNAKE_BULLETS_T1_DEFAULT = 30
SNAKE_BULLETS_T2_DEFAULT = 20
SNAKE_BULLETS_T3_DEFAULT = 10
SNAKE_BULLETS_T4_DEFAULT = 6

SNAKE_BULLETS_MAX = 499  # For each type


class Snake(pg.sprite.Sprite):
    """Represents a snake."""
    sprite_images = {}

    def __init__(self, color, x, y, game):
        super().__init__()
        self.color = color
        self.is_alive = True
        self.change_x = 0
        self.change_y = 0
        self.game = game
        self.snake = self
        self.attack_power = SNAKE_DEFAULT_ATTACK_POWER
        self.other_snakes = pg.sprite.Group()
        self.body_length = Snake.body_len_start = Settings.snake_body_len_start
        self.speed = Settings.cell_size
        self.body_pieces = []
        self.rip_frames = []
        self.direction = consts.DIRECTION_RIGHT
        self.direction_old = self.direction
        self.images_sprite_no = 1
        self.frame = 0
        self.rect = False
        self.rect_old = False
        self.body_len_start = None
        self.stats = {'score': 0,
                      'lives': SNAKE_LIVES_DEFAULT,
                      'health': SNAKE_HEALTH_DEFAULT,
                      'power': SNAKE_POWER_DEFAULT,
                      'speed': self.speed,
                      'health_max': SNAKE_HEALTH,
                      'power_max': SNAKE_POWER,
                      'bullets_t01': SNAKE_BULLETS_T1_DEFAULT,
                      'bullets_t01_shot': 0,
                      'bullets_t02': SNAKE_BULLETS_T2_DEFAULT,
                      'bullets_t02_shot': 0,
                      'bullets_t03': SNAKE_BULLETS_T3_DEFAULT,
                      'bullets_t03_shot': 0,
                      'bullets_t04': SNAKE_BULLETS_T4_DEFAULT,
                      'bullets_t04_shot': 0,
                      'apples': 0,
                      'apples_t01': 0,
                      'apples_t02': 0,
                      'apples_t03': 0,
                      'mines': 0,
                      'mines_t01': 0,
                      'mines_t02': 0,
                      'bats': 0,
                      'bats_t01': 0,
                      'bats_t02': 0,
                      'bats_t03': 0,
                      }
        self.stats_old = {'score': None,
                          'lives': None,
                          'health': None,
                          'power': None,
                          'speed': None,
                          'bullets_t01': None,
                          'bullets_t02': None,
                          'bullets_t03': None,
                          'bullets_t04': None,
                          'apples': None,
                          'mines': None,
                          }

        # Snake's head by direction
        if not Snake.sprite_images.get((self.color, consts.DIRECTION_RIGHT)):
            snake_type_short = 'head'
            image_quality = '_md' if Settings.cell_size >= consts.CELL_SIZE_MIN_FOR_IM_MD else ''

            image = pg.image.load(resources.file_name_get(name='im_snake_', subname=snake_type_short,
                                                          quality=image_quality, num=self.color, subnum=1)).convert()
            image = pg.transform.smoothscale(image, (Settings.cell_size, Settings.cell_size))
            image.set_colorkey(Color.BLACK)
            Snake.sprite_images[(self.color, consts.DIRECTION_RIGHT)] = image

            image = pg.image.load(resources.file_name_get(name='im_snake_', subname=snake_type_short,
                                                          quality=image_quality, num=self.color, subnum=1)).convert()
            image = pg.transform.flip(image, True, False)
            image = pg.transform.smoothscale(image, (Settings.cell_size, Settings.cell_size))
            image.set_colorkey(Color.BLACK)
            Snake.sprite_images[(self.color, consts.DIRECTION_LEFT)] = image

            image = pg.image.load(resources.file_name_get(name='im_snake_', subname=snake_type_short,
                                                          quality=image_quality, num=self.color, subnum=1)).convert()
            image = pg.transform.rotate(image, 90)
            image = pg.transform.smoothscale(image, (Settings.cell_size, Settings.cell_size))
            image.set_colorkey(Color.BLACK)
            Snake.sprite_images[(self.color, consts.DIRECTION_UP)] = image

            image = pg.image.load(resources.file_name_get(name='im_snake_', subname=snake_type_short,
                                                          quality=image_quality, num=self.color, subnum=1)).convert()
            image = pg.transform.rotate(image, 270)
            image = pg.transform.smoothscale(image, (Settings.cell_size, Settings.cell_size))
            image.set_colorkey(Color.BLACK)
            Snake.sprite_images[(self.color, consts.DIRECTION_DOWN)] = image

        self.image = Snake.sprite_images[(self.color, consts.DIRECTION_RIGHT)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect_old = self.image.get_rect()
        self.rect_old.x = self.rect.x
        self.rect_old.y = self.rect.y

        # Snake's body and tail
        previous_body_piece = self
        for i in range(self.body_length):
            self.body_pieces.append(SnakeBodyPiece(snake=self, previous_body_piece=previous_body_piece,
                                    x=self.rect.x-((i+1)*Settings.cell_size), y=self.rect.y))
            previous_body_piece = self.body_pieces[i]

        # Add snake's head and body to the active sprite list
        self.game.active_sprites.add(self)
        for body_piece in self.body_pieces:
            self.game.active_sprites.add(body_piece)
            self.game.snakes.add(body_piece)

    def add_body_piece(self):
        snake_body_piece = SnakeBodyPiece(snake=self, previous_body_piece=self.body_pieces[self.body_length-1],
                                          x=self.body_pieces[self.body_length-1].previous_body_piece.rect_old.x,
                                          y=self.body_pieces[self.body_length-1].previous_body_piece.rect_old.y)
        self.body_pieces.append(snake_body_piece)
        self.game.active_sprites.add(self.body_pieces[self.body_length])
        self.body_length += 1
        for snake in self.game.snake_heads:
            if snake is not self:
                snake.other_snakes.add(snake_body_piece)

    def fill_other_snakes_group(self):
        # For each snake, find out which snake body pieces are from another snakes
        for snake_piece in self.game.snakes:
            if snake_piece.snake is not self:
                self.other_snakes.add(snake_piece)

    def update(self):
        if self.direction == consts.DIRECTION_RIP:
            # Check if any bullet hit us
            bullet_hit_list = pg.sprite.spritecollide(self, self.game.bullets, False)
            for bullet in bullet_hit_list:
                self.game.sound_effects and resources.Resource.bullet_hit_sound.play()
                bullet.kill()
            return
        # Previous position. It will be used for the first piece of the body
        self.rect_old.x = self.rect.x
        self.rect_old.y = self.rect.y
        self.direction_old = self.direction

        # Move left, right, up, down
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        self.image = Snake.sprite_images[(self.color, self.direction)]

        # Control board's limits
        if self.rect.x >= Settings.screen_width:
            self.rect.x = 0
        elif self.rect.x < 0:
            self.rect.x = Settings.screen_near_right
        if self.rect.y >= Settings.screen_near_bottom:
            self.rect.y = Settings.screen_near_top
        elif self.rect.y < Settings.screen_near_top - 2:
            self.rect.y = Settings.screen_height - Settings.cell_size

        # Check if we hit any apple
        apple_hit_list = pg.sprite.spritecollide(self, self.game.apples, False)
        for apple in apple_hit_list:
            self.game.sound_effects and resources.Resource.apple_hit_sound.play()
            self.add_body_piece()
            self.stats[apple.apple_type_txt] += 1
            self.stats['score'] += ExperiencePoints.xp_points[apple.apple_type_txt]
            self.stats['apples'] += 1
            apple.kill()

        # Check if we hit any cartridge
        cartridge_hit_list = pg.sprite.spritecollide(self, self.game.cartridges, False)
        for cartridge in cartridge_hit_list:
            self.game.sound_effects and resources.Resource.item_hit_sound.play()
            self.stats[cartridge.bullet_type.value] += cartridge.qty
            if self.stats[cartridge.bullet_type.value] > SNAKE_BULLETS_MAX:
                self.stats[cartridge.bullet_type.value] = SNAKE_BULLETS_MAX
            cartridge.kill()

        # Check if we hit any recovery potion
        rec_potion_hit_list = pg.sprite.spritecollide(self, self.game.rec_potions, False)
        for rec_potion in rec_potion_hit_list:
            self.game.sound_effects and resources.Resource.item_hit_sound.play()
            self.stats[rec_potion.rec_potion_type.value] += rec_potion.qty
            if self.stats[rec_potion.rec_potion_type.value] > self.stats[f'{rec_potion.rec_potion_type.value}_max']:
                self.stats[rec_potion.rec_potion_type.value] = self.stats[f'{rec_potion.rec_potion_type.value}_max']
            rec_potion.kill()

        # Check if we hit any mine
        mine_hit_list = pg.sprite.spritecollide(self, self.game.mines, False)
        for mine in mine_hit_list:
            self.game.sound_effects and resources.Resource.mine_hit_sound.play()
            mine.kill()
            self.stats['health'] -= mine.attack_power
            if self.stats['health'] < 1:
                self._die_hard()

        # Check if we hit any bat
        bat_hit_list = pg.sprite.spritecollide(self, self.game.bats, False)
        for bat in bat_hit_list:
            bat.health -= self.attack_power
            if bat.health < 1:
                self.game.sound_effects and resources.Resource.bat_scream_sound.play()
                self.stats[bat.bat_type_txt] += 1
                self.stats['bats'] += 1
                self.stats['score'] += ExperiencePoints.xp_points[bat.bat_type_txt]
                bat.kill()
            else:
                self.game.sound_effects and resources.Resource.bat_hit_sound.play()
            self.stats['health'] -= bat.attack_power
            if self.stats['health'] < 1:
                self._die_hard()

        # Check if we hit another snake
        snake_piece_hit_list = pg.sprite.spritecollide(self, self.other_snakes, False)
        for snake_piece in snake_piece_hit_list:
            self.game.sound_effects and resources.Resource.collission_sound.play()
            self.stats['health'] -= snake_piece.snake.attack_power
            if self.stats['health'] < 1:
                self._die_hard()

        # Check if any bullet hit us
        bullet_hit_list = pg.sprite.spritecollide(self, self.game.bullets, False)
        for bullet in bullet_hit_list:
            if bullet.owner == self:
                break
            self.game.sound_effects and resources.Resource.bullet_hit_sound.play()
            bullet.kill()
            self.stats['health'] -= bullet.attack_power
            if self.stats['health'] < 1:
                self._die_hard()

        if self.body_length >= Settings.snake_body_len_max or self.stats['score'] >= Settings.score_to_win:
            self.game.winner = self

    def go_left(self):
        if self.direction in (consts.DIRECTION_RIP, consts.DIRECTION_RIGHT):
            return
        self.change_x = -self.speed
        self.change_y = 0
        self.direction = consts.DIRECTION_LEFT

    def go_right(self):
        if self.direction in (consts.DIRECTION_RIP, consts.DIRECTION_LEFT):
            return
        self.change_x = self.speed
        self.change_y = 0
        self.direction = consts.DIRECTION_RIGHT

    def go_up(self):
        if self.direction in (consts.DIRECTION_RIP, consts.DIRECTION_DOWN):
            return
        self.change_y = -self.speed
        self.change_x = 0
        self.direction = consts.DIRECTION_UP

    def go_down(self):
        if self.direction in (consts.DIRECTION_RIP, consts.DIRECTION_UP):
            return
        self.change_y = self.speed
        self.change_x = 0
        self.direction = consts.DIRECTION_DOWN

    def stop(self):
        self.change_x = 0
        self.change_y = 0

    def shot_bullet(self, bullet_type):
        if self.direction == consts.DIRECTION_RIP:
            return
        if (self.stats[bullet_type.value] < 1
                or self.stats['power'] < Bullet.power_min_to_use[bullet_type]):
            # Not enough bullets or power for this kind of weapon
            self.game.sound_effects and resources.Resource.weapon_empty_sound.play()
            return
        self.stats[f'{bullet_type.value}_shot'] += 1
        self.stats[bullet_type.value] -= 1
        self.stats['power'] -= Bullet.power_consumption[bullet_type]
        Bullet.shot(bullet_type=bullet_type, change_x=self.change_x * 2,
                    change_y=self.change_y * 2, owner=self, game=self.game)

    def _die_hard(self):
        if self.direction == consts.DIRECTION_RIP:
            return
        self.stats['lives'] -= 1
        self.stats['health'] = SNAKE_HEALTH_DEFAULT
        if self.stats['lives'] < 1:
            self.stop()
            self.direction = consts.DIRECTION_RIP
            self.stats['health'] = 0
            self.is_alive = False

    @classmethod
    def init(cls):
        cls._resize_images_on_cache()

    @classmethod
    def _resize_images_on_cache(cls):
        if not cls.sprite_images:
            return
        cell_size = Settings.cell_size
        for key, image in cls.sprite_images.items():
            if cell_size != image.get_size()[0] or cell_size != image.get_size()[1]:
                cls.sprite_images[key] = pg.transform.smoothscale(image, (cell_size, cell_size))

        for key, image in SnakeBodyPiece.sprite_images.items():
            if cell_size != image.get_size()[0] or cell_size != image.get_size()[1]:
                SnakeBodyPiece.sprite_images[key] = pg.transform.smoothscale(image, (cell_size, cell_size))


class SnakeBodyPiece(pg.sprite.Sprite):
    """Represents a body piece of a snake."""
    sprite_images = {}

    def __init__(self, snake, previous_body_piece, x, y):
        super().__init__()
        self.snake = snake
        self.previous_body_piece = previous_body_piece
        self.direction = consts.DIRECTION_RIGHT
        self.rect = False
        self.rect_old = False

        # Snake's body piece
        if not SnakeBodyPiece.sprite_images.get(self.snake.color):
            snake_type_short = 'body'
            image_quality = '_md' if Settings.cell_size >= consts.CELL_SIZE_MIN_FOR_IM_MD else ''
            image = pg.image.load(resources.file_name_get(name='im_snake_',
                                                          subname=snake_type_short,
                                                          quality=image_quality,
                                                          num=self.snake.color, subnum=1)).convert()
            image = pg.transform.smoothscale(image, (Settings.cell_size, Settings.cell_size))
            image.set_colorkey(Color.BLACK)
            self.image = image
            SnakeBodyPiece.sprite_images[self.snake.color] = self.image
        else:
            self.image = SnakeBodyPiece.sprite_images[self.snake.color]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect_old = self.image.get_rect()
        self.rect_old.x = self.rect.x
        self.rect_old.y = self.rect.y

    def update(self):
        # Check if any bullet hit us
        bullet_hit_list = pg.sprite.spritecollide(self, self.snake.game.bullets, False)
        for bullet in bullet_hit_list:
            self.snake.game.sound_effects and resources.Resource.bullet_hit_sound.play()
            bullet.kill()
        if self.direction == consts.DIRECTION_RIP:
            return
        self.rect_old.x = self.rect.x
        self.rect_old.y = self.rect.y
        self.direction_old = self.direction
        self.rect.x = self.previous_body_piece.rect_old.x
        self.rect.y = self.previous_body_piece.rect_old.y
        self.direction = self.previous_body_piece.direction
