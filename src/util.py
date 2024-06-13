import playerboard
from gameboard import GameBoard


COLOR_MAP = {
    'R': '\x1B[31m',
    'U': "\x1B[34m",
    'Y': "\x1B[33m",
    'B': "\x1B[36m",
    'L': "\x1B[35m",
    'X': "\x1B[0m",
}

def print_boards(gameboard, board_p1, board_p2):
    gameboard.print_board()
    space = 60
    print('-' * (50 + space))
    print('Player 1' + ' ' * space + 'Player 2')
    print('-' * (50 + space))
    print(f'Score: {board_p1.score}' + ' ' * space + f'Score: {board_p2.score}')
    print('-' * (50 + space))
    for i in range(5):
        #replace None with ' ' for better visualization
        #print then board
        print(
            f'{i} | {[p if p else " " for p in board_p1.build_tower[i]]}'
            + ' ' * ((space - 40) - (i*5)) + '|' 
            + f'{[ p[0].lower() if p[1] == 0 else p[0] for p in board_p1.board[i]]}'
            + ' ' * 13
            + f'{i} | {[p if p else " " for p in board_p2.build_tower[i]]}'
            + ' ' * ((space - 40) - (i*5)) + '|'
            + f'{[ p[0] for p in board_p2.board[i]]}'
            
        )

gbord = GameBoard(2)
p1 = playerboard.PlayerBoard()
p2 = playerboard.PlayerBoard()

print_boards(gbord, p1, p2)
