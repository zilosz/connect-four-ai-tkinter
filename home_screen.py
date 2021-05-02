import tkinter as tk

from option_chooser import OptionChooser
from player import Player
from ai import AI


class HomeScreen(tk.Frame):

    BG = "light blue"
    # Ratio to screen width
    WIDTH = 0.4

    # Ratio to height without title
    WIDGET_Y_GAP = 0.05

    TITLE_BG = "gray"
    TITLE_FG = "black"
    TITLE_FONT_NAME = "Georgia bold"
    # Ratio to screen width
    TITLE_FONT_SIZE = 0.065
    # Ratio to screen height
    TITLE_HEIGHT = 0.2

    PLAY_BG = "gray"
    PLAY_ACTIVE_BG = "gray60"
    PLAY_FG = "black"
    PLAY_FONT = "Georgia bold"
    # Ratio to screen width
    PLAY_FONT_SIZE = 0.12
    # Ratio to chooser height
    PLAY_HEIGHT = 1
    # Ratio to play button height
    PLAY_Y_PAD = 0.2
    # Ratio to screen width
    PLAY_WIDTH = 0.3

    # Ratio to chooser height
    CHOOSER_Y_PAD = 0.15

    def __init__(self, app):

        tk.Frame.__init__(
            self,
            app,
            highlightthickness=app.BORDER_WIDTH,
            highlightcolor=app.BORDER_COLOR,
            highlightbackground=app.BORDER_COLOR,
        )

        self.app = app
        self.width = app.width * self.WIDTH
        self.height = app.height - app.BORDER_WIDTH * 2

        self.canvas = tk.Canvas(
            self,
            width=self.width,
            height=self.height,
            bg=self.BG,
            highlightthickness=0,
        )

        self.canvas.grid()

        title_height = self.height * self.TITLE_HEIGHT
        title_font_size = int(self.width * self.TITLE_FONT_SIZE)
        title_x = self.width / 2 - self.width / 2
        title_font = (self.TITLE_FONT_NAME, title_font_size)

        title = tk.Label(
            self,
            text="Connect Four",
            bg=self.TITLE_BG,
            fg=self.TITLE_FG,
            font=title_font,
        )

        current_widget_y = 0

        self.canvas.create_window(
            title_x,
            current_widget_y,
            window=title,
            width=self.width,
            height=title_height,
            anchor="nw",
        )

        space_left = self.height - title_height
        widget_y_gap = space_left * self.WIDGET_Y_GAP

        # Ratio to chooser height
        play_gap_ratio = self.PLAY_Y_PAD * self.PLAY_HEIGHT
        total_chooser_ratio = (
            self.CHOOSER_Y_PAD * 4 + self.PLAY_HEIGHT + play_gap_ratio + 5
        )
        chooser_height = (space_left - widget_y_gap * 2) / total_chooser_ratio
        chooser_gap = chooser_height * self.CHOOSER_Y_PAD

        current_widget_y += title_height + widget_y_gap
        row_options = list(range(app.MIN_BOARD_SIZE, app.MAX_BOARD_SIZE + 1))

        self.row_chooser = OptionChooser(
            self,
            "Rows",
            current_widget_y,
            chooser_height,
            row_options,
            app.DEFAULT_ROWS,
        )

        current_widget_y += chooser_height + chooser_gap
        col_options = list(range(app.MIN_BOARD_SIZE, app.MAX_BOARD_SIZE + 1))

        self.column_chooser = OptionChooser(
            self,
            "Columns",
            current_widget_y,
            chooser_height,
            col_options,
            app.DEFAULT_COLUMNS,
        )

        current_widget_y += chooser_height + chooser_gap
        connect_options = list(
            range(app.MIN_CONNECT_AMOUNT, app.MAX_CONNECT_AMOUNT + 1)
        )

        self.connect_amount_chooser = OptionChooser(
            self,
            "Connect Amount",
            current_widget_y,
            chooser_height,
            connect_options,
            app.DEFAULT_CONNECT_AMOUNT,
        )

        current_widget_y += chooser_height + chooser_gap
        user_options = [Player.CHOOSER_NAME, AI.CHOOSER_NAME]

        self.user1_chooser = OptionChooser(
            self,
            "User 1",
            current_widget_y,
            chooser_height,
            user_options,
            app.DEFAULT_USER_1.CHOOSER_NAME,
        )

        current_widget_y += chooser_height + chooser_gap

        self.user2_chooser = OptionChooser(
            self,
            "User 2",
            current_widget_y,
            chooser_height,
            user_options,
            app.DEFAULT_USER_2.CHOOSER_NAME,
        )

        play_button_gap = chooser_height * play_gap_ratio
        current_widget_y += chooser_height + play_button_gap
        play_width = self.width * self.PLAY_WIDTH
        play_x = self.width / 2 - play_width / 2
        play_height = chooser_height * self.PLAY_HEIGHT
        play_font_size = int(play_width * self.PLAY_FONT_SIZE)
        play_font = (self.PLAY_FONT, play_font_size)

        self.play_button = tk.Button(
            self,
            text="Play!",
            command=app.start_game,
            bg=self.PLAY_BG,
            fg=self.PLAY_FG,
            font=play_font,
        )

        self.play_button.bind("<Enter>", self.on_play_button_hover)
        self.play_button.bind("<Leave>", self.on_play_button_leave)

        self.canvas.create_window(
            play_x,
            current_widget_y,
            window=self.play_button,
            width=play_width,
            height=play_height,
            anchor="nw",
        )

    def on_play_button_hover(self, event):
        self.play_button.configure(bg=self.PLAY_ACTIVE_BG)

    def on_play_button_leave(self, event):
        self.play_button.configure(bg=self.PLAY_BG)

    def draw(self):
        self.grid(padx=(self.app.width / 2 - self.width / 2, 0))

    def set_options_to_default(self):
        self.row_chooser.set_to_default()
        self.column_chooser.set_to_default()
        self.connect_amount_chooser.set_to_default()
        self.user1_chooser.set_to_default()
        self.user2_chooser.set_to_default()
