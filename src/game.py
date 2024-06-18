import copy
import os
import random

from gameboard import GameBoard
from playerboard import PlayerBoard
from ai.minmax import MinMaxPlayer
from util import print_boards


class Game:
    INITIAL_PIECES = ["🟥", "⬛", "🟩", "🟧", "🟦"]
    PIECES_PER_TYPE = 20
    MINIMUM_PIECES_IN_BAG = 4
    HISTORY = []

    def __init__(self, qtd_players=2) -> None:
        self.bag = self.INITIAL_PIECES * self.PIECES_PER_TYPE
        self.used_pieces = []
        self.players = [PlayerBoard() for _ in range(qtd_players)]
        self.current_player = 0
        self.game_board = GameBoard(qtd_players)

    def start(self) -> None:
        random.shuffle(self.bag)
        self.game_board.distribute_pieces(self.bag)

    def turn_select(self, pick) -> None:
        if not self._validate_pick_input(pick):
            raise ValueError("Invalid Pick")

        store_index, piece = self._parse_pick_input(pick)
        picked = self.game_board.pick_piece(store_index, piece)

        return picked

    def turn_placement(self) -> list:
        used_pieces = []
        for player in self.players:
            filled_lines = player.check_tower()
            for line in filled_lines:
                used_pieces.extend(player.build_tower[line][1:])
                player.fill_board(line)
            if player.check_end_game():
                player.score += player.calculate_bonus_points()
        return used_pieces

    def all_stores_empty(self) -> bool:
        return (
            all(not store for store in self.game_board.stores)
            and not self.game_board.center
        )

    def find_starting_player(self) -> int:
        for i, player in enumerate(self.players):
            if "⬜" in player.broken_pieces:
                return i
        return 0

    def play_game(self) -> None:
        self.start()
        while not self.check_end_game():
            while not self.all_stores_empty():
                self._update_display()
                state = {
                    "player": self.current_player,
                    "p1_score": copy.deepcopy(self.players[0].score),
                    "p2_score": copy.deepcopy(self.players[1].score),
                    "build_tower": copy.deepcopy(
                        self.players[self.current_player].build_tower
                    ),
                    "board": copy.deepcopy(self.players[self.current_player].board),
                    "broken": copy.deepcopy(
                        self.players[self.current_player].broken_pieces
                    ),
                    "stores": copy.deepcopy(self.game_board.stores),
                    "center": copy.deepcopy(self.game_board.center),
                }
                pick = input(
                    "Pick a Piece | EX: (5U for U in Store 5, CU for U in Center): "
                )
                was_picked = False
                while not was_picked:
                    try:
                        picked = self.turn_select(pick)
                        was_picked = True
                    except ValueError as e:
                        print(e)

                player = self.players[self.current_player]
                place_lines = []
                while picked:
                    self._update_display(picked)
                    line = input("Place pieces in the tower (line number): ")
                    picked = player.place_pieces_tower(picked, line)
                    place_lines.append(line)
                state["pick"] = pick
                state["place_lines"] = place_lines
                self.HISTORY.append(state)
                self._advance_turn()
            self.used_pieces.extend(self.turn_placement())
            self.current_player = self.find_starting_player()
            self._refill_bag_if_needed()
            self.game_board.distribute_pieces(self.bag)
        self._end_game()
        
    def play_game_ai(self) -> None:
        self.start()
        AI_INDEX = 1
        AI_PLAYER = MinMaxPlayer(3, AI_INDEX)
        while not any(player.check_end_game() for player in self.players):
            while not self.all_stores_empty():
                self._update_display()
                if self.current_player != AI_INDEX:
                    pick = input(
                    "Pick a Piece | EX: (5U for U in Store 5, CU for U in Center): "
                    )
                    was_picked = False
                    while not was_picked:
                        try:
                            picked = self.turn_select(pick)
                            was_picked = True
                        except ValueError as e:
                            print(e)

                    player = self.players[self.current_player]
                    while picked:
                        self._update_display(picked)
                        line = input("Place pieces in the tower (line number): ")
                        picked = player.place_pieces_tower(picked, line)
                    self._advance_turn()
                else:
                    best_move = AI_PLAYER.get_best_move_2(self)
                    print(best_move)
                    # picked = self.turn_select(best_move[0])
                    # player = self.players[self.current_player]
                    # while picked:
                    #     player.place_pieces_tower(picked, best_move[1])
                    # self._advance_turn()
                    
            

    def undo_move(self):
        game_status = self.HISTORY[-1]
        self.current_player = game_status["player"]
        self.players[0].score = game_status["p1_score"]
        self.players[1].score = game_status["p2_score"]
        self.players[self.current_player].build_tower = game_status["build_tower"]
        self.players[self.current_player].board = game_status["board"]
        self.players[self.current_player].broken_pieces = game_status["broken"]
        self.game_board.stores = game_status["stores"]
        self.game_board.center = game_status["center"]
        
    def check_end_game(self):
        return any(player.check_end_game() for player in self.players)

    def _update_display(self, picked=None) -> None:
        #self._clear_screen()
        self._display_game_status()
        self._display_turn_info()
        if picked:
            self._display_remain_pieces_to_place(picked)

    def _display_remain_pieces_to_place(self, picked) -> None:
        print(f"{' ' * (50 - len(picked))}To be placed: {' '.join(picked)}")
        print("-" * 115)

    def _clear_screen(self) -> None:
        os.system("clear" if os.name == "nt" else "printf '\033c'")

    def _display_game_status(self) -> None:
        print(
            f"QTY Pieces in Bag: {len(self.bag)} | QTY Pieces Used: {len(self.used_pieces)}"
        )
        print_boards(self.game_board, *self.players)

    def _refill_bag_if_needed(self) -> None:
        if len(self.bag) < self.MINIMUM_PIECES_IN_BAG * len(self.game_board.stores):
            self.bag.extend(self.used_pieces)
            random.shuffle(self.bag)

    def _end_game(self) -> None:
        print("Game Over")
        for i, player in enumerate(self.players):
            print(f"Player {i + 1} score: {player.score}")

    def _display_turn_info(self) -> None:
        print(f"Player {self.current_player + 1}")
        print(
            "Color Codes: R=🟥, B=⬛, G=🟩, Y=🟧, U=🟦, X=⬜ | Extra Line Codes: B=Broken Line"
        )
        print("-" * 115)

    def _validate_pick_input(self, pick: str) -> bool:
        return len(pick) >= 2 and (pick[0].isdigit() or pick[0].upper() == "C")

    def _parse_pick_input(self, pick: str) -> tuple:
        store_index = pick[0].upper()
        piece = pick[1].upper()
        if store_index != "C":
            store_index = int(store_index)
        return store_index, piece

    def _advance_turn(self) -> None:
        print("-" * 20)
        self.current_player = (self.current_player + 1) % len(self.players)
