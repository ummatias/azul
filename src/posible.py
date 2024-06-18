import random
import copy

from gameboard import GameBoard
from playerboard import PlayerBoard

gb = GameBoard(2)
stores = [
    ['🟧', '🟩', '🟦', '🟦'],
    ['🟧', '🟩', '🟦', '🟦'],
    ['⬛', '🟦', '🟧', '🟦'],
    ['🟧', '🟧', '🟧', '🟥'],
    ['🟩', '🟩', '🟦', '🟥'],
]

gb.stores = copy.deepcopy(stores)
p = PlayerBoard()
p2 = PlayerBoard()

b_tower = [
    [None],
    ['🟩', None],
    [None, None, None],
    [None, None, None, None],
    [None, None, None, None, None],
]

b2_tower = [
    [None],
    [None, None],
    [None, None, None],
    [None, None, None, None],
    [None, None, None, None, None],
]
p.build_tower = copy.deepcopy(b_tower)

p_moves = p.get_possible_moves(['🟧', '🟧'])
p_moves_2 = p2.get_possible_moves(['⬜'])
print(p_moves)
print()
print(p_moves_2)