import tkinter as tk

from option_chooser import OptionChooser
from player import Player
from ai import AI


class HomeScreen(tk.Frame):

    BG = 'light blue'
    WIDTH_RATIO = 0.4

    CONTENT_GAP_TO_CONTENT_HEIGHT_RATIO = 0.07

    TITLE_BG = 'gray'
    TITLE_FG = 'black'
    TITLE_FONT_NAME = 'Georgia bold'
    TITLE_FONT_SIZE_TO_WIDTH_RATIO = 0.065
    TITLE_HEIGHT_RATIO = 0.2
    TITLE_WIDTH_RATIO = 1

    PLAY_BUTTON_BG = 'gray'
    PLAY_BUTTON_ACTIVE_BG = 'gray60'
    PLAY_BUTTON_FG = 'black'
    PLAY_BUTTON_FONT_NAME = 'Georgia bold'
    PLAY_BUTTON_FONT_SIZE_TO_WIDTH_RATIO = 0.12
    PLAY_BUTTON_HEIGHT_TO_CHOOSER_HEIGHT_RATIO = 1
    PLAY_BUTTON_GAP_TO_HEIGHT_RATIO = 0.2
    PLAY_BUTTON_WIDTH_RATIO = 0.3

    def __init__(self, app):
        
        tk.Frame.__init__(
            self, 
            app, 
            highlightthickness=app.BORDER_WIDTH,
            highlightcolor=app.BORDER_COLOR,
            highlightbackground=app.BORDER_COLOR
        )

        self.app = app
        self.width = app.width * self.WIDTH_RATIO
        self.height = app.height - app.BORDER_WIDTH * 2

        self.canvas = tk.Canvas(
            self, 
            width=self.width,
            height=self.height,
            bg=self.BG, 
            highlightthickness=0
        )
        self.canvas.grid()

        title_height = self.height * self.TITLE_HEIGHT_RATIO
        title_font_size = int(
            self.width
            * self.TITLE_FONT_SIZE_TO_WIDTH_RATIO
            * self.TITLE_WIDTH_RATIO
        )
        title_width = self.width * self.TITLE_WIDTH_RATIO
        title_x = self.width / 2 - title_width / 2

        title = tk.Label(
            self, 
            text='Connect Four',
            bg=self.TITLE_BG, 
            fg=self.TITLE_FG,
            font=(self.TITLE_FONT_NAME, title_font_size)
        )

        current_widget_y = 0
        self.canvas.create_window(
            title_x, 
            current_widget_y,
            window=title,
            width=title_width, 
            height=title_height, 
            anchor='nw'
        )

        space_left = self.height - title_height
        content_gap = space_left * self.CONTENT_GAP_TO_CONTENT_HEIGHT_RATIO

        play_button_gap_to_chooser_height_ratio = \
            self.PLAY_BUTTON_GAP_TO_HEIGHT_RATIO \
            * self.PLAY_BUTTON_HEIGHT_TO_CHOOSER_HEIGHT_RATIO

        total_chooser_ratio = OptionChooser.BOTTOM_PADDING_TO_HEIGHT_RATIO * 4 \
            + self.PLAY_BUTTON_HEIGHT_TO_CHOOSER_HEIGHT_RATIO \
            + play_button_gap_to_chooser_height_ratio + 5 \

        chooser_height = (space_left - content_gap * 2) / total_chooser_ratio
        chooser_gap = chooser_height \
            * OptionChooser.BOTTOM_PADDING_TO_HEIGHT_RATIO

        current_widget_y += title_height + content_gap
        self.row_chooser = OptionChooser(
            self, 
            'Rows', 
            current_widget_y, 
            chooser_height,
            list(range(app.MIN_BOARD_SIZE, app.MAX_BOARD_SIZE + 1)),
            app.DEFAULT_ROWS
        )

        current_widget_y += chooser_height + chooser_gap
        self.column_chooser = OptionChooser(
            self, 
            'Columns', 
            current_widget_y, 
            chooser_height,
            list(range(app.MIN_BOARD_SIZE, app.MAX_BOARD_SIZE + 1)),
            app.DEFAULT_COLUMNS
        )

        current_widget_y += chooser_height + chooser_gap
        self.connect_amount_chooser = OptionChooser(
            self, 
            'Connect Amount', 
            current_widget_y, 
            chooser_height,
            list(range(app.MIN_CONNECT_AMOUNT, app.MAX_CONNECT_AMOUNT + 1)),
            app.DEFAULT_CONNECT_AMOUNT
        )

        current_widget_y += chooser_height + chooser_gap
        user_options = [Player.CHOOSER_NAME, AI.CHOOSER_NAME]
        self.user1_chooser = OptionChooser(
            self, 
            'User 1', 
            current_widget_y, 
            chooser_height,
            user_options, 
            app.DEFAULT_USER_1.CHOOSER_NAME
        )

        current_widget_y += chooser_height + chooser_gap
        self.user2_chooser = OptionChooser(
            self, 
            'User 2', 
            current_widget_y, 
            chooser_height,
            user_options, 
            app.DEFAULT_USER_2.CHOOSER_NAME
        )

        play_button_gap = chooser_height * play_button_gap_to_chooser_height_ratio
        current_widget_y += chooser_height + play_button_gap
        play_button_width = self.width * self.PLAY_BUTTON_WIDTH_RATIO
        play_button_x = self.width / 2 - play_button_width / 2
        play_button_height = chooser_height \
            * self.PLAY_BUTTON_HEIGHT_TO_CHOOSER_HEIGHT_RATIO
        play_button_font_size = int(
            play_button_width * self.PLAY_BUTTON_FONT_SIZE_TO_WIDTH_RATIO
        )
        play_button_font = (self.PLAY_BUTTON_FONT_NAME, play_button_font_size)

        self.play_button = tk.Button(
            self, 
            text='Play!', 
            command=app.start_game, 
            bg=self.PLAY_BUTTON_BG,
            fg=self.PLAY_BUTTON_FG, 
            font=play_button_font
        )

        self.play_button.bind('<Enter>', self.on_play_button_hover)
        self.play_button.bind('<Leave>', self.on_play_button_leave)

        self.canvas.create_window(
            play_button_x, 
            current_widget_y, 
            window=self.play_button,
            width=play_button_width, 
            height=play_button_height, 
            anchor='nw'
        )

    def on_play_button_hover(self, event):
        self.play_button.configure(bg=self.PLAY_BUTTON_ACTIVE_BG)

    def on_play_button_leave(self, event):
        self.play_button.configure(bg=self.PLAY_BUTTON_BG)

    def draw(self):
        self.grid(padx=(self.app.width / 2 - self.width / 2, 0))

    def set_options_to_default(self):
        self.row_chooser.set_to_default()
        self.column_chooser.set_to_default()
        self.connect_amount_chooser.set_to_default()
        self.user1_chooser.set_to_default()
        self.user2_chooser.set_to_default()
