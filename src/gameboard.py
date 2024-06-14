class GameBoard:
    def __init__(self, qtd_players) -> None:
        stores_qtd = {2: 5, 3: 7, 4: 9}
        self.center = ["⬜"]
        self.stores = [[] for _ in range(stores_qtd[qtd_players])]

    def distribute_pieces(self, pieces) -> None:
        for store in self.stores:
            for _ in range(4):
                store.append(pieces.pop())

    def pick_piece(self, store_index: int, piece: str) -> list:
        piece = piece.upper()
        if not store_index.isdigit():
            store_index = store_index.upper()

        if store_index != "C":
            if piece not in self.stores[store_index]:
                raise ValueError("Piece not in store")

            picked = []
            while piece in self.stores[store_index]:
                picked.append(
                    self.stores[store_index].pop(self.stores[store_index].index(piece))
                )
            self.center.extend(self.stores[store_index])
            self.stores[store_index] = []
        else:
            if piece not in self.center:
                raise ValueError("Piece not in center")

            picked = []
            while piece in self.center:
                picked.append(self.center.pop(self.center.index(piece)))
            if "⬜" in self.center:
                picked.append("⬜")
                self.center.remove("⬜")

        return picked
