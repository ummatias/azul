import pytest

from src.playerboard import PlayerBoard


@pytest.fixture
def player_board():
    return PlayerBoard()


def test_initialization(player_board):
    assert len(player_board.board) == 5
    assert len(player_board.build_tower) == 5
    assert len(player_board.broken_pieces) == 7
    assert player_board.score == 0


def test_check_tower(player_board):
    assert player_board.check_tower() == []

    # Fill some lines of the tower
    player_board.build_tower[0] = ["🟦"]
    player_board.build_tower[1] = ["🟩", "🟩"]
    player_board.build_tower[4] = ["🟦", "🟦", "🟦", "🟦", "🟦"]
    assert player_board.check_tower() == [0, 1, 4]


def test_place_pieces_tower(player_board):
    pieces = ["🟦", "🟧", "🟥"]

    # Test valid placement
    player_board.place_pieces_tower(pieces, 2)
    assert player_board.build_tower[2] == ["🟦", "🟧", "🟥"]

    # Test handling broken piece
    player_board.place_pieces_tower(["⬜"], "b")
    assert player_board.broken_pieces[0] == "⬜"

    # Test invalid line number
    with pytest.raises(ValueError):
        player_board.place_pieces_tower(pieces, 5)

    # Test invalid placement due to existing pieces
    with pytest.raises(ValueError):
        player_board.place_pieces_tower(["🟦"], 2)


def test_add_to_broken_pieces(player_board):
    player_board.add_to_broken_pieces("⬜")
    print(player_board.broken_pieces)
    assert player_board.broken_pieces[0] == "⬜"
    for _ in range(7):
        player_board.add_to_broken_pieces("🟦")

    assert player_board.broken_pieces[-1] == "🟦"


def test_calculate_penalties(player_board):
    player_board.add_to_broken_pieces("⬜")
    assert player_board.calculate_penalties() == -1
    assert all(piece is None for piece in player_board.broken_pieces)


def test_fill_board(player_board):
    player_board.build_tower[0] = ["🟦"]
    player_board.fill_board(0)
    assert player_board.board[0][0][1] == 1


def test_calculate_points(player_board):
    player_board.build_tower[0] = ["🟦"]
    player_board.build_tower[1] = ["🟩", "🟩"]
    player_board.build_tower[4] = ["🟦", "🟦", "🟦", "🟦", "🟦"]
    score = 0
    for line in [0, 1, 4]:
        for i, (p, filled) in enumerate(player_board.board[line]):
            if p == player_board.build_tower[line][0] and filled == 0:
                player_board.board[line][i] = (player_board.build_tower[line][0], 1)
                score += player_board.calculate_points(line, i)
    assert score == 4


def test_calculate_bonus_points(player_board):
    player_board.fill_board(0)
    assert player_board.calculate_bonus_points() >= 0


def test_check_end_game(player_board):
    assert not player_board.check_end_game()

    # Fill the board to simulate end game condition
    for row in player_board.board:
        for i, _ in enumerate(row):
            row[i] = (row[i][0], 1)
    assert player_board.check_end_game()
