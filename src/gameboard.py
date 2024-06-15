class GameBoard:
    PIECE_DICT = {
        "U": "🟦",
        "R": "🟥",
        "B": "⬛",
        "G": "🟩",
        "Y": "🟧",
        "X": "⬜",
    }
    CENTER_INITIAL = ["⬜"]
    STORE_SIZES = {2: 5, 3: 7, 4: 9}
    PIECES_PER_STORE = 4

    def __init__(self, qtd_players) -> None:
        self.center = self.CENTER_INITIAL.copy()
        self.stores = [[] for _ in range(self.STORE_SIZES[qtd_players])]

    def distribute_pieces(self, pieces) -> None:
        for store in self.stores:
            store.extend(self._draw_pieces(pieces, self.PIECES_PER_STORE))
        self.center = self.CENTER_INITIAL.copy()

    def _draw_pieces(self, pieces: list, count: int) -> list:
        drawn_pieces = []
        for _ in range(count):
            drawn_pieces.append(pieces.pop())
        return drawn_pieces

    def pick_piece(self, store_index, piece: str) -> list:
        piece = self._validate_and_convert_piece(piece)

        if store_index.lower() == "c":
            return self._pick_from_center(piece)
        else:
            return self._pick_from_store(store_index, piece)

    def _validate_and_convert_piece(self, piece: str) -> str:
        piece = piece.upper()
        if piece not in self.PIECE_DICT:
            raise ValueError("Invalid piece")
        return self.PIECE_DICT[piece]

    def _pick_from_store(self, store_index: int, piece: str) -> list:
        if piece not in self.stores[store_index]:
            raise ValueError("Piece not in store")

        picked_pieces = self._remove_all_occurrences(self.stores[store_index], piece)
        self.center.extend(self.stores[store_index])
        self.stores[store_index] = []
        return picked_pieces

    def _pick_from_center(self, piece: str) -> list:
        if piece not in self.center:
            raise ValueError("Piece not in center")

        picked_pieces = self._remove_all_occurrences(self.center, piece)
        if "⬜" in self.center:
            picked_pieces.append("⬜")
            self.center.remove("⬜")
        return picked_pieces

    def _remove_all_occurrences(self, collection: list, item: str) -> list:
        occurrences = [i for i in collection if i == item]
        collection[:] = [i for i in collection if i != item]
        return occurrences
