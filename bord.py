import random

pieces = ['R', 'B' , 'L' , 'Y' , 'U' ]


class PlayerBoard:
    
    def __init__(self) -> None:
        self.board = [
            [ ('U', 0), ('Y', 0), ('R', 0), ('B', 0), ('L', 0)],
            [ ('L', 0), ('U', 0), ('Y', 0), ('R', 0), ('B', 0)],
            [ ('B', 0), ('L', 0), ('U', 0), ('Y', 0), ('R', 0)],
            [ ('R', 0), ('B', 0), ('L', 0), ('U', 0), ('Y', 0)],
            [ ('Y', 0), ('R', 0), ('B', 0), ('L', 0), ('U', 0)],
            
        ]
        self.build_tower = [
            [None],
            [ None, None],
            [ None, None, None],
            [ None, None, None, None],
            [ None, None, None, None, None],
        ]
        
        self.broken_pieces = []
        self.score = 0
        
    def place_pieces_tower(self, pieces: list, line: int) -> list:
        if 'X' in pieces:
            self.broken_pieces.append('X')
            pieces.remove('X')
        
        if set(self.build_tower[line]) != { None } and set(self.build_tower[line]) != set(pieces + [None]):
            print('Invalid Placement!')
            return pieces
        
        for i in range(len(self.build_tower[line])):
            try:
                self.build_tower[line][i] = pieces.pop(0)
            except IndexError:
                break
        
        return pieces[i:]
    
    def print_tower(self) -> None:
        for i, line in enumerate(self.build_tower):
            print(f'{i} | {line}')
            
    def print_board(self) -> None:
        for i, line in enumerate(self.board):
            print(f'| {[ p+str(d) for p, d in line]} |')
            
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
        return [ i for i, line in enumerate(self.build_tower) if None not in line]    

class GameBoard:
    
    def __init__(self, qtd_players) -> None:
        stores_qtd = { 2: 5, 3: 7, 4: 9}
        self.center = ['X']
        self.stores = [ [] for _ in range(stores_qtd[qtd_players])]
        
    def distribute_pieces(self, pieces) -> None:
        for store in self.stores:
            for _ in range(4):
                store.append(pieces.pop())
    
    def pick_piece(self, store_index: int, piece: str) -> list:
        piece = piece.upper()
        
        if piece not in self.stores[store_index]:
            raise ValueError('Piece not in store')
        
        picked = []
        if store_index != 'C':
            while piece in self.stores[store_index]:
                picked.append(self.stores[store_index].pop(self.stores[store_index].index(piece)))
            self.center.extend(self.stores[store_index])
            self.stores[store_index] = []
        else:
            while piece in self.center:
                if 'X' in self.center:
                    picked.append('X')
                    self.center.remove('X')
                picked.append(self.center.pop())
                
        return picked
    
            
    def print_board(self) -> None:
        for i, store in enumerate(self.stores):
            print(f'{i} | {store}')
            
        print('C |', self.center)
                
        
class Game:
    
    def __init__(self, qtd_players = 2) -> None:
        self.bag = [ *pieces * 20]
        self.players = [ PlayerBoard() for _ in range(qtd_players)]
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
        pick = input('Pick a Piece | EX: (5U for U in Store 5): ')
        if len(pick) != 2:
            print('Invalid Input')
            return self.turn()
        
        store_index, piece = pick
        store_index = int(store_index)
        picked = self.game_board.pick_piece(store_index, piece)
        print('- ' * 20)
        print(f'Picked: {picked}')
        print('- ' * 20)
        
        while picked:
            player.print_tower()
            line = input(f'Place {picked} in the tower | EX: (1): ')
            picked = player.place_pieces_tower(picked, int(line))
            
        print('- ' * 20)
        self.current_player = (self.current_player + 1) % len(self.players)
        
    def turn_placement(self) -> None:
        player = self.players[self.current_player]
        print(f'Player {self.current_player + 1}')
        print('- ' * 20)
        player.print_tower()
        filled = player.check_tower()
        print('- ' * 20)
        print(filled)
        player.print_board()
        for line in filled:
            player.fill_board(line)
        print()
        print('- ' * 20)
            
        player.print_board()
        if player.check_end_game():
            player.score += player.calculate_bonus_points()
            
    
        
        
if __name__ == '__main__':
    game = Game()
    game.start()
    #game.turn_select()
    game.turn_placement()
    