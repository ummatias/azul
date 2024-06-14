from game import Game
from gameboard import GameBoard
from playerboard import PlayerBoard

color_map = {
    "🟥": "\033[48;2;224;192;192;10m",  # Low-saturation red
    "🟩": "\033[48;2;192;224;192;10m",  # Low-saturation green
    "🟦": "\033[48;2;192;192;224;10m",  # Low-saturation blue
    "⬛": "\033[48;2;192;192;192;10m",  # Low-saturation black
    "🟧": "\033[48;2;224;224;192;10m",  # Low-saturation yellow
}


def emoji_with_color(emoji: str, flag: int) -> str:
    if flag == 0:
        return f"{color_map[emoji]}{'    '}\033[0m"
    else:
        return f"{color_map[emoji]} { emoji } \033[0m"


def print_boards(
    gameboard: GameBoard, board_p1: PlayerBoard, board_p2: PlayerBoard
) -> None:

    print(" " * 7 + "STORE")
    for row_index, row in enumerate(gameboard.stores):
        print(f"{row_index} | {' '.join(cell[0] for cell in row)}")

    print("C |", " ".join(cell[0] for cell in gameboard.center))

    print("-" * 85)

    print("Player 1".ljust(50) + "Player 2")
    print("-" * 85)

    print("Score: 0".ljust(50) + "Score: 0")
    print("-" * 85)

    for i in range(len(board_p1.build_tower)):
        tower_1 = board_p1.build_tower[i]
        tower_2 = board_p2.build_tower[i]
        print(
            f"{i} |{' ' * (10 - 2*len(tower_1))} {' '.join('.' if cell is None else cell[0] for cell in tower_1)}",
            end=" | ",
        )
        print(
            f"{i} | {' '.join(emoji_with_color(cell[0], cell[1]) for cell in board_p1.board[i])}",
            end=" | ",
        )

        print(" " * 13, end="")

        print(
            f"{i} |{' ' * (10 - 2*len(tower_2))} {' '.join('.' if cell is None else cell[0] for cell in tower_2)}",
            end=" | ",
        )

        print(
            f"{i} | {' '.join(emoji_with_color(cell[0], cell[1]) for cell in board_p1.board[i])}"
        )
