from gameboard import GameBoard
from playerboard import PlayerBoard

color_map = {
    "🟥": "\033[48;2;224;192;192;10m",  # Low-saturation red
    "🟩": "\033[48;2;192;224;192;10m",  # Low-saturation green
    "🟦": "\033[48;2;192;192;224;10m",  # Low-saturation blue
    "⬛": "\033[48;2;192;192;192;10m",  # Low-saturation black
    "🟧": "\033[48;2;224;224;192;10m",  # Low-saturation yellow
}


def _emoji_with_color(emoji: str, flag: int) -> str:
    if flag == 0:
        return f"{color_map[emoji]}{'    '}\033[0m"
    else:
        return f"{color_map[emoji]} { emoji } \033[0m"


def print_boards(
    gameboard: GameBoard, board_p1: PlayerBoard, board_p2: PlayerBoard
) -> None:
    print("-" * 115)
    print(" " * 57 + "STORE")
    for row_index, row in enumerate(gameboard.stores):
        print(f"{' ' * 50}" + f"{row_index} | {' '.join(cell[0] for cell in row)}")

    print(f"{' ' * 50}" + "C |", " ".join(cell[0] for cell in gameboard.center))

    print("-" * 115)

    print(f"{' ' * 25}" + "Player 1".ljust(65) + "Player 2")
    print("-" * 115)

    print(
        f"{' ' * 25}"
        + f"Score: {board_p1.score}".ljust(65)
        + f"Score: {board_p2.score}"
    )
    print("-" * 115)

    for i in range(len(board_p1.build_tower)):
        tower_1 = board_p1.build_tower[i]
        tower_2 = board_p2.build_tower[i]
        print(
            f"{i} |{' ' * (15 - 3*len(tower_1))} {' '.join('🟫' if cell is None else cell[0] for cell in tower_1)}",
            end=" | ",
        )
        print(
            f"{i} | {' '.join(_emoji_with_color(cell[0], cell[1]) for cell in board_p1.board[i])}",
            end=" | ",
        )

        print(" " * 13, end="")

        print(
            f"{i} |{' ' * (15 - 3*len(tower_2))} {' '.join('🟫' if cell is None else cell[0] for cell in tower_2)}",
            end=" | ",
        )

        print(
            f"{i} | {' '.join(_emoji_with_color(cell[0], cell[1]) for cell in board_p1.board[i])}"
        )

    print("-" * 115)
