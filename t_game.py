import random
import tkinter as tk
from tkinter import messagebox

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


class Game:
    def __init__(self, qtd_players=2) -> None:
        self.bag = pieces * 20
        self.players = [PlayerBoard() for _ in range(qtd_players)]
        self.current_player = 0
        self.game_board = GameBoard(qtd_players)
        self.window = tk.Tk()
        self.window.title("Azul Board Game")
        self.setup_ui()

    def start(self) -> None:
        random.shuffle(self.bag)
        self.game_board.distribute_pieces(self.bag)
        self.update_ui()

    def setup_ui(self) -> None:
        self.store_frames = [tk.Frame(self.window) for _ in range(len(self.game_board.stores))]
        for i, frame in enumerate(self.store_frames):
            frame.grid(row=0, column=i, padx=10)
            tk.Label(frame, text=f'Store {i}').pack()
            for _ in range(4):
                tk.Label(frame, text='').pack()
        
        self.center_frame = tk.Frame(self.window)
        self.center_frame.grid(row=0, column=len(self.store_frames), padx=10)
        tk.Label(self.center_frame, text='Center').pack()
        for _ in range(4):
            tk.Label(self.center_frame, text='').pack()

        self.player_frames = [tk.Frame(self.window) for _ in range(len(self.players))]
        for i, frame in enumerate(self.player_frames):
            frame.grid(row=1, column=i, padx=10)
            tk.Label(frame, text=f'Player {i + 1}').pack()
            self.update_player_ui(i)

    def update_ui(self) -> None:
        for i, frame in enumerate(self.store_frames):
            for widget in frame.winfo_children()[1:]:
                widget.destroy()
            for piece in self.game_board.stores[i]:
                tk.Label(frame, text=piece).pack()
        
        for widget in self.center_frame.winfo_children()[1:]:
            widget.destroy()
        for piece in self.game_board.center:
            tk.Label(self.center_frame, text=piece).pack()

        for i in range(len(self.players)):
            self.update_player_ui(i)

    def update_player_ui(self, player_index: int) -> None:
        frame = self.player_frames[player_index]
        for widget in frame.winfo_children()[1:]:
            widget.destroy()
        
        player = self.players[player_index]
        tk.Label(frame, text=f'Score: {player.score}').pack()
        
        tower_frame = tk.Frame(frame)
        tower_frame.pack()
        for line in player.build_tower:
            tk.Label(tower_frame, text=line).pack()

        board_frame = tk.Frame(frame)
        board_frame.pack()
        for line in player.board:
            tk.Label(board_frame, text=line).pack()
        
        broken_frame = tk.Frame(frame)
        broken_frame.pack()
        tk.Label(broken_frame, text=f'Broken: {player.broken_pieces}').pack()

    def turn_select(self) -> None:
        player = self.players[self.current_player]
        messagebox.showinfo("Turn", f"Player {self.current_player + 1}'s turn")
        self.update_ui()
        pick = tk.simpledialog.askstring("Input", "Pick a Piece (e.g., 5U for U in Store 5, CU for U in Center):")
        if not pick or len(pick) < 2 or (pick[0] != 'C' and not pick[0].isdigit()):
            messagebox.showerror("Invalid Input", "Invalid Input")
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
            messagebox.showerror("Error", str(e))
            return self.turn_select()

        while picked:
            self.update_ui()
            line = tk.simpledialog.askinteger("Input", "Place pieces in the tower (line number):")
            try:
                picked = player.place_pieces_tower(picked, line)
            except ValueError:
                messagebox.showerror("Error", "Invalid line number")
            except IndexError:
                messagebox.showerror("Error", "Invalid line number")

        self.current_player = (self.current_player + 1) % len(self.players)
        self.update_ui()

    def turn_placement(self) -> None:
        player = self.players[self.current_player]
        self.update_ui()
        filled = player.check_tower()
        for line in filled:
            player.fill_board(line)
        self.update_ui()
        if player.check_end_game():
            player.score += player.calculate_bonus_points()
            messagebox.showinfo("Game Over", f"Player {self.current_player + 1} wins with {player.score} points!")

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
        messagebox.showinfo("Game Over", "Game Over")
        for i, player in enumerate(self.players):
            messagebox.showinfo(f"Player {i + 1} score", f"{player.score}")

if __name__ == "__main__":
    game = Game(qtd_players=2)
    game.play_game()
    game.window.mainloop()
