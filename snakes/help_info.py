"""Module help_info."""
__author__ = 'Joan A. Pinol  (japinol)'


class HelpInfo:
    """Manages information used for help purposes."""

    def print_help_keys(self):
        print('  F1: \t show a help screen while playing the game'
              '   t: \t stats on/off\n'
              '  L_Ctrl + R_Alt + g:  grid\n'
              '   p: \t pause\n'
              ' ESC: exit game\n'
              '  ^m: \t pause/resume music\n'
              '  ^s: \t sound effects on/off\n'
              '  Alt + Enter: change full screen / normal screen mode\n'
              '  ^h: \t shows this help\n'
              '     \t left,     a:  move snake to the left\n'
              '     \t right,    d:  move snake to the right\n'
              '     \t up,       w:  move snake up\n'
              '     \t down,     s:  move snake down\n'
              '     \t u         4:  fire a light shot\n'
              '     \t i         5:  fire a medium shot\n'
              '     \t j         1:  fire a strong shot\n'
              '     \t k         2:  fire a heavy shot\n'
              )
