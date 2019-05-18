"""Module debug_info."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import OrderedDict
from datetime import datetime

from snakes import constants as consts
from snakes import lib_jp
from snakes.settings import Settings


class DebugInfo:
    """Manages information used for debug and log purposes."""

    def __init__(self, snake1, snake2, game):
        self.snake1 = snake1
        self.snake2 = snake2
        self.game = game
        lib_jp.write_list_to_file(consts.LOG_FILE, [],
                                  open_method='a' if game.current_game > 1 else 'w')

    def print_help_keys(self):
        print('  ^;: \t ^ñ interactive debug output (not available)\n'
              '  ^d: \t print debug information to console\n'
              '  ^l: \t write debug information to log file\n'
              )

    def print_debug_info(self, to_log_file=False):
        debug_dict = OrderedDict([
                    ('time', str(datetime.now())),
                    ('full screen', Settings.is_full_screen),
                    ('screen size', self.game.size),
                    ('speed', Settings.speed_pct),
                    ('fps in settings', Settings.fps),
                    ('fps', self.game.is_paused and '\t ---- (The game is paused)'
                     or "\t {:.2f}".format(self.game.clock.get_fps())),
                    ('cell size', Settings.cell_size),
                    ('body length start', Settings.snake_body_len_start),
                    ('body length to win', Settings.snake_body_len_max),
                    ('score to win', Settings.score_to_win),
                    ('current song', consts.MUSIC_BOX[self.game.current_song]),
                    ('music playing', not self.game.is_music_paused),
                    ('sound effects', self.game.sound_effects),
                    ('game paused', self.game.is_paused),
                    ('current game', self.game.current_game),
                    ('level', self.game.current_level_no + 1),
                    ('level_name', self.game.current_level.name),
                    ('total sprites', self.game.active_sprites),
                    ('apples on the board', self.game.apples),
                    ('mines on the board', self.game.mines),
                    ('bats on the board', self.game.bats),
                    ('bullets on the board', self.game.bullets),
                    ('game over:', self.game.is_over),
                    ('winner:', self.game.winner and lib_jp.map_color_num_to_name_txt(self.game.winner.color)),
                    ('-----' * 3, ''),
                    ('snake1', OrderedDict([
                            ('color:', lib_jp.map_color_num_to_name_txt(self.snake1.color)),
                            ('position (x, y)', (self.snake1.rect.x, self.snake1.rect.y)),
                            ('position (bottom)', self.snake1.rect.bottom),
                            ('direction', lib_jp.map_direction_to_string(self.snake1.direction)),
                            ('change position (x, y)', (self.snake1.change_x, "%.3f" % self.snake1.change_y)),
                            ('body length', self.snake1.body_length),
                            ('stats', OrderedDict([
                                    ('lives', self.snake1.stats['lives']),
                                    ('health', self.snake1.stats['health']),
                                    ('power', int(round(self.snake1.stats['power'], 0))),
                                    ('speed', self.snake1.stats['speed']),
                                    ('bullets_t1 shot', self.snake1.stats['bullets_t01_shot']),
                                    ('bullets_t2 shot', self.snake1.stats['bullets_t02_shot']),
                                    ('bullets_t3 shot', self.snake1.stats['bullets_t03_shot']),
                                    ('bullets_t4 shot', self.snake1.stats['bullets_t04_shot']),
                                    ('bullets_t1 remaining', self.snake1.stats['bullets_t01']),
                                    ('bullets_t2 remaining', self.snake1.stats['bullets_t02']),
                                    ('bullets_t3 remaining', self.snake1.stats['bullets_t03']),
                                    ('bullets_t4 remaining', self.snake1.stats['bullets_t04']),
                                    ('mines', self.snake1.stats['mines']),
                                    ('mines_t1', self.snake1.stats['mines_t01']),
                                    ('mines_t2', self.snake1.stats['mines_t02']),
                                    ('bats   ', self.snake1.stats['bats']),
                                    ('bats_t1 B', self.snake1.stats['bats_t01']),
                                    ('bats_t2 L', self.snake1.stats['bats_t02']),
                                    ('bats_t3 R', self.snake1.stats['bats_t03']),
                                    ('score', self.snake1.stats['score']),
                                    ('apples', self.snake1.stats['apples']),
                                    ('apples_t1 R', self.snake1.stats['apples_t01']),
                                    ('apples_t2 G', self.snake1.stats['apples_t02']),
                                    ('apples_t3 Y', self.snake1.stats['apples_t03']),
                                ])
                             ),
                             ])
                     ),
                    ('-----' * 3 + '-', ''),
                    ('snake2', OrderedDict([
                            ('color:', lib_jp.map_color_num_to_name_txt(self.snake2.color)),
                            ('position (x, y)', (self.snake2.rect.x, self.snake2.rect.y)),
                            ('position (bottom)', self.snake2.rect.bottom),
                            ('direction', lib_jp.map_direction_to_string(self.snake2.direction)),
                            ('change position (x, y)', (self.snake2.change_x, "%.3f" % self.snake2.change_y)),
                            ('body length', self.snake2.body_length),
                            ('stats', OrderedDict([
                                    ('lives', self.snake2.stats['lives']),
                                    ('health', self.snake2.stats['health']),
                                    ('power', int(round(self.snake2.stats['power'], 0))),
                                    ('speed', self.snake2.stats['speed']),
                                    ('bullets_t1 shot', self.snake2.stats['bullets_t01_shot']),
                                    ('bullets_t2 shot', self.snake2.stats['bullets_t02_shot']),
                                    ('bullets_t3 shot', self.snake2.stats['bullets_t03_shot']),
                                    ('bullets_t4 shot', self.snake2.stats['bullets_t04_shot']),
                                    ('bullets_t1 remaining', self.snake2.stats['bullets_t01']),
                                    ('bullets_t2 remaining', self.snake2.stats['bullets_t02']),
                                    ('bullets_t3 remaining', self.snake2.stats['bullets_t03']),
                                    ('bullets_t4 remaining', self.snake2.stats['bullets_t04']),
                                    ('mines', self.snake2.stats['mines']),
                                    ('mines_t1', self.snake2.stats['mines_t01']),
                                    ('mines_t2', self.snake2.stats['mines_t02']),
                                    ('bats   ', self.snake2.stats['bats']),
                                    ('bats_t1 B', self.snake2.stats['bats_t01']),
                                    ('bats_t2 L', self.snake2.stats['bats_t02']),
                                    ('bats_t3 R', self.snake2.stats['bats_t03']),
                                    ('score', self.snake2.stats['score']),
                                    ('apples', self.snake2.stats['apples']),
                                    ('apples_t1 R', self.snake2.stats['apples_t01']),
                                    ('apples_t2 G', self.snake2.stats['apples_t02']),
                                    ('apples_t3 Y', self.snake2.stats['apples_t03']),
                                ])
                             ),
                             ])
                     ),
        ])
        debug_info_title = 'Current game stats'
        debug_info = '%s%s%s%s\n' % ('\n\n\n', '-' * 25, debug_info_title, '-' * 25)
        debug_info = '%s%s%s\n' % (debug_info, lib_jp.pretty_dict_to_string(debug_dict, with_last_new_line=True),
                                   '-' * (25 + len(debug_info_title) + 25))
        if to_log_file:
            lib_jp.write_list_to_file(consts.LOG_FILE, [debug_info], open_method='a')
        else:
            print(debug_info)
