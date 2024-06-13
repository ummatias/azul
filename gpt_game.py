import random

pieces = ['R', 'B', 'L', 'Y', 'U']

class PlayerBoard:
    def __init__(self) -> None:
        self.board = [
            [('U', 0), ('Y', 0), ('R', 0), ('B', 0), ('L', 0)],
            [('L', 0), ('U', 0), ('Y', 0), ('R', 0), ('B', 0)],
            [('B', 0), ('L', 0), ('U', 0), ('Y', 0), ('R', 0)],
            [('R', 0), ('B', 0), ('L', 0), ('U', 0), ('Y', 0)],
            [('Y', 0), ('R', 0), ('B', 0), ('L', 0), ('U', 0)],
        ]
        self.build_tower = [
            [None],
            [None, None],
            [None, None, None],
            [None, None, None, None],
            [None, None, None, None, None],
        ]
        self.broken_pieces = []
        self.score = 0
        self.penalties = [-1, -1, -2, -2, -2, -3, -3]

    def place_pieces_tower(self, pieces: list, line: int) -> list:
        piece_type = pieces[0]
        # Check if the piece is already on the wall for this line
        if piece_type in [p for p, filled in self.board[line] if filled == 1]:
            print('Invalid Placement! Piece already on the wall.')
            self.broken_pieces.extend(pieces)
            self.update_score_with_penalties()
            return []

        # Place pieces in the build tower line
        for i in range(len(self.build_tower[line])):
            if self.build_tower[line][i] is None:
                self.build_tower[line][i] = piece_type
                pieces.pop(0)
                if not pieces:
                    break

        # Any remaining pieces go to broken pieces
        if pieces:
            self.broken_pieces.extend(pieces)
            self.update_score_with_penalties()

        return pieces

    def add_to_broken_pieces(self, piece) -> None:
        if len(self.broken_pieces) < 7:
            self.broken_pieces.append(piece)
            self.score += self.penalties[len(self.broken_pieces) - 1]
        else:
            print(f"Piece {piece} discarded as broken pieces limit reached.")

    def update_score_with_penalties(self) -> None:
        while len(self.broken_pieces) > 7:
            self.broken_pieces.pop()
        self.score += sum(self.penalties[:len(self.broken_pieces)])

    def print_tower(self) -> None:
        for i, line in enumerate(self.build_tower):
            print(f'{i} | {line}')

    def print_board(self) -> None:
        for i, line in enumerate(self.board):
            print(f'| {[p + str(d) for p, d in line]} |')

    def fill(self, nt):
        self.build_tower = nt

    def fill_board(self, line) -> None:
        for i, (p, filled) in enumerate(self.board[line]):
            if p == self.build_tower[line][0] and filled == 0:
                self.board[line][i] = (self.build_tower[line][0], 1)
                self.score += self.calculate_points(line, i)
                self.build_tower[line] = [None for _ in range(line + 1)]
                return

    def calculate_points(self, row, col) -> int:
        points = 1  # Start with the piece itself

        # Check horizontally
        for j in range(col - 1, -1, -1):
            if self.board[row][j][1] == 1:
                points += 1
            else:
                break
        for j in range(col + 1, len(self.board[row])):
            if self.board[row][j][1] == 1:
                points += 1
            else:
                break

        # Check vertically
        for i in range(row - 1, -1, -1):
            if self.board[i][col][1] == 1:
                points += 1
            else:
                break
        for i in range(row + 1, len(self.board)):
            if self.board[i][col][1] == 1:
                points += 1
            else:
                break

        return points

    def calculate_bonus_points(self) -> int:
        bonus_points = 0

        # Check for completed horizontal lines
        for row in self.board:
            if all(filled == 1 for _, filled in row):
                bonus_points += 2

        # Check for completed vertical lines
        for col in range(len(self.board[0])):
            if all(self.board[row][col][1] == 1 for row in range(len(self.board))):
                bonus_points += 7

        # Check for 5 pieces set completed
        piece_counts = {}
        for row in self.board:
            for piece, filled in row:
                if filled == 1:
                    if piece not in piece_counts:
                        piece_counts[piece] = 0
                    piece_counts[piece] += 1

        for count in piece_counts.values():
            if count == 5:
                bonus_points += 10

        return bonus_points

    def check_end_game(self) -> bool:
        for row in self.board:
            if all(filled == 1 for _, filled in row):
                return True
        return False

    def check_tower(self) -> list:
        return [i for i, line in enumerate(self.build_tower) if None not in line]


class GameBoard:
    def __init__(self, qtd_players) -> None:
        stores_qtd = {2: 5, 3: 7, 4: 9}
        self.center = ['X']
        self.stores = [[] for _ in range(stores_qtd[qtd_players])]

    def distribute_pieces(self, pieces) -> None:
        for store in self.stores:
            for _ in range(4):
                store.append(pieces.pop())

    def pick_piece(self, store_index: int, piece: str) -> list:
        piece = piece.upper()

        if store_index != 'C':
            if piece not in self.stores[store_index]:
                raise ValueError('Piece not in store')

            picked = []
            while piece in self.stores[store_index]:
                picked.append(self.stores[store_index].pop(self.stores[store_index].index(piece)))
            self.center.extend(self.stores[store_index])
            self.stores[store_index] = []
        else:
            if piece not in self.center:
                raise ValueError('Piece not in center')

            picked = []
            while piece in self.center:
                picked.append(self.center.pop(self.center.index(piece)))
            if 'X' in self.center:
                picked.append('X')
                self.center.remove('X')

        return picked

    def print_board(self) -> None:
        for i, store in enumerate(self.stores):
            print(f'{i} | {store}')
        print('C |', self.center)


class Game:
    def __init__(self, qtd_players=2) -> None:
        self.bag = pieces * 20
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

        if store_index == 'C':
            store_index = 'C'
        else:
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
                self.bag.extend(pieces * 20)
                random.shuffle(self.bag)
            self.game_board.distribute_pieces(self.bag)
        print('Game Over')
        for i, player in enumerate(self.players):
            print(f'Player {i + 1} score: {player.score}')

if __name__ == "__main__":
    game = Game(qtd_players=2)
    game.play_game()