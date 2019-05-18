"""Module levels."""
__author__ = 'Joan A. Pinol  (japinol)'

from random import randint

from snakes.actors import Actor
from snakes.apples import Apple, AppleType
from snakes.bats import Bat, BatType
from snakes.bullets import Bullet
from snakes.cartridges import Cartridge, CartridgeType
from snakes.mines import Mine, MineType
from snakes.recovery_potions import RecoveryPotion, RecoveryPotionType
from snakes.snakes import Snake


APPLE_TYPE_01_LEVEL_MULTIPLIER = 0.19
APPLE_TYPE_02_LEVEL_MULTIPLIER = 0.24
APPLE_TYPE_03_LEVEL_MULTIPLIER = 0.29

MINE_TYPE_01_LEVEL_MULTIPLIER = 0.25
MINE_TYPE_02_LEVEL_MULTIPLIER = 0.17

BAT_TYPE_01_LEVEL_MULTIPLIER = 0.22
BAT_TYPE_02_LEVEL_MULTIPLIER = 0.17
BAT_TYPE_03_LEVEL_MULTIPLIER = 0.13


class Level:
    """Represents a level."""
    def __init__(self, game):
        self.id = None
        self.start_time = None
        self.end_time = None
        self.game = game
        self.name = None
        self.next_level = None

    def start_up(self):
        self.start_time = self.game.current_time

    def clean_up(self):
        self.end_time = self.game.current_time
        # Remove current mines, cartridges and recovery potions from the board
        for mine in self.game.mines:
            mine.kill()
        for cartridge in self.game.cartridges:
            cartridge.kill()
        for rec_potion in self.game.rec_potions:
            rec_potion.kill()


class Level_01(Level):
    """Represents level 1."""
    def __init__(self, game):
        super().__init__(game)
        self.id = 0
        self.name = f'{self.id + 1:03}'
        self.next_level = self.id + 1
        # Initialize actors
        Actor.initialize_actors([Apple, Mine, Bat, Snake, Bullet, Cartridge, RecoveryPotion])

    def start_up(self):
        super().start_up()
        # Put apples on the board
        Apple.create_some_random_pos(n=2, apple_type=AppleType.T1_RED,
                                     apple_list=self.game.apples, game=self.game)

    def clean_up(self):
        super().clean_up()


class Level_02(Level):
    """Represents level 2."""
    def __init__(self, game):
        super().__init__(game)
        self.id = 1
        self.name = f'{self.id + 1:03}'
        self.next_level = self.id + 1

    def start_up(self):
        super().start_up()
        # Put apples on the board
        Apple.create_some_random_pos(n=2, apple_type=AppleType.T2_GREEN,
                                     apple_list=self.game.apples, game=self.game)
        Apple.create_some_random_pos(n=1, apple_type=AppleType.T3_YELLOW,
                                     apple_list=self.game.apples, game=self.game)

    def clean_up(self):
        super().clean_up()


class Level_03(Level):
    """Represents level 3."""
    def __init__(self, game):
        super().__init__(game)
        self.id = 2
        self.name = f'{self.id + 1:03}'
        self.next_level = self.id + 1

    def start_up(self):
        super().start_up()
        # Put apples on the board
        Apple.create_some_random_pos(n=1, apple_type=AppleType.T1_RED,
                                     apple_list=self.game.apples, game=self.game)
        Apple.create_some_random_pos(n=1, apple_type=AppleType.T2_GREEN,
                                     apple_list=self.game.apples, game=self.game)
        Apple.create_some_random_pos(n=1, apple_type=AppleType.T3_YELLOW,
                                     apple_list=self.game.apples, game=self.game)
        # Put mines on the board
        Mine.create_some_random_pos(n=1, mine_type=MineType.T1_AQUA, mine_list=self.game.mines,
                                    probability_each=80, game=self.game)
        # Put bats on the board
        Bat.create_some_random_pos(n=1, bat_type=BatType.T1_BLUE, bat_list=self.game.bats,
                                   probability_each=30, game=self.game)

    def clean_up(self):
        super().clean_up()


class Level_04(Level):
    """Represents level 4."""
    def __init__(self, game):
        super().__init__(game)
        self.id = 3
        self.name = f'{self.id + 1:03}'
        self.next_level = self.id + 1

    def start_up(self):
        super().start_up()
        # Put apples on the board
        Apple.create_some_random_pos(n=2, apple_type=AppleType.T1_RED,
                                     apple_list=self.game.apples, game=self.game)
        Apple.create_some_random_pos(n=2, apple_type=AppleType.T3_YELLOW,
                                     apple_list=self.game.apples, game=self.game)
        # Put mines on the board
        Mine.create_some_random_pos(n=1, mine_type=MineType.T1_AQUA, mine_list=self.game.mines,
                                    probability_each=100, game=self.game)
        Mine.create_some_random_pos(n=1, mine_type=MineType.T2_LILAC, mine_list=self.game.mines,
                                    probability_each=80, game=self.game)
        # Put bats on the board
        Bat.create_some_random_pos(n=1, bat_type=BatType.T2_LILAC, bat_list=self.game.bats,
                                   probability_each=80, game=self.game)

    def clean_up(self):
        super().clean_up()


class Level_05(Level):
    """Represents level 5."""
    def __init__(self, game):
        super().__init__(game)
        self.id = 4
        self.name = f'{self.id + 1:03}'
        self.next_level = self.id + 1

    def start_up(self):
        super().start_up()
        # Put apples on the board
        Apple.create_some_random_pos(n=1, apple_type=AppleType.T1_RED, probability_each=100,
                                     apple_list=self.game.apples, game=self.game)
        Apple.create_some_random_pos(n=3, apple_type=AppleType.T2_GREEN, probability_each=40,
                                     apple_list=self.game.apples, game=self.game)
        Apple.create_some_random_pos(n=3, apple_type=AppleType.T3_YELLOW, probability_each=40,
                                     apple_list=self.game.apples, game=self.game)
        # Put mines on the board
        Mine.create_some_random_pos(n=2, mine_type=MineType.T1_AQUA, mine_list=self.game.mines,
                                    probability_each=100, game=self.game)
        Mine.create_some_random_pos(n=1, mine_type=MineType.T2_LILAC, mine_list=self.game.mines,
                                    probability_each=100, game=self.game)
        Mine.create_some_random_pos(n=1, mine_type=MineType.T2_LILAC, mine_list=self.game.mines,
                                    probability_each=30, game=self.game)
        # Put bats on the board
        Bat.create_some_random_pos(n=1, bat_type=BatType.T1_BLUE, bat_list=self.game.bats,
                                   probability_each=100, game=self.game)

    def clean_up(self):
        super().clean_up()


class Level_06(Level):
    """Represents level 6."""
    def __init__(self, game):
        super().__init__(game)
        self.id = 5
        self.name = f'{self.id + 1:03}'
        self.next_level = self.id + 1

    def start_up(self):
        super().start_up()
        # Put apples on the board
        Apple.create_some_random_pos(n=1, apple_type=AppleType.T1_RED, probability_each=100,
                                     apple_list=self.game.apples, game=self.game)
        Apple.create_some_random_pos(n=3, apple_type=AppleType.T2_GREEN, probability_each=40,
                                     apple_list=self.game.apples, game=self.game)
        Apple.create_some_random_pos(n=4, apple_type=AppleType.T3_YELLOW, probability_each=20,
                                     apple_list=self.game.apples, game=self.game)
        # Put mines on the board
        Mine.create_some_random_pos(n=3, mine_type=MineType.T1_AQUA, mine_list=self.game.mines,
                                    probability_each=75, game=self.game)
        Mine.create_some_random_pos(n=1, mine_type=MineType.T2_LILAC, mine_list=self.game.mines,
                                    probability_each=100, game=self.game)
        Mine.create_some_random_pos(n=1, mine_type=MineType.T2_LILAC, mine_list=self.game.mines,
                                    probability_each=30, game=self.game)
        # Put bats on the board
        Bat.create_some_random_pos(n=2, bat_type=BatType.T1_BLUE, bat_list=self.game.bats,
                                   probability_each=60, game=self.game)

    def clean_up(self):
        super().clean_up()


class Level_07(Level):
    """Represents level 7."""
    def __init__(self, game):
        super().__init__(game)
        self.id = 6
        self.name = f'{self.id + 1:03}'
        self.next_level = self.id + 1

    def start_up(self):
        super().start_up()
        # Put apples on the board
        Apple.create_some_random_pos(n=1, apple_type=AppleType.T3_YELLOW, probability_each=100,
                                     apple_list=self.game.apples, game=self.game)
        Apple.create_some_random_pos(n=1, apple_type=AppleType.T1_RED, probability_each=40,
                                     apple_list=self.game.apples, game=self.game)
        Apple.create_some_random_pos(n=1, apple_type=AppleType.T2_GREEN, probability_each=40,
                                     apple_list=self.game.apples, game=self.game)
        Apple.create_some_random_pos(n=1, apple_type=AppleType.T3_YELLOW, probability_each=40,
                                     apple_list=self.game.apples, game=self.game)
        # Put mines on the board
        Mine.create_some_random_pos(n=2, mine_type=MineType.T1_AQUA, mine_list=self.game.mines,
                                    probability_each=100, game=self.game)
        Mine.create_some_random_pos(n=1, mine_type=MineType.T2_LILAC, mine_list=self.game.mines,
                                    probability_each=100, game=self.game)
        Mine.create_some_random_pos(n=1, mine_type=MineType.T2_LILAC, mine_list=self.game.mines,
                                    probability_each=40, game=self.game)
        # Put bats on the board
        Bat.create_some_random_pos(n=1, bat_type=BatType.T2_LILAC, bat_list=self.game.bats,
                                   probability_each=100, game=self.game)

    def clean_up(self):
        super().clean_up()


class Level_others(Level):
    """Represents other high levels."""
    def __init__(self, game):
        super().__init__(game)
        self.id = 7
        self.name = f'{self.id + 1:03}'
        self.next_level = self.id

    def start_up(self):
        super().start_up()
        self.id = self.game.current_level_no
        self.name = f'{self.game.current_level_no + 1:03}'
        level = self.game.current_level_no + 1
        # Put apples on the board
        Apple.create_some_random_pos(n=int(1 + level * APPLE_TYPE_01_LEVEL_MULTIPLIER),
                                     apple_type=AppleType.T1_RED, apple_list=self.game.apples,
                                     probability_each=75, game=self.game)
        Apple.create_some_random_pos(n=int(1 + level * APPLE_TYPE_02_LEVEL_MULTIPLIER),
                                     apple_type=AppleType.T2_GREEN, apple_list=self.game.apples,
                                     probability_each=90, game=self.game)
        Apple.create_some_random_pos(n=int(1 + level * APPLE_TYPE_03_LEVEL_MULTIPLIER),
                                     apple_type=AppleType.T3_YELLOW, apple_list=self.game.apples,
                                     probability_each=85, game=self.game)
        # Put mines on the board
        Mine.create_some_random_pos(n=int(level * MINE_TYPE_01_LEVEL_MULTIPLIER),
                                    mine_type=MineType.T1_AQUA, mine_list=self.game.mines,
                                    probability_each=80, game=self.game)
        Mine.create_some_random_pos(n=int(level * MINE_TYPE_02_LEVEL_MULTIPLIER),
                                    mine_type=MineType.T2_LILAC, mine_list=self.game.mines,
                                    probability_each=70, game=self.game)
        # Put cartridges and recovery potions on the board
        random_items_prob = randint(1, 100)
        if random_items_prob < 21:
            Cartridge.create_some_random_pos(n=1, cartridge_type=CartridgeType.T1_LASER1,
                                             cartridge_list=self.game.cartridges,
                                             probability_each=100, game=self.game)
        elif random_items_prob < 61:
            Cartridge.create_some_random_pos(n=1, cartridge_type=CartridgeType.T2_LASER2,
                                             cartridge_list=self.game.cartridges,
                                             probability_each=100, game=self.game)
            if level >= 14 and randint(1, 100) >= 80:
                Cartridge.create_some_random_pos(n=1, cartridge_type=CartridgeType.T3_PHOTONIC,
                                                 cartridge_list=self.game.cartridges,
                                                 probability_each=80, game=self.game)
                RecoveryPotion.create_some_random_pos(n=1, rec_potion_type=RecoveryPotionType.T2_POWER,
                                                      rec_potion_list=self.game.rec_potions,
                                                      probability_each=20, game=self.game)
        elif random_items_prob < 81:
            Cartridge.create_some_random_pos(n=1, cartridge_type=CartridgeType.T3_PHOTONIC,
                                             cartridge_list=self.game.cartridges,
                                             probability_each=90, game=self.game)
            RecoveryPotion.create_some_random_pos(n=1, rec_potion_type=RecoveryPotionType.T1_HEALTH,
                                                  rec_potion_list=self.game.rec_potions,
                                                  probability_each=80, game=self.game)
            if level >= 14 and randint(1, 100) >= 70:
                Cartridge.create_some_random_pos(n=1, cartridge_type=CartridgeType.T4_NEUTRONIC,
                                                 cartridge_list=self.game.cartridges,
                                                 probability_each=60, game=self.game)
                Cartridge.create_some_random_pos(n=1, cartridge_type=CartridgeType.T2_LASER2,
                                                 cartridge_list=self.game.cartridges,
                                                 probability_each=80, game=self.game)
        else:
            Cartridge.create_some_random_pos(n=1, cartridge_type=CartridgeType.T2_LASER2,
                                             cartridge_list=self.game.cartridges,
                                             probability_each=70, game=self.game)
            Cartridge.create_some_random_pos(n=1, cartridge_type=CartridgeType.T3_PHOTONIC,
                                             cartridge_list=self.game.cartridges,
                                             probability_each=30, game=self.game)
            if level >= 10 and randint(1, 100) >= 56:
                RecoveryPotion.create_some_random_pos(n=1, rec_potion_type=RecoveryPotionType.T1_HEALTH,
                                                      rec_potion_list=self.game.rec_potions,
                                                      probability_each=60, game=self.game)
                RecoveryPotion.create_some_random_pos(n=1, rec_potion_type=RecoveryPotionType.T2_POWER,
                                                      rec_potion_list=self.game.rec_potions,
                                                      probability_each=60, game=self.game)
        # Put bats on the board
        if level > 9:
            Bat.create_some_random_pos(n=1, bat_type=BatType.T3_RED, bat_list=self.game.bats,
                                       probability_each=90, game=self.game)
            Bat.create_some_random_pos(n=1, bat_type=BatType.T2_LILAC, bat_list=self.game.bats,
                                       probability_each=100, game=self.game)
        Bat.create_some_random_pos(n=int(level * BAT_TYPE_01_LEVEL_MULTIPLIER),
                                   bat_type=BatType.T1_BLUE, bat_list=self.game.bats,
                                   probability_each=80, game=self.game)
        Bat.create_some_random_pos(n=int(level * BAT_TYPE_02_LEVEL_MULTIPLIER),
                                   bat_type=BatType.T2_LILAC, bat_list=self.game.bats,
                                   probability_each=68, game=self.game)
        Bat.create_some_random_pos(n=1, bat_type=BatType.T3_RED, bat_list=self.game.bats,
                                   probability_each=34, game=self.game)

    def clean_up(self):
        super().clean_up()
