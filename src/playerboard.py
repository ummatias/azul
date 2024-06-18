import copy


class PlayerBoard:
    EMPTY_TILE = None
    BROKEN_TILE_LIMIT = 7

    def __init__(self) -> None:
        self.board = [
            [("🟦", 0), ("🟧", 0), ("🟥", 0), ("⬛", 0), ("🟩", 0)],
            [("🟩", 0), ("🟦", 0), ("🟧", 0), ("🟥", 0), ("⬛", 0)],
            [("⬛", 0), ("🟩", 0), ("🟦", 0), ("🟧", 0), ("🟥", 0)],
            [("🟥", 0), ("⬛", 0), ("🟩", 0), ("🟦", 0), ("🟧", 0)],
            [("🟧", 0), ("🟥", 0), ("⬛", 0), ("🟩", 0), ("🟦", 0)],
        ]
        self.build_tower = [
            [self.EMPTY_TILE],
            [self.EMPTY_TILE, self.EMPTY_TILE],
            [self.EMPTY_TILE, self.EMPTY_TILE, self.EMPTY_TILE],
            [self.EMPTY_TILE, self.EMPTY_TILE, self.EMPTY_TILE, self.EMPTY_TILE],
            [
                self.EMPTY_TILE,
                self.EMPTY_TILE,
                self.EMPTY_TILE,
                self.EMPTY_TILE,
                self.EMPTY_TILE,
            ],
        ]
        self.broken_pieces = [self.EMPTY_TILE] * self.BROKEN_TILE_LIMIT
        self.score = 0
        self.penalties = [-1, -1, -2, -2, -2, -3, -3]

    def place_pieces_tower(self, pieces: list, line) -> list:
        pieces = self._handle_broken_piece(pieces, "⬜")
        if not pieces:
            return []

        if line == "b" or line == "B":
            self._add_all_to_broken_pieces(pieces)
            return []

        line = int(line)
        self._validate_line_number(line)
        self._validate_placement(line, pieces[0])

        pieces = self._place_pieces_in_tower(line, pieces)
        return pieces

    def _place_pieces_in_tower(self, line, pieces: list) -> list:
        for i in range(len(self.build_tower[line])):
            if self.build_tower[line][i] is self.EMPTY_TILE:
                self.build_tower[line][i] = pieces.pop(0)
                if not pieces:
                    break
        return pieces

    def get_possible_moves(self, pieces: list) -> list:

        if "⬜" in pieces:
            return []

        if not pieces:
            return []

        def backtrack(placed_pieces, remaining_pieces):
            if not remaining_pieces:
                result.append(placed_pieces[:])
                return

            for line in range(len(self.build_tower)):
                original_row = self.build_tower[line][:]
                try:
                    remaining_pieces_after_placement = self.place_pieces_tower(
                        remaining_pieces, line
                    )
                    placed_pieces.append(line)

                    if not remaining_pieces_after_placement:
                        backtrack(placed_pieces, remaining_pieces_after_placement)
                    else:
                        backtrack(placed_pieces, remaining_pieces_after_placement)

                    placed_pieces.pop()
                except ValueError:
                    pass
                finally:
                    self.build_tower[line] = original_row

        result = []
        backtrack([], pieces)
        for i in range(len(result)):
            if len(result[i]) >= 2:
                b_element = result[i][:-1] + ["B"]
                if b_element not in result:
                    result.append(b_element)
        result.sort(key=lambda x: x[0])
        result.append(["B"])
        return result

    def _handle_broken_piece(self, pieces: list, piece_type: str) -> list:
        if piece_type in pieces:
            self.add_to_broken_pieces(piece_type)
            pieces.remove(piece_type)
        return pieces

    def _add_all_to_broken_pieces(self, pieces: list) -> None:
        for piece in pieces:
            self.add_to_broken_pieces(piece)

    def _validate_line_number(self, line: int) -> None:
        if line < 0 or line >= len(self.build_tower):
            raise ValueError("Invalid Line Number")

    def _validate_placement(self, line: int, piece_type: str) -> None:
        if (
            set(self.build_tower[line]) != {self.EMPTY_TILE}
            and piece_type not in self.build_tower[line]
        ):
            raise ValueError(
                "Invalid Placement! This line is filled with another tile."
            )
        if self.EMPTY_TILE not in self.build_tower[line]:
            raise ValueError("Invalid Placement! No empty space in the line.")
        if piece_type in [p for p, filled in self.board[line] if filled == 1]:
            raise ValueError("Invalid Placement! Piece already on the wall.")

    def add_to_broken_pieces(self, piece) -> None:
        if self.EMPTY_TILE in self.broken_pieces:
            self.broken_pieces[self.broken_pieces.index(self.EMPTY_TILE)] = piece

    def calculate_penalties(self) -> int:
        penalty = 0
        for i in range(self.BROKEN_TILE_LIMIT):
            if self.broken_pieces[i] is not None:
                penalty += self.penalties[i]
                self.broken_pieces[i] = self.EMPTY_TILE
        return penalty

    def fill(self, nt):
        self.build_tower = nt

    def fill_board(self, line) -> None:
        for i, (p, filled) in enumerate(self.board[line]):
            if p == self.build_tower[line][0] and filled == 0:
                self.board[line][i] = (self.build_tower[line][0], 1)
                self.score += self.calculate_points(line, i)
                self.build_tower[line] = [self.EMPTY_TILE] * (line + 1)
                return

    def calculate_points(self, row, col) -> int:
        points = 1
        points += self._calculate_horizontal_points(row, col)
        points += self._calculate_vertical_points(row, col)
        return points + self.calculate_penalties()

    def _calculate_horizontal_points(self, row, col) -> int:
        points = 0
        points += self._count_filled_tiles(row, col, -1, 0)
        points += self._count_filled_tiles(row, col, 1, 0)
        return points

    def _calculate_vertical_points(self, row, col) -> int:
        points = 0
        points += self._count_filled_tiles(row, col, 0, -1)
        points += self._count_filled_tiles(row, col, 0, 1)
        return points

    def _count_filled_tiles(self, row, col, row_delta, col_delta) -> int:
        points = 0
        current_row, current_col = row + row_delta, col + col_delta
        while 0 <= current_row < len(self.board) and 0 <= current_col < len(
            self.board[row]
        ):
            if self.board[current_row][current_col][1] == 0:
                break
            points += 1
            current_row += row_delta
            current_col += col_delta
        return points

    def check_tower(self) -> list:
        return [
            i for i, line in enumerate(self.build_tower) if self.EMPTY_TILE not in line
        ]

    def check_end_game(self) -> bool:
        return any(all(filled for _, filled in row) for row in self.board)

    def calculate_bonus_points(self) -> int:
        bonus_points = 0
        bonus_points += self._calculate_row_bonus()
        bonus_points += self._calculate_col_bonus()
        bonus_points += self._calculate_color_bonus()
        return bonus_points

    def _calculate_row_bonus(self) -> int:
        return sum(2 for row in self.board if all(filled for _, filled in row))

    def _calculate_col_bonus(self) -> int:
        cols = len(self.board[0])
        rows = len(self.board)
        return sum(
            7
            for col in range(cols)
            if all(self.board[row][col][1] == 1 for row in range(rows))
        )

    def _calculate_color_bonus(self) -> int:
        colors = {color: 0 for color, _ in self.board[0]}
        for row in self.board:
            for color, filled in row:
                if filled == 1:
                    colors[color] += 1
        return sum(10 for count in colors.values() if count == 5)
