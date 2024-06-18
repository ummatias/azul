import copy

import os
class MinMaxPlayer:
    
    def __init__(self, depth: int, ai_player_index: int) -> None:
        self.depth = depth
        self.player = ai_player_index
        self.c = 0
    def minmax(self, game, depth: int, is_maximizing_player: bool):
        if self.depth == 0 or game.check_end_game():
            return game.players[self.player].score
        self.c+=1
        possible_picks = game.game_board.get_possible_moves()
        if is_maximizing_player:
            print()
            print("SIMULATING MAX PLAYER")
            best_value = float("-inf")
            for pick in possible_picks:
                game_copy = copy.deepcopy(game)
                print("-" * 50)
                for store in game_copy.game_board.stores:
                    print(store)
                print(game_copy.game_board.center)
                print("-" * 50)
                picked_pieces = game_copy.turn_select(f"{pick[0]}{pick[1]}")
                print(f"MAX PLAYER CHOSE: {pick}")
                print(f"MAX PLAYER PICKED: {picked_pieces}")
                player_copy = copy.deepcopy(game_copy.players[self.player])
                places_to_play = player_copy.get_possible_moves(picked_pieces)
                print(f"MAX PLAYER PLACES TO PLAY:", places_to_play)
                for places in places_to_play:
                    game_copy_2 = copy.deepcopy(game_copy)
                    player_copy_2 = copy.deepcopy(player_copy)
                    print(f"MAX PLAYER - Gonna {places}")
                    for place in places:
                        print("*" * 50)
                        print(f"MAX PLAYER - Placing {picked_pieces} in line {place}")
                        picked_pieces = player_copy_2.place_pieces_tower(picked_pieces, place)
                        for i in player_copy_2.build_tower:
                            print(i)
                        print("*" * 50)
                    game_copy_2.players[self.player] = player_copy_2
                    game_copy_2._advance_turn()
                    value = self.minmax(game_copy_2, depth - 1, False)
                    best_value = max(best_value, value)
            return best_value
        else:
            print()
            print("SIMULATING MIN PLAYER")
            best_value = float("inf")
            for pick in possible_picks:
                game_copy = copy.deepcopy(game)
                print("-" * 50)
                for store in game_copy.game_board.stores:
                    print(store)
                print(game_copy.game_board.center)
                print("-" * 50)
                picked_pieces = game_copy.turn_select(f"{pick[0]}{pick[1]}")
                print(f"MIN PLAYER CHOSE: {pick}")
                print(f"MIN PLAYER PICKED: {picked_pieces}")
                # not the self.player
                player_copy = copy.deepcopy(game_copy.players[0 if self.player == 1 else 1])
                places_to_play = player_copy.get_possible_moves(picked_pieces)
                print(f"MIN PLAYER PLACES TO PLAY:", places_to_play)
                for places in places_to_play:
                    game_copy_2 = copy.deepcopy(game_copy)
                    player_copy_2 = copy.deepcopy(player_copy)
                    print(f"MIN PLAYER - Gonna {places}")
                    for place in places:
                        print("*" * 50)
                        print(f"MIN PLAYER - Placing {picked_pieces} in line {place}")
                        picked_pieces = player_copy_2.place_pieces_tower(picked_pieces, place)
                        for i in player_copy_2.build_tower:
                            print(i)
                        print("*" * 50)
                    game_copy_2.players[0 if self.player == 1 else 1] = player_copy_2
                    game_copy_2._advance_turn()
                    value = self.minmax(game_copy_2, depth - 1, True)
                    best_value = min(best_value, value)
            return best_value
        
    def _clear_screen(self) -> None:
        os.system("clear" if os.name == "nt" else "printf '\033c'")

    def get_best_move(self, game):
        print("*" * 50)
        print("SIMULATING MAX PLAYER")
        best_value = float("-inf")
        best_move = None
        c = 0
        possible_picks = game.game_board.get_possible_moves()
        for pick in possible_picks:
            self._clear_screen()
            c+=1
            game_copy = copy.deepcopy(game)
            print("-" * 50)
            for store in game_copy.game_board.stores:
                print(store)
            print(game_copy.game_board.center)
            print("-" * 50)
            print(f"MAX PLAYER CHOSE: {pick}")
            picked_pieces = game_copy.turn_select(f"{pick[0]}{pick[1]}")
            print(f"MAX PLAYER PICKED: {picked_pieces}")
            player_copy = copy.deepcopy(game_copy.players[self.player])
            places_to_play = player_copy.get_possible_moves(picked_pieces)
            print(f"MIN PLAYER PLACES TO PLAY:", places_to_play)
            for places in places_to_play:
                game_copy_2 = copy.deepcopy(game_copy)
                player_copy_2 = copy.deepcopy(game_copy.players[self.player])
                print(f"MAX PLAYER - Gonna {places}")
                for place in places:
                    
                    print(f"MIN PLAYER - Placing {picked_pieces} in line {place}")
                    picked_pieces = player_copy_2.place_pieces_tower(picked_pieces, place)
                    print("*" * 50)
                game._advance_turn()
    
                value = self.minmax(game_copy_2, self.depth, False)
                print(f"Value: {value}")
                if value > best_value:
                    best_value = value
                    best_move = pick
        return best_move
    
                    
    def get_best_move_2(self, game):
        best_move = None
        best_value = float("-inf")
        possible_picks = game.game_board.get_possible_moves()
        print("*" * 50)
        print("SIMULATING MAX PLAYER")
        for pick in possible_picks:
            
            game_copy = copy.deepcopy(game)
            print("-" * 50)
            for store in game_copy.game_board.stores:
                print(store)
            print(game_copy.game_board.center)
            print(f"MAX PLAYER CHOSE: {pick}")
            picked_pieces = game_copy.turn_select(f"{pick[0]}{pick[1]}")
            print(f"MAX PLAYER PICKED: {picked_pieces}")
            player_copy = copy.deepcopy(game_copy.players[self.player])
            
            places_to_play = player_copy.get_possible_moves(picked_pieces)
            print(f"MAX PLAYER PLACES TO PLAY:", places_to_play)
            for places in places_to_play:
                game_copy_2 = copy.deepcopy(game_copy)
                player_copy_2 = copy.deepcopy(player_copy)
                for place in places:
                    print(f"MAX PLAYER - Placing {picked_pieces} in line {place}")
                    picked_pieces = player_copy_2.place_pieces_tower(picked_pieces, place)
                    for i in player_copy_2.build_tower:
                        print(i)
                    print("*" * 50)
                game_copy_2.players[self.player] = player_copy_2
                game_copy_2._advance_turn()
                move_value = self.minmax(game_copy_2, self.depth - 1, False)
                if move_value > best_value:
                    best_value = move_value
                    best_move = (pick, places)

        return best_move
                
            
                
                
                
                