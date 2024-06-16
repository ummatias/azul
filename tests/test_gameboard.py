import pytest

from src.gameboard import GameBoard


def test_gameboard_initialization():
    board = GameBoard(2)
    assert board.center == ["⬜"]
    assert len(board.stores) == 5
    assert all(store == [] for store in board.stores)

    board = GameBoard(3)
    assert board.center == ["⬜"]
    assert len(board.stores) == 7
    assert all(store == [] for store in board.stores)

    board = GameBoard(4)
    assert board.center == ["⬜"]
    assert len(board.stores) == 9
    assert all(store == [] for store in board.stores)


def test_distribute_pieces():
    board = GameBoard(2)
    pieces = ["U", "R", "B", "G", "Y"] * 4
    board.distribute_pieces(pieces.copy())
    assert len(board.center) == 1
    assert all(len(store) == 4 for store in board.stores)
    assert sum(len(store) for store in board.stores) == 20


def test_draw_pieces():
    board = GameBoard(2)
    pieces = ["U", "R", "B", "G", "Y"]
    drawn_pieces = board._draw_pieces(pieces, 3)
    assert len(drawn_pieces) == 3
    assert len(pieces) == 2


def test_pick_piece_from_store():
    board = GameBoard(2)
    board.stores = [
        ["🟦", "🟩", "🟩", "🟩"],
        ["🟩", "🟦", "🟦", "🟦"],
        ["🟦", "🟦", "🟦", "🟦"],
        ["🟦", "🟦", "🟦", "🟦"],
        ["🟦", "🟦", "🟦", "🟦"],
    ]
    picked_pieces = board.pick_piece(0, "U")
    assert picked_pieces == ["🟦"] * 1
    assert len(board.stores[0]) == 0
    assert len(board.center) == 4  # 1 initial + 3 remaining from store


def test_pick_piece_from_center():
    board = GameBoard(2)
    board.center = ["⬜", "🟦", "🟩", "🟦"]
    picked_pieces = board.pick_piece("C", "U")
    assert picked_pieces == ["🟦", "🟦", "⬜"]
    assert board.center == ["🟩"]


def test_validate_and_convert_piece():
    board = GameBoard(2)
    assert board._validate_and_convert_piece("U") == "🟦"
    assert board._validate_and_convert_piece("u") == "🟦"

    with pytest.raises(ValueError):
        board._validate_and_convert_piece("Z")


def test_remove_all_occurrences():
    board = GameBoard(2)
    collection = ["🟦", "🟩", "🟦", "🟧"]
    removed_items = board._remove_all_occurrences(collection, "🟦")
    assert removed_items == ["🟦", "🟦"]
    assert collection == ["🟩", "🟧"]


def test_pick_piece_invalid_store_index():
    board = GameBoard(2)
    with pytest.raises(IndexError):
        board.pick_piece(10, "U")


def test_pick_piece_invalid_piece_in_store():
    board = GameBoard(2)
    board.stores[0] = ["🟦", "🟥", "⬛"]
    with pytest.raises(ValueError):
        board.pick_piece(0, "G")


def test_pick_piece_invalid_piece_in_center():
    board = GameBoard(2)
    board.center = ["🟦", "🟥", "⬛"]
    with pytest.raises(ValueError):
        board.pick_piece("C", "G")
