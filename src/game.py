import random

from gameboard import GameBoard
from playerboard import PlayerBoard


class Game:
    def __init__(self, qtd_players=2) -> None:
        self.pieces = ['R', 'B', 'L', 'Y', 'U']
        self.bag = self.pieces * 20
        self.players = [PlayerBoard() for _ in range(qtd_players)]
        self.current_player = 0
        self.game_board = GameBoard(qtd_players)

    def start(self) -> None:
        random.shuffle(self.bag)
        self.game_board.distribute_pieces(self.bag)

    def turn_select(self) -> None:
        player = self.players[self.current_player]
        print(f'Player {self.current_player + 1}')
        print('-' * 20)
        self.game_board.print_board()
        pick = input('Pick a Piece | EX: (5U for U in Store 5, CU for U in Center): ')
        if len(pick) < 2 or (pick[0] != 'C' and not pick[0].isdigit()):
            print('Invalid Input')
            return self.turn_select()

        store_index = pick[0]
        piece = pick[1]

        if store_index != 'C':
            store_index = int(store_index)

        try:
            picked = self.game_board.pick_piece(store_index, piece)
        except ValueError as e:
            print(e)
            return self.turn_select()

        print('-' * 20)
        print(f'Picked: {picked}')
        print('-' * 20)

        while picked:
            player.print_tower()
            line = input(f'Place pieces in the tower (line number): ')
            try:
                line = int(line)
                picked = player.place_pieces_tower(picked, line)
            except ValueError:
                print('Invalid line number')
            except IndexError:
                print('Invalid line number')

        print('-' * 20)
        self.current_player = (self.current_player + 1) % len(self.players)

    def turn_placement(self) -> None:
        player = self.players[self.current_player]
        print(f'Player {self.current_player + 1}')
        print('-' * 20)
        player.print_tower()
        filled = player.check_tower()
        print('-' * 20)
        print(f'Filled lines: {filled}')
        player.print_board()
        for line in filled:
            player.fill_board(line)
        print()
        print('-' * 20)
        player.print_board()
        if player.check_end_game():
            player.score += player.calculate_bonus_points()

    def all_stores_empty(self) -> bool:
        return all(not store for store in self.game_board.stores) and not self.game_board.center

    def find_starting_player(self) -> int:
        for i, player in enumerate(self.players):
            if 'X' in player.broken_pieces:
                return i
        return 0

    def play_game(self) -> None:
        self.start()
        while not any(player.check_end_game() for player in self.players):
            while not self.all_stores_empty():
                self.turn_select()
            for _ in range(len(self.players)):
                self.turn_placement()
            self.current_player = self.find_starting_player()
            if len(self.bag) < 4 * len(self.game_board.stores):
                self.bag.extend(self.pieces * 20)
                random.shuffle(self.bag)
            self.game_board.distribute_pieces(self.bag)
        print('Game Over')
        for i, player in enumerate(self.players):
            print(f'Player {i + 1} score: {player.score}')