import tkinter as tk
import random
import threading

from app import App
from player import Player
from ai import AI
from slot import Slot
from board import Board
from user import User


class GameScreen(tk.Frame):
    BG = 'gray90'

    HOME_BUTTON_FONT_NAME = 'Alegreya SC'
    HOME_BUTTON_FONT_SIZE_TO_HEIGHT_RATIO = 0.4
    HOME_BUTTON_BG = 'navy'
    HOME_BUTTON_ACTIVE_BG = '#0000AE'
    HOME_BUTTON_FG = 'white'
    HOME_BUTTON_GAP_TO_PIECE_SIZE_RATIO = 0.2
    HOME_BUTTON_HEIGHT_TO_PIECE_SIZE_RATIO = 0.6

    TOP_CANVAS_COLOR = 'light blue'
    TOP_CANVAS_Y_PAD_TO_PIECE_SIZE_RATIO = 0.25

    ARROW_COLOR = 'gray80'
    ARROW_ACTIVE_COLOR = 'gray70'
    ARROW_LENGTH_TO_PIECE_SIZE_RATIO = 0.75
    ARROW_BASE_TO_PIECE_SIZE_RATIO = 0.65
    ARROW_DISTANCE_TO_PIECE_SIZE_RATIO = 0.25
    DOWN_ARROW_LENGTH_TO_PIECE_SIZE_RATIO = 0.6

    BOARD_COLOR = 'navy'
    BOARD_SLOT_GAP_TO_PIECE_SIZE_RATIO = 0.3

    EMPTY_SLOT_COLOR = 'white'
    PIECE_COLOR_1 = 'red'
    WIN_COLOR_1 = 'gold'
    PIECE_COLOR_2 = 'yellow'
    WIN_COLOR_2 = 'black'

    JUST_PLAYED_WIDTH_TO_PIECE_SIZE_RATIO = 0.08

    WAIT_SYMBOL_COLOR = 'black'
    WAIT_SYMBOL_GAP_TO_SIZE_RATIO = 0.4

    def __init__(
            self,
            app: App,
            rows: int,
            columns: int,
            connect_amount: int,
            user1: User,
            user2: User
    ) -> None:

        tk.Frame.__init__(
            self,
            app,
            highlightthickness=app.BORDER_WIDTH,
            highlightcolor=app.BORDER_COLOR,
            highlightbackground=app.BORDER_COLOR
        )

        self.app = app
        self.rows = rows
        self.columns = columns
        self.connect_amount = connect_amount

        if user1 == Player.__name__:
            self.user1 = Player(self, self.PIECE_COLOR_1, self.WIN_COLOR_1)

        else:
            self.user1 = AI(self, self.PIECE_COLOR_1, self.WIN_COLOR_1)

        if user2 == Player.__name__:
            self.user2 = Player(self, self.PIECE_COLOR_2, self.WIN_COLOR_2)

        else:
            self.user2 = AI(self, self.PIECE_COLOR_2, self.WIN_COLOR_2)

        top_ratio = 1 \
            + self.TOP_CANVAS_Y_PAD_TO_PIECE_SIZE_RATIO * 2 \
            + self.ARROW_DISTANCE_TO_PIECE_SIZE_RATIO \
            + self.DOWN_ARROW_LENGTH_TO_PIECE_SIZE_RATIO \
            + self.HOME_BUTTON_GAP_TO_PIECE_SIZE_RATIO * 2 \
            + self.HOME_BUTTON_HEIGHT_TO_PIECE_SIZE_RATIO

        board_ratio = self.rows \
            + self.BOARD_SLOT_GAP_TO_PIECE_SIZE_RATIO \
            * (self.rows + 1)
        total_ratio = top_ratio + board_ratio

        self.height = app.height - app.BORDER_WIDTH * 2

        self.piece_size = self.height / total_ratio
        self.gap_size = self.piece_size \
            * self.BOARD_SLOT_GAP_TO_PIECE_SIZE_RATIO

        self.width = self.columns \
            * (self.piece_size + self.gap_size) \
            + self.gap_size

        if self.width > app.width:
            ratio = app.width / self.width
            self.piece_size *= ratio
            self.gap_size *= ratio
            self.width = self.columns \
                * (self.piece_size + self.gap_size) \
                + self.gap_size

        self.board_frame = tk.Frame(self, bg=self.BOARD_COLOR)
        self.board_frame.pack(side=tk.BOTTOM)

        self.slots = []

        for row in range(self.rows):
            row_slots = []

            for column in range(self.columns):
                first_gap_x = 0

                if column == 0:
                    first_gap_x = self.gap_size

                first_gap_y = 0

                if row == 0:
                    first_gap_y = self.gap_size

                slot = Slot(self.board_frame, self.piece_size, self.BOARD_COLOR)
                slot.grid(
                    row=row,
                    column=column,
                    padx=(first_gap_x, self.gap_size),
                    pady=(first_gap_y, self.gap_size)
                )
                row_slots.append(slot)

            self.slots.append(row_slots)

        self.app.update_idletasks()

        top_canvas_height = top_ratio * self.piece_size
        self.top_canvas = tk.Canvas(
            self,
            width=self.board_frame.winfo_reqwidth(),
            height=top_canvas_height,
            bg=self.TOP_CANVAS_COLOR,
            highlightthickness=0
        )
        self.top_canvas.pack(side=tk.TOP)

        home_button_gap = self.HOME_BUTTON_GAP_TO_PIECE_SIZE_RATIO \
            * self.piece_size
        home_button_height = self.HOME_BUTTON_HEIGHT_TO_PIECE_SIZE_RATIO \
            * self.piece_size
        home_button_font_size = int(
            self.HOME_BUTTON_FONT_SIZE_TO_HEIGHT_RATIO * home_button_height
        )
        home_button_font = (self.HOME_BUTTON_FONT_NAME, home_button_font_size)

        self.home_button = tk.Button(
            self,
            text='Home',
            font=home_button_font,
            bg=self.HOME_BUTTON_BG,
            fg=self.HOME_BUTTON_FG,
            command=app.go_home
        )

        self.home_button.bind('<Enter>', self.on_home_button_hover)
        self.home_button.bind('<Leave>', self.on_home_button_leave)

        home_button_x = app.BORDER_WIDTH + home_button_gap
        home_button_y = app.BORDER_WIDTH + home_button_gap

        self.home_button_window = self.top_canvas.create_window(
            home_button_x, home_button_y,
            window=self.home_button,
            height=home_button_height,
            anchor='nw'
        )

        y_pad = self.piece_size * self.TOP_CANVAS_Y_PAD_TO_PIECE_SIZE_RATIO
        center_x = self.width / 2
        half_piece_size = self.piece_size / 2
        piece_left_x = center_x - half_piece_size
        piece_top_y = y_pad + home_button_gap * 2 + home_button_height
        piece_bottom_y = piece_top_y + self.piece_size

        self.dropper_piece = self.top_canvas.create_oval(
            piece_left_x, piece_top_y,
            piece_left_x + self.piece_size, piece_bottom_y,
            width=1,
            outline='black'
        )

        wait_symbol_size = (1 - self.WAIT_SYMBOL_GAP_TO_SIZE_RATIO * 4) \
            * self.piece_size / 3
        wait_symbol_gap = self.WAIT_SYMBOL_GAP_TO_SIZE_RATIO * wait_symbol_size

        piece_center_y = (piece_top_y + piece_bottom_y) / 2
        half_wait_symbol_size = wait_symbol_size / 2
        symbol_top_y = piece_center_y - half_wait_symbol_size
        symbol_bottom_y = piece_center_y + half_wait_symbol_size
        total_space = wait_symbol_size * 3 + wait_symbol_gap * 4
        start_x = piece_left_x + (self.piece_size - total_space) / 2

        self.wait_symbols = []

        for symbol in range(3):
            symbol_left_x = start_x \
                + symbol * wait_symbol_gap \
                + symbol * wait_symbol_size \
                + wait_symbol_gap

            self.wait_symbols.append(self.top_canvas.create_oval(
                symbol_left_x, symbol_top_y,
                symbol_left_x + wait_symbol_size, symbol_bottom_y,
                fill=self.WAIT_SYMBOL_COLOR,
                width=1,
                outline='black'
            ))

        self.change_wait_symbol_state('hidden')

        tip_y = piece_top_y + self.piece_size / 2
        arrow_base_length = self.ARROW_BASE_TO_PIECE_SIZE_RATIO \
            * self.piece_size
        top_y = tip_y - arrow_base_length / 2
        bottom_y = tip_y + arrow_base_length / 2

        arrow_length = self.ARROW_LENGTH_TO_PIECE_SIZE_RATIO \
            * self.piece_size
        arrow_distance = self.ARROW_DISTANCE_TO_PIECE_SIZE_RATIO \
            * self.piece_size

        left_side_x = center_x - arrow_distance - self.piece_size / 2
        left_tip_x = left_side_x - arrow_length

        self.left_arrow = self.top_canvas.create_polygon(
            left_tip_x, tip_y,
            left_side_x, top_y,
            left_side_x, bottom_y,
            fill=self.ARROW_COLOR,
            activefill=self.ARROW_ACTIVE_COLOR,
            width=1, outline='black'
        )

        right_side_x = center_x + arrow_distance + self.piece_size / 2
        right_tip_x = right_side_x + arrow_length

        self.right_arrow = self.top_canvas.create_polygon(
            right_tip_x, tip_y,
            right_side_x, top_y,
            right_side_x, bottom_y,
            fill=self.ARROW_COLOR,
            activefill=self.ARROW_ACTIVE_COLOR,
            width=1,
            outline='black'
        )

        down_arrow_length = self.piece_size \
            * self.DOWN_ARROW_LENGTH_TO_PIECE_SIZE_RATIO

        half_arrow_base = arrow_base_length / 2
        down_left_x = center_x - half_arrow_base
        down_right_x = center_x + half_arrow_base
        top_y = piece_bottom_y + arrow_distance
        down_tip_x = (down_right_x + down_left_x) / 2
        down_tip_y = top_y + down_arrow_length

        self.down_arrow = self.top_canvas.create_polygon(
            down_left_x, top_y,
            down_right_x, top_y,
            down_tip_x, down_tip_y,
            fill=self.ARROW_COLOR,
            activefill=self.ARROW_ACTIVE_COLOR,
            width=1,
            outline='black'
        )

        self.top_widgets = [
            self.left_arrow,
            self.right_arrow,
            self.dropper_piece,
            self.down_arrow
        ]

        self.board = Board(self.rows, self.columns)

        if self.columns % 2 == 0:
            shift_amount = (self.piece_size + self.gap_size) / 2

            self.move_top_widgets(shift_amount)

            for symbol in self.wait_symbols:
                self.top_canvas.move(symbol, shift_amount, 0)

        self.drop_piece_column = self.board.center_column()

        self.bind_all('<r>', app.go_home)

        self.users = [self.user1, self.user2]
        self.user_going = random.choice(self.users)

    def on_home_button_hover(self, event) -> None:
        self.home_button.configure(bg=self.HOME_BUTTON_ACTIVE_BG)

    def on_home_button_leave(self, event) -> None:
        self.home_button.configure(bg=self.HOME_BUTTON_BG)

    def draw(self) -> None:
        self.grid(padx=(self.app.width / 2 - self.width / 2, 0))

    def get_other_color(self, color: str) -> str:

        if color == self.user1.color:
            return self.user2.color

        return self.user1.color

    def move_top_widgets(self, x: float) -> None:

        for widget in self.top_widgets:
            self.top_canvas.move(widget, x, 0)

    def change_wait_symbol_state(self, state: str) -> None:

        for symbol in self.wait_symbols:
            self.top_canvas.itemconfig(symbol, state=state)

    def set_drop_color(self, color: str) -> None:
        self.top_canvas.itemconfig(self.dropper_piece, fill=color)

    def manage_turn(self) -> None:
        self.center_drop_piece()
        self.top_canvas.itemconfig(
            self.dropper_piece,
            fill=self.user_going.color
        )
        turn_thread = threading.Thread(target=self.user_going.initiate_turn)
        turn_thread.start()

    def move_drop_piece_left(self, event=None) -> None:

        if self.drop_piece_column == self.columns - 1:
            self.top_canvas.itemconfig(self.right_arrow, state='normal')

        if self.drop_piece_column > 0:
            self.move_top_widgets(-self.piece_size - self.gap_size)

            self.drop_piece_column -= 1

            if self.drop_piece_column == 0:
                self.top_canvas.itemconfig(self.left_arrow, state='hidden')

    def move_drop_piece_right(self, event=None) -> None:

        if self.drop_piece_column == 0:
            self.top_canvas.itemconfig(self.left_arrow, state='normal')

        if self.drop_piece_column < self.columns - 1:
            self.move_top_widgets(self.piece_size + self.gap_size)

            self.drop_piece_column += 1

            if self.drop_piece_column == self.columns - 1:
                self.top_canvas.itemconfig(self.right_arrow, state='hidden')

    def center_drop_piece(self) -> None:
        self.move_drop_piece_to_column(self.board.center_column())

    def move_drop_piece_to_column(
            self, column: int, move_time: float = 0) -> None:

        while self.drop_piece_column < column:
            self.move_drop_piece_right()

            if move_time > 0:
                self.app.after(move_time, self.app.update())
                self.app.update_idletasks()

        while self.drop_piece_column > column:
            self.move_drop_piece_left()

            if move_time > 0:
                self.app.after(move_time, self.app.update())
                self.app.update_idletasks()

    def drop_piece(self, event=None) -> None:

        if self.board.is_column_open(self.drop_piece_column):

            if self.board.has_piece_been_played():
                last_row = self.board.last_played_coordinate[0]
                last_col = self.board.last_played_coordinate[1]
                self.slots[last_row][last_col].mark_as_normal()

            drop_row = self.board.get_drop_row_in_column(self.drop_piece_column)
            slot = self.slots[drop_row][self.drop_piece_column]
            self.board.drop_piece_in_column(
                self.drop_piece_column,
                self.user_going.color
            )
            slot.set_piece_color(self.user_going.color)
            slot.mark_as_last_played()

            if self.board.has_last_move_won_game(self.connect_amount):
                winning_coordinates = self.board.find_winning_piece_coordinates(
                    drop_row,
                    self.drop_piece_column,
                    self.connect_amount
                )

                for coordinate in winning_coordinates:
                    self.slots[coordinate[0]][coordinate[1]].set_winner(
                        self.user_going.win_color
                    )

                if isinstance(self.user_going, Player):
                    self.disable_player_input()

                return

            if self.board.is_full():
                return

            next_user_index = self.users.index(self.user_going) % 2 - 1
            self.user_going = self.users[next_user_index]
            self.manage_turn()

    def enable_piece_mover_arrows(self) -> None:
        self.top_canvas.tag_bind(
            self.left_arrow,
            '<Button-1>',
            self.move_drop_piece_left
        )
        self.bind_all('<Left>', self.move_drop_piece_left)

        self.top_canvas.tag_bind(
            self.right_arrow,
            '<Button-1>',
            self.move_drop_piece_right
        )
        self.bind_all('<Right>', self.move_drop_piece_right)

    def disable_piece_mover_arrows(self) -> None:
        self.top_canvas.tag_unbind(self.left_arrow, '<Button-1>')
        self.unbind_all('<Left>')

        self.top_canvas.tag_unbind(self.right_arrow, '<Button-1>')
        self.unbind_all('<Right>')

    def enable_drop(self) -> None:
        self.bind_all('<Down>', self.drop_piece)
        self.top_canvas.tag_bind(
            self.down_arrow,
            '<Button-1>',
            self.drop_piece
        )

    def disable_drop(self) -> None:
        self.unbind_all('<Down>')
        self.top_canvas.tag_unbind(self.down_arrow, '<Button-1>')

    def enable_player_input(self) -> None:
        self.enable_drop()
        self.enable_piece_mover_arrows()

    def disable_player_input(self) -> None:
        self.disable_drop()
        self.disable_piece_mover_arrows()
