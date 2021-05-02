from slot import Slot


class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.last_coord = None
        self.colors = [[Slot.EMPTY_COLOR] * columns for _ in range(rows)]

    def center_column(self):
        return self.columns // 2

    def is_column_open(self, column):
        return self.colors[0][column] == Slot.EMPTY_COLOR

    def get_drop_row_in_column(self, column):

        for row in range(self.rows - 1, -1, -1):

            if self.colors[row][column] == Slot.EMPTY_COLOR:
                return row

    def drop_in_col(self, column, piece_color):
        lowest_row = self.get_drop_row_in_column(column)
        self.colors[lowest_row][column] = piece_color
        self.last_coord = (lowest_row, column)

    def open_columns(self):
        return [col for col in range(self.columns) if self.is_column_open(col)]

    def winning_coordinates(self, piece_row, piece_column, connect_amount):
        winning_coordinates = []
        color = self.colors[piece_row][piece_column]
        horizontal_coordinates = []
        c = piece_column

        while c >= 0 and self.colors[piece_row][c] == color:
            horizontal_coordinates.append((piece_row, c))
            c -= 1

        c = piece_column + 1

        while c < self.columns and self.colors[piece_row][c] == color:
            horizontal_coordinates.append((piece_row, c))
            c += 1

        if len(horizontal_coordinates) >= connect_amount:
            winning_coordinates += horizontal_coordinates

        vertical_coordinates = []
        r = piece_row

        while r >= 0 and self.colors[r][piece_column] == color:
            vertical_coordinates.append((r, piece_column))
            r -= 1

        r = piece_row + 1

        while r < self.rows and self.colors[r][piece_column] == color:
            vertical_coordinates.append((r, piece_column))
            r += 1

        if len(vertical_coordinates) >= connect_amount:
            winning_coordinates += vertical_coordinates

        back_diagonal_coordinates = []
        r = piece_row
        c = piece_column

        while r >= 0 and c >= 0 and self.colors[r][c] == color:
            back_diagonal_coordinates.append((r, c))
            r -= 1
            c -= 1

        r = piece_row + 1
        c = piece_column + 1

        while r < self.rows and c < self.columns and self.colors[r][c] == color:
            back_diagonal_coordinates.append((r, c))
            r += 1
            c += 1

        if len(back_diagonal_coordinates) >= connect_amount:
            winning_coordinates += back_diagonal_coordinates

        front_diagonal_coordinates = []
        r = piece_row
        c = piece_column

        while r >= 0 and c < self.columns and self.colors[r][c] == color:
            front_diagonal_coordinates.append((r, c))
            r -= 1
            c += 1

        r = piece_row + 1
        c = piece_column - 1

        while r < self.rows and c >= 0 and self.colors[r][c] == color:
            front_diagonal_coordinates.append((r, c))
            r += 1
            c -= 1

        if len(front_diagonal_coordinates) >= connect_amount:
            winning_coordinates += front_diagonal_coordinates

        return winning_coordinates

    def has_piece_been_played(self):
        return self.last_coord is not None

    def has_last_move_won_game(self, connect_amount):
        win_coords = self.winning_coordinates(*self.last_coord, connect_amount)
        return len(win_coords) >= connect_amount

    def is_full(self):
        return len(self.open_columns()) == 0
