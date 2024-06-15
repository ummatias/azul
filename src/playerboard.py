class PlayerBoard:
    def __init__(self) -> None:
        self.board = [
            [("🟦", 0), ("🟧", 0), ("🟥", 0), ("⬛", 0), ("🟩", 0)],
            [("🟩", 0), ("🟦", 0), ("🟧", 0), ("🟥", 0), ("⬛", 0)],
            [("⬛", 0), ("🟩", 0), ("🟦", 0), ("🟧", 0), ("🟥", 0)],
            [("🟥", 0), ("⬛", 0), ("🟩", 0), ("🟦", 0), ("🟧", 0)],
            [("🟧", 0), ("🟥", 0), ("⬛", 0), ("🟩", 0), ("🟦", 0)],
        ]
        self.build_tower = [
            [None],
            [None, None],
            [None, None, None],
            [None, None, None, None],
            [None, None, None, None, None],
        ]
        self.broken_pieces = [None, None, None, None, None, None, None]
        self.score = 0
        self.penalties = [-1, -1, -2, -2, -2, -3, -3]

    def place_pieces_tower(
        self,
        pieces: list,
        line,
    ) -> list:
        if "⬜" in pieces:
            self.add_to_broken_pieces("⬜")
            pieces.remove("⬜")

        piece_type = pieces[0]

        if line == "B" or line == "b":
            for piece in pieces:
                self.add_to_broken_pieces(piece)
            return []

        line = int(line)
        if line < 0 or line >= len(self.build_tower):
            raise ValueError("Invalid Line Number")

        if (
            set(self.build_tower[line]) != {None}
            and piece_type not in self.build_tower[line]
        ):
            print("Invalid Placement! This line is filled with another tile.")
            return pieces

        # Check if has any line with empty space
        if None not in self.build_tower[line]:
            print("Invalid Placement! No empty space in the line.")
            return pieces

        # Check if the piece is already on the wall for this line
        if piece_type in [p for p, filled in self.board[line] if filled == 1]:
            print("Invalid Placement! Piece already on the wall.")
            return pieces

        # Place pieces in the build tower line
        for i in range(len(self.build_tower[line])):
            if self.build_tower[line][i] is None:
                self.build_tower[line][i] = piece_type
                pieces.pop(0)
                if not pieces:
                    break
        return pieces

    def add_to_broken_pieces(self, piece) -> None:
        if None in self.broken_pieces:
            self.broken_pieces[self.broken_pieces.index(None)] = piece
        else:
            print(f"Piece {piece} discarded as broken pieces limit reached.")

    def calculate_penalties(self) -> int:
        penality = 0
        for i in range(len(self.broken_pieces)):
            if self.broken_pieces[i] is not None:
                penality += self.penalties[i]
                self.broken_pieces[i] = None
        return penality

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

        return points + self.calculate_penalties()

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
