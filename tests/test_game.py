from unittest.mock import MagicMock, patch

import pytest

from src.game import Game
from src.gameboard import GameBoard
from src.playerboard import PlayerBoard


@pytest.fixture
def game():
    return Game(qtd_players=2)


def test_game_initialization(game):
    assert len(game.bag) == 100  # 5 types * 20 pieces each
    assert game.used_pieces == []  # No pieces used yet
    assert len(game.players) == 2  # 2 players
    assert game.current_player == 0  # Player 1 starts


def test_start_game(game):
    with patch("random.shuffle") as mock_shuffle:
        game.start()
        mock_shuffle.assert_called_once()
        assert len(game.bag) == 80  # 20 is distributed to each store
        for store in game.game_board.stores:
            assert len(store) == game.game_board.PIECES_PER_STORE
        assert len(game.bag) == 100 - (
            len(game.game_board.stores) * game.game_board.PIECES_PER_STORE
        )


def test_turn_select(game):
    game.game_board.stores = [["🟦", "🟦", "🟦", "🟦"], [], [], [], []]
    with patch("builtins.input", side_effect=["0U", "4"]):
        game.turn_select()
        assert game.current_player == 1
        assert game.players[0].build_tower[4] == ["🟦", "🟦", "🟦", "🟦", None]

    game.game_board.center = ["⬜", "🟦", "🟩"]
    with patch("builtins.input", side_effect=["CU", "2"]):
        game.turn_select()
        assert game.current_player == 0
        assert game.players[1].build_tower[2] == ["🟦", None, None]
        assert game.players[1].broken_pieces == [
            "⬜",
            None,
            None,
            None,
            None,
            None,
            None,
        ]
        assert game.game_board.center == ["🟩"]


def test_validate_pick_input(game):
    assert game._validate_pick_input("0U") is True
    assert game._validate_pick_input("CU") is True
    assert game._validate_pick_input("5R") is True
    assert game._validate_pick_input("XU") is False
    assert game._validate_pick_input("0") is False


def test_parse_pick_input(game):
    assert game._parse_pick_input("0U") == (0, "U")
    assert game._parse_pick_input("CU") == ("C", "U")
    assert game._parse_pick_input("5R") == (5, "R")


def test_advance_turn(game):
    game._advance_turn()
    assert game.current_player == 1
    game._advance_turn()
    assert game.current_player == 0  # Should cycle back to the first player


def test_turn_placement(game):
    player_mock = MagicMock()
    player_mock.check_tower.return_value = [1]
    player_mock.build_tower = {1: ["🟦", "🟦"]}

    player_mock_2 = MagicMock()
    player_mock_2.check_tower.return_value = [2]
    player_mock_2.build_tower = {2: ["🟩", "🟩", "🟩"]}

    player_mock.check_end_game.return_value = False
    game.players = [player_mock, player_mock_2]
    used_pieces = game.turn_placement()
    assert used_pieces == ["🟦", "🟩", "🟩"]
    player_mock.check_tower.assert_called()
    player_mock.fill_board.assert_called()
    player_mock.calculate_bonus_points.assert_not_called()

    player_mock.check_end_game.return_value = True
    used_pieces = game.turn_placement()
    player_mock.calculate_bonus_points.assert_called()


def test_all_stores_empty(game):
    assert game.all_stores_empty() is False
    game.game_board.stores = [[] for _ in game.game_board.stores]
    game.game_board.center = []
    assert game.all_stores_empty() is True


def test_find_starting_player(game):
    game.players[0].broken_pieces = ["⬜"]
    game.players[1].broken_pieces = []
    assert game.find_starting_player() == 0

    game.players[0].broken_pieces = []
    game.players[1].broken_pieces = ["⬜"]
    assert game.find_starting_player() == 1

    game.players[0].broken_pieces = []
    game.players[1].broken_pieces = []
    assert game.find_starting_player() == 0


def test_clear_screen(game):
    with patch("os.system") as mock_system:
        game._clear_screen()
        mock_system.assert_called_once()


def test_refill_bag_if_needed(game):
    game.bag = []
    game._refill_bag_if_needed()
    assert len(game.bag) == 100
