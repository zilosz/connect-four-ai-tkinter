from slot import Slot


class Board:

    def __init__(self, rows: int, columns: int) -> None:
        self.rows = rows
        self.columns = columns
        self.last_played_coordinate = None
        self.colors = [[Slot.EMPTY_COLOR] * columns for _ in range(rows)]

    def center_column(self) -> int:
        return self.columns // 2

    def is_column_open(self, column: int) -> bool:
        return self.colors[0][column] == Slot.EMPTY_COLOR

    def get_drop_row_in_column(self, column: int) -> int:

        for row in range(self.rows - 1, -1, -1):

            if self.colors[row][column] == Slot.EMPTY_COLOR:
                return row

    def drop_piece_in_column(self, column: int, piece_color: str) -> None:
        lowest_row = self.get_drop_row_in_column(column)
        self.colors[lowest_row][column] = piece_color
        self.last_played_coordinate = (lowest_row, column)

    def get_open_columns(self) -> list[int]:
        return [col for col in range(self.columns) if self.is_column_open(col)]

    def find_winning_piece_coordinates(
            self,
            piece_row: int,
            piece_column: int,
            connect_amount: int
            ) -> list[tuple[int, int]]:

        winning_coordinates = []
        color = self.colors[piece_row][piece_column]
        horizontal_coordinates = []
        column = piece_column

        while column >= 0 and self.colors[piece_row][column] == color:
            horizontal_coordinates.append((piece_row, column))
            column -= 1

        column = piece_column + 1

        while column < self.columns and self.colors[piece_row][column] == color:
            horizontal_coordinates.append((piece_row, column))
            column += 1

        if len(horizontal_coordinates) >= connect_amount:
            winning_coordinates += horizontal_coordinates

        vertical_coordinates = []
        row = piece_row

        while row >= 0 and self.colors[row][piece_column] == color:
            vertical_coordinates.append((row, piece_column))
            row -= 1

        row = piece_row + 1

        while row < self.rows and self.colors[row][piece_column] == color:
            vertical_coordinates.append((row, piece_column))
            row += 1

        if len(vertical_coordinates) >= connect_amount:
            winning_coordinates += vertical_coordinates

        back_diagonal_coordinates = []
        row = piece_row
        column = piece_column

        while row >= 0 and column >= 0 and self.colors[row][column] == color:
            back_diagonal_coordinates.append((row, column))
            row -= 1
            column -= 1

        row = piece_row + 1
        column = piece_column + 1

        while row < self.rows \
                and column < self.columns \
                and self.colors[row][column] == color:

            back_diagonal_coordinates.append((row, column))
            row += 1
            column += 1

        if len(back_diagonal_coordinates) >= connect_amount:
            winning_coordinates += back_diagonal_coordinates

        front_diagonal_coordinates = []
        row = piece_row
        column = piece_column

        while row >= 0 \
                and column < self.columns \
                and self.colors[row][column] == color:

            front_diagonal_coordinates.append((row, column))
            row -= 1
            column += 1

        row = piece_row + 1
        column = piece_column - 1

        while row < self.rows \
                and column >= 0 \
                and self.colors[row][column] == color:
            front_diagonal_coordinates.append((row, column))
            row += 1
            column -= 1

        if len(front_diagonal_coordinates) >= connect_amount:
            winning_coordinates += front_diagonal_coordinates

        return winning_coordinates

    def has_piece_been_played(self) -> bool:
        return self.last_played_coordinate is not None

    def has_last_move_won_game(self, connect_amount: int) -> bool:
        return len(self.find_winning_piece_coordinates(
                *self.last_played_coordinate, connect_amount)) >= connect_amount

    def is_full(self) -> bool:

        for row in self.colors:

            for color in row:

                if color == Slot.EMPTY_COLOR:
                    return False

        return True
