"""Module __main__. Entry point."""
__author__ = 'Joan A. Pinol  (japinol)'
__version__ = '1.0.4'

from argparse import ArgumentParser
import gc
import traceback

import pygame as pg

from snakes.snakes_game import Game, logger
from snakes import screen


def main():
    """Entry point of the Snakes program."""
    # Parse optional arguments from the command line
    parser = ArgumentParser(description="Snakes.",
                            prog="snakes",
                            usage="%(prog)s [-h] [-b BODY_LENGTH] [-m MAX_BODY_LEN] [-r SCORE_TO_WIN]"
                            "[-c CELL_SIZE] [-w SCREEN_WIDTH] [-e SCREEN_HEIGHT] [-p] [-f] [-s SPEED_PCT] "
                            "[-u] [-t]")
    parser.add_argument('-b', '--bodylen', default=None,
                        help='body length of the snakes at the start of the game.')
    parser.add_argument('-m', '--maxbodylen', default=None,
                        help='when a snake reaches the max. body length, the game ends.')
    parser.add_argument('-r', '--scoretowin', default=None,
                        help='when a snake reaches this score, the game ends and it wins.')
    parser.add_argument('-c', '--cellsize', default=None,
                        help='the size of each cell, i.e., the size of the serpent pieces.')
    parser.add_argument('-w', '--widthscreen', default=None,
                        help='the width of the screen.\n'
                              'If screen height is not supplied, the best proportion is calculated.')
    parser.add_argument('-e', '--heightscreen', default=None,
                        help='the height of the screen.\n'
                              'If screen width is not supplied, the best proportion is calculated.')
    parser.add_argument('-p', '--portrait', default=None, action='store_true',
                        help='set screen to portrait mode.')
    parser.add_argument('-f', '--fullscreen', default=None, action='store_true',
                        help='Starts the game in full screen mode.')
    parser.add_argument('-s', '--speedpct', default=None,
                        help='changes the speed of the game by a percentage.\n'
                             'For example: 200 would be twice the normal speed, 50 would be half the normal speed.')
    parser.add_argument('-u', '--nodisplayscaled', default=False, action='store_true',
                        help='Remove the scaling of the game screen. '
                             'Resolution depends on desktop size and scale graphics. '
                             'Note that Pygame scaled is considered an experimental API '
                             'and is subject to change.')
    parser.add_argument('-t', '--debugtraces', default=None, action='store_true',
                        help='Show debug back traces information when something goes wrong.')
    args = parser.parse_args()

    pg.init()
    is_music_paused = False
    # Multiple games loop
    while not Game.is_exit_game:
        try:
            game = Game(screen_width=args.widthscreen, screen_height=args.heightscreen,
                        is_full_screen=args.fullscreen, is_no_display_scaled=args.nodisplayscaled,
                        cell_size=args.cellsize, speed_pct=args.speedpct,
                        snake_body_len_start=args.bodylen, snake_body_len_max=args.maxbodylen,
                        score_to_win=args.scoretowin, portrait_mode=args.portrait)
            game.is_music_paused = is_music_paused
            screen_start_game = screen.StartGame(game)
            while game.is_start_screen:
                screen_start_game.start_up()
            if not Game.is_exit_game:
                game.start()
                is_music_paused = game.is_music_paused
                del screen_start_game
                del game
                gc.collect()
        except FileNotFoundError as e:
            if args.debugtraces:
                traceback.print_tb(e.__traceback__)
            logger.critical(f'File not found error: {e}')
            break
        except Exception as e:
            if args.debugtraces:
                traceback.print_tb(e.__traceback__)
            logger.critical(f'Error: {e}')
            break
    pg.quit()


if __name__ == '__main__':
    main()
