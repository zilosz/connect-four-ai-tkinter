import tkinter as tk
import random

from player import Player
from ai import AI
from slot import Slot
from board import Board


# All sizes are ratios to the piece size
class GameScreen(tk.Frame):

    BG = "gray90"

    BUTTON_FONT_NAME = "Alegreya SC"
    BUTTON_FONT_SIZE = 0.25
    BUTTON_GAP = 0.2
    BUTTON_HEIGHT = 0.6

    HOME_BUTTON_BG = "navy"
    HOME_BUTTON_ACTIVE_BG = "#0000AE"
    HOME_BUTTON_FG = "white"

    SPEED_BUTTON_NORMAL_BG = "navy"
    SPEED_BUTTON_FAST_BG = "#0000AE"
    SPEED_BUTTON_FG = "white"
    SPEED_BUTTON_X_OFFSET = 0.25

    TOP_CANVAS_COLOR = "light blue"
    TOP_CANVAS_Y_PAD = 0.25

    ARROW_COLOR = "gray80"
    ARROW_ACTIVE_COLOR = "gray70"
    ARROW_LENGTH = 0.75
    ARROW_BASE = 0.65
    ARROW_DISTANCE = 0.25
    DOWN_ARROW_LENGTH = 0.6

    BOARD_COLOR = "navy"
    BOARD_THICKNESS = 0.3

    EMPTY_SLOT_COLOR = "white"
    PIECE_COLOR_1 = "red"
    WIN_COLOR_1 = "gold"
    PIECE_COLOR_2 = "yellow"
    WIN_COLOR_2 = "black"

    PIECE_HIGHLIGHT_WIDTH = 0.08

    WAIT_SYMBOL_COLOR = "black"
    WAIT_FONT_SIZE = 0.3

    def __init__(self, app, rows, columns, connect_amount, user1, user2):

        tk.Frame.__init__(
            self,
            app,
            highlightthickness=app.BORDER_WIDTH,
            highlightcolor=app.BORDER_COLOR,
            highlightbackground=app.BORDER_COLOR,
        )

        self.app = app
        self.rows = rows
        self.columns = columns
        self.connect_amount = connect_amount

        params1 = (self, self.PIECE_COLOR_1, self.WIN_COLOR_1)
        params2 = (self, self.PIECE_COLOR_2, self.WIN_COLOR_2)

        self.user1 = AI(*params1) if user1 == AI.CHOOSER_NAME else Player(*params1)
        self.user2 = AI(*params2) if user2 == AI.CHOOSER_NAME else Player(*params2)

        top_ratio = (
            1
            + self.TOP_CANVAS_Y_PAD * 2
            + self.ARROW_DISTANCE
            + self.DOWN_ARROW_LENGTH
            + self.BUTTON_GAP * 2
            + self.BUTTON_HEIGHT
        )

        board_ratio = self.rows + self.BOARD_THICKNESS * (self.rows + 1)
        total_ratio = top_ratio + board_ratio

        height = app.height - app.BORDER_WIDTH * 2
        piece_size = height / total_ratio
        gap_size = piece_size * self.BOARD_THICKNESS
        width = self.columns * (piece_size + gap_size) + gap_size

        # Resize if width exceeds screen width
        if width > app.width:
            ratio = app.width / width
            piece_size *= ratio
            gap_size *= ratio
            width = self.columns * (piece_size + gap_size) + gap_size

        self.board_frame = tk.Frame(self, bg=self.BOARD_COLOR)
        self.board_frame.pack(side=tk.BOTTOM)

        self.slots = [[0] * self.columns for _ in range(self.rows)]

        for row in range(self.rows):

            for column in range(self.columns):
                first_gap_x = 0

                if column == 0:
                    first_gap_x = gap_size

                first_gap_y = 0

                if row == 0:
                    first_gap_y = gap_size

                slot = Slot(self.board_frame, piece_size, self.BOARD_COLOR)

                slot.grid(
                    row=row,
                    column=column,
                    padx=(first_gap_x, gap_size),
                    pady=(first_gap_y, gap_size),
                )

                self.slots[row][column] = slot

        self.app.update_idletasks()
        top_height = top_ratio * piece_size

        self.top = tk.Canvas(
            self,
            width=self.board_frame.winfo_reqwidth(),
            height=top_height,
            bg=self.TOP_CANVAS_COLOR,
            highlightthickness=0,
        )

        self.top.pack(side=tk.TOP)

        home_button_gap = self.BUTTON_GAP * piece_size
        home_button_height = self.BUTTON_HEIGHT * piece_size
        button_font_size = int(self.BUTTON_FONT_SIZE * piece_size)
        button_font = (self.BUTTON_FONT_NAME, button_font_size)

        self.home_button = tk.Button(
            self,
            text="Home",
            font=button_font,
            bg=self.HOME_BUTTON_BG,
            fg=self.HOME_BUTTON_FG,
            command=app.go_home,
        )

        self.home_button.bind("<Enter>", self.on_home_button_hover)
        self.home_button.bind("<Leave>", self.on_home_button_leave)

        home_button_x = app.BORDER_WIDTH + home_button_gap
        button_y = app.BORDER_WIDTH + home_button_gap

        self.home_button_window = self.top.create_window(
            home_button_x,
            button_y,
            window=self.home_button,
            height=home_button_height,
            anchor="nw",
        )

        self.speed_button = tk.Button(
            self,
            text="Speed Off",
            font=button_font,
            bg=self.SPEED_BUTTON_NORMAL_BG,
            fg=self.SPEED_BUTTON_FG,
            command=self.speed_toggle,
        )

        home_button_right_x = self.top.bbox(self.home_button_window)[2]
        speed_button_x_offset = self.SPEED_BUTTON_X_OFFSET * piece_size
        speed_button_x = home_button_right_x + speed_button_x_offset

        self.speed_button_window = self.top.create_window(
            speed_button_x,
            button_y,
            window=self.speed_button,
            height=home_button_height,
            anchor="nw",
        )

        self.speed_button.bind("<Enter>", self.on_speed_button_hover)
        self.speed_button.bind("<Leave>", self.on_speed_button_leave)

        y_pad = piece_size * self.TOP_CANVAS_Y_PAD
        center_x = width / 2
        half_piece_size = piece_size / 2
        piece_left_x = center_x - half_piece_size
        piece_top_y = y_pad + home_button_gap * 2 + home_button_height
        piece_bottom_y = piece_top_y + piece_size

        self.dropper_piece = self.top.create_oval(
            piece_left_x,
            piece_top_y,
            piece_left_x + piece_size,
            piece_bottom_y,
            width=1,
            outline="black",
        )

        piece_center_y = piece_top_y + piece_size / 2
        piece_center_x = piece_left_x + piece_size / 2
        wait_font_size = int(self.WAIT_FONT_SIZE * piece_size)

        self.wait_symbol = self.top.create_text(
            piece_center_x,
            piece_center_y,
            text="AI",
            font=("Georgia bold", wait_font_size),
            fill=self.WAIT_SYMBOL_COLOR,
            state="hidden",
        )

        tip_y = piece_top_y + piece_size / 2
        arrow_base_length = self.ARROW_BASE * piece_size
        top_y = tip_y - arrow_base_length / 2
        bottom_y = tip_y + arrow_base_length / 2
        arrow_length = self.ARROW_LENGTH * piece_size
        arrow_distance = self.ARROW_DISTANCE * piece_size
        left_side_x = center_x - arrow_distance - piece_size / 2
        left_tip_x = left_side_x - arrow_length

        self.left_arrow = self.top.create_polygon(
            left_tip_x,
            tip_y,
            left_side_x,
            top_y,
            left_side_x,
            bottom_y,
            fill=self.ARROW_COLOR,
            activefill=self.ARROW_ACTIVE_COLOR,
            width=1,
            outline="black",
        )

        right_side_x = center_x + arrow_distance + piece_size / 2
        right_tip_x = right_side_x + arrow_length

        self.right_arrow = self.top.create_polygon(
            right_tip_x,
            tip_y,
            right_side_x,
            top_y,
            right_side_x,
            bottom_y,
            fill=self.ARROW_COLOR,
            activefill=self.ARROW_ACTIVE_COLOR,
            width=1,
            outline="black",
        )

        down_arrow_length = piece_size * self.DOWN_ARROW_LENGTH
        half_arrow_base = arrow_base_length / 2
        down_left_x = center_x - half_arrow_base
        down_right_x = center_x + half_arrow_base
        top_y = piece_bottom_y + arrow_distance
        down_tip_x = (down_right_x + down_left_x) / 2
        down_tip_y = top_y + down_arrow_length

        self.down_arrow = self.top.create_polygon(
            down_left_x,
            top_y,
            down_right_x,
            top_y,
            down_tip_x,
            down_tip_y,
            fill=self.ARROW_COLOR,
            activefill=self.ARROW_ACTIVE_COLOR,
            width=1,
            outline="black",
        )

        if self.columns % 2 == 0:
            self.move_top_widgets((piece_size + gap_size) / 2)

        self.user_going = random.choice([self.user1, self.user2])
        self.is_speed_on = False
        self.drop_piece_move_length = piece_size + gap_size
        self.board = Board(self.rows, self.columns)
        self.drop_col = self.board.center_column()

        self.bind_all("<r>", app.go_home)

    def set_ai_speed(self, speed):

        if isinstance(self.user1, AI):
            self.user1.set_speed(speed)

        if isinstance(self.user2, AI):
            self.user2.set_speed(speed)

    def reset_ai_speed(self):

        if isinstance(self.user1, AI):
            self.user1.reset_speed()

        if isinstance(self.user2, AI):
            self.user2.reset_speed()

    def speed_toggle(self, event=None):
        self.is_speed_on = not self.is_speed_on

        if self.is_speed_on:
            self.speed_button.configure(bg=self.SPEED_BUTTON_FAST_BG)
            self.speed_button.configure(text="Speed On")
            self.set_ai_speed(0)

        else:
            self.speed_button.configure(bg=self.SPEED_BUTTON_NORMAL_BG)
            self.speed_button.configure(text="Speed Off")
            self.reset_ai_speed()

    def on_speed_button_hover(self, event):

        if self.is_speed_on:
            self.speed_button.configure(bg=self.SPEED_BUTTON_NORMAL_BG)

        else:
            self.speed_button.configure(bg=self.SPEED_BUTTON_FAST_BG)

    def on_speed_button_leave(self, event):

        if self.is_speed_on:
            self.speed_button.configure(bg=self.SPEED_BUTTON_FAST_BG)

        else:
            self.speed_button.configure(bg=self.SPEED_BUTTON_NORMAL_BG)

    def on_home_button_hover(self, event):
        self.home_button.configure(bg=self.HOME_BUTTON_ACTIVE_BG)

    def on_home_button_leave(self, event):
        self.home_button.configure(bg=self.HOME_BUTTON_BG)

    def draw(self):
        self.grid(padx=(self.app.width / 2 - self.winfo_reqwidth() / 2, 0))

    def get_other_color(self, color):

        if color == self.user1.color:
            return self.user2.color

        return self.user1.color

    def move_top_widgets(self, x):
        self.top.move(self.left_arrow, x, 0)
        self.top.move(self.right_arrow, x, 0)
        self.top.move(self.dropper_piece, x, 0)
        self.top.move(self.wait_symbol, x, 0)
        self.top.move(self.down_arrow, x, 0)

    def change_wait_symbol_state(self, state):
        self.top.itemconfig(self.wait_symbol, state=state)

    def set_drop_color(self, color):
        self.top.itemconfig(self.dropper_piece, fill=color)

    def manage_turn(self):
        self.center_drop_piece()
        self.top.itemconfig(self.dropper_piece, fill=self.user_going.color)
        self.user_going.initiate_turn()

    def move_drop_piece_left(self, event=None):

        if self.drop_col == self.columns - 1:
            self.top.itemconfig(self.right_arrow, state="normal")

        if self.drop_col > 0:
            self.move_top_widgets(-self.drop_piece_move_length)
            self.drop_col -= 1

            if self.drop_col == 0:
                self.top.itemconfig(self.left_arrow, state="hidden")

    def move_drop_piece_right(self, event=None):

        if self.drop_col == 0:
            self.top.itemconfig(self.left_arrow, state="normal")

        if self.drop_col < self.columns - 1:
            self.move_top_widgets(self.drop_piece_move_length)
            self.drop_col += 1

            if self.drop_col == self.columns - 1:
                self.top.itemconfig(self.right_arrow, state="hidden")

    def center_drop_piece(self):
        self.move_drop_piece_to_column(self.board.center_column())

    def move_drop_piece_to_column(self, column, move_time=0):

        while self.drop_col < column:
            self.move_drop_piece_right()

            if move_time > 0:
                self.app.after(move_time, self.app.update())
                self.app.update_idletasks()

        while self.drop_col > column:
            self.move_drop_piece_left()

            if move_time > 0:
                self.app.after(move_time, self.app.update())
                self.app.update_idletasks()

    def drop_piece(self, event=None):

        if self.board.is_column_open(self.drop_col):

            if self.board.has_piece_been_played():
                last_row = self.board.last_coord[0]
                last_col = self.board.last_coord[1]
                self.slots[last_row][last_col].mark_as_normal()

            drop_row = self.board.get_drop_row_in_column(self.drop_col)
            slot = self.slots[drop_row][self.drop_col]
            self.board.drop_piece_in_column(
                self.drop_col, self.user_going.color
            )
            slot.set_piece_color(self.user_going.color)
            slot.mark_as_last_played()

            if self.board.has_last_move_won_game(self.connect_amount):
                winning_coordinates = self.board.winning_coordinates(
                    drop_row, self.drop_col, self.connect_amount
                )

                for coordinate in winning_coordinates:
                    winning_slot = self.slots[coordinate[0]][coordinate[1]]
                    winning_slot.set_winner(self.user_going.win_color)

                if isinstance(self.user_going, Player):
                    self.disable_player_input()

                return

            if self.board.is_full():
                return

            if self.user_going == self.user1:
                self.user_going = self.user2

            else:
                self.user_going = self.user1

            self.manage_turn()

    def enable_piece_mover_arrows(self):
        self.top.tag_bind(
            self.left_arrow, "<Button-1>", self.move_drop_piece_left
        )
        self.bind_all("<Left>", self.move_drop_piece_left)

        self.top.tag_bind(
            self.right_arrow, "<Button-1>", self.move_drop_piece_right
        )
        self.bind_all("<Right>", self.move_drop_piece_right)

    def disable_piece_mover_arrows(self):
        self.top.tag_unbind(self.left_arrow, "<Button-1>")
        self.unbind_all("<Left>")
        self.top.tag_unbind(self.right_arrow, "<Button-1>")
        self.unbind_all("<Right>")

    def enable_drop(self):
        self.bind_all("<Down>", self.drop_piece)
        self.top.tag_bind(self.down_arrow, "<Button-1>", self.drop_piece)

    def disable_drop(self):
        self.unbind_all("<Down>")
        self.top.tag_unbind(self.down_arrow, "<Button-1>")

    def enable_player_input(self):
        self.enable_drop()
        self.enable_piece_mover_arrows()

    def disable_player_input(self):
        self.disable_drop()
        self.disable_piece_mover_arrows()
