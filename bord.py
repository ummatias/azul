import random

pieces = ['R', 'B' , 'L' , 'Y' , 'U' ]


class PlayerBoard:
    
    def __init__(self) -> None:
        self.board = [
            [ None, None, None, None, None],
            [ None, None, None, None, None],
            [ None, None, None, None, None],
            [ None, None, None, None, None],
            [ None, None, None, None, None],
        ]
        self.build_tower = [
            [ None],
            [ None, None],
            [ None, None, None],
            [ None, None, None, None],
            [ None, None, None, None, None],
        ]
        
        self.broken_pieces = []
        self.points = 0
        

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
            
    def print_bord(self) -> None:
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
        
    def turn(self) -> None:
        player = self.players[self.current_player]
        print(f'Player {self.current_player + 1}')
        print('-' * 20)
        self.game_board.print_bord()
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
        
        
if __name__ == '__main__':
    game = Game()
    game.start()
    game.turn()