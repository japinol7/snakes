"""Module scores."""
__author__ = 'Joan A. Pinol  (japinol)'

from datetime import datetime

from snakes import constants as consts
from snakes import lib_jp
from snakes.settings import Settings


class Scores:
    """Scores related stuff.

       TODO: Load and show scores of previous games.
    """

    @staticmethod
    def write_scores_to_file(game):
        """Save scores of the specified game to a file."""
        sep = ' |.| '  # Separator
        winner = game.winner and lib_jp.map_color_num_to_name_txt(game.winner.color) or 'Tie'
        scores_info = f"date: {str(datetime.now()):22}{sep}winner: {winner:10}{sep}" \
                      f"snake1_score: {game.snake1.stats['score']:7}{sep}snake2_score: {game.snake2.stats['score']:7}{sep}" \
                      f"snake1_apples: {game.snake1.stats['apples']:5}{sep}snake2_apples: {game.snake2.stats['apples']:5}{sep}" \
                      f"snake1_apples_t1 R: {game.snake1.stats['apples_t01']:5}{sep}snake2_apples_t1 R: {game.snake2.stats['apples_t01']:5}{sep}" \
                      f"snake1_apples_t2 G: {game.snake1.stats['apples_t02']:5}{sep}snake2_apples_t2 G: {game.snake2.stats['apples_t02']:5}{sep}" \
                      f"snake1_apples_t3 Y: {game.snake1.stats['apples_t03']:5}{sep}snake2_apples_t3 Y: {game.snake2.stats['apples_t03']:5}{sep}" \
                      f"snake1_bats_t1 B: {game.snake1.stats['bats_t01']:5}{sep}snake2_bats_t1 B: {game.snake2.stats['bats_t01']:5}{sep}" \
                      f"snake1_bats_t2 L: {game.snake1.stats['bats_t02']:5}{sep}snake2_bats_t2 L: {game.snake2.stats['bats_t02']:5}{sep}" \
                      f"snake1_bats_t3 R: {game.snake1.stats['bats_t03']:5}{sep}snake2_bats_t3 R: {game.snake2.stats['bats_t03']:5}{sep}" \
                      f"snake1_mines_t1 A: {game.snake1.stats['mines_t01']:5}{sep}snake2_mines_t1 A: {game.snake2.stats['mines_t01']:5}{sep}" \
                      f"snake1_mines_t2 L: {game.snake1.stats['mines_t02']:5}{sep}snake2_mines_t2 L: {game.snake2.stats['mines_t02']:5}{sep}" \
                      f"snake1_bullets_t1 shot: {game.snake1.stats['bullets_t01_shot']:5}{sep}snake2_bullets_t1 shot: {game.snake2.stats['bullets_t01_shot']:5}{sep}" \
                      f"snake1_bullets_t2 shot: {game.snake1.stats['bullets_t02_shot']:5}{sep}snake2_bullets_t2 shot: {game.snake2.stats['bullets_t02_shot']:5}{sep}" \
                      f"snake1_bullets_t3 shot: {game.snake1.stats['bullets_t03_shot']:5}{sep}snake2_bullets_t3 shot: {game.snake2.stats['bullets_t03_shot']:5}{sep}" \
                      f"snake1_bullets_t4 shot: {game.snake1.stats['bullets_t04_shot']:5}{sep}snake2_bullets_t4 shot: {game.snake2.stats['bullets_t04_shot']:5}{sep}" \
                      f"snake1_body_len: {game.snake1.body_length:4}{sep}snake2_body_len: {game.snake2.body_length:4}{sep}" \
                      f"level: {game.current_level_no+1:4}{sep}snake_body_len_start: {Settings.snake_body_len_start:4}{sep}" \
                      f"snake_body_len_to_win: {Settings.snake_body_len_max:4}{sep}score_to_win: {Settings.score_to_win:7}{sep}" \
                      f"screen_width: {Settings.screen_width:4}{sep}screen_height: {Settings.screen_height:4}{sep}" \
                      f"cell_size: {Settings.cell_size:3}{sep}fps: {Settings.fps:3}{sep}speed: {Settings.speed_pct:4}\n"
        lib_jp.write_list_to_file(consts.SCORES_FILE, [scores_info], open_method='a')
