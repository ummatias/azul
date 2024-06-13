import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), './'))

from game import Game

if __name__ == "__main__":
    game = Game(qtd_players=2)
    game.play_game()