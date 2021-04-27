import tkinter as tk


class Slot(tk.Canvas):

    EMPTY_COLOR = 'white'
    HIGHLIGHT_COLOR = 'black'
    WIN_SYMBOL = '♛'
    WIN_FONT_TO_PIECE_SIZE_RATIO = 0.4

    def __init__(self, board_frame, size, color):
        self.size = size

        tk.Canvas.__init__(
            self,
            board_frame,
            bg=color,
            width=size,
            height=size,
            highlightthickness=0
        )
        
        self.shape = self.create_oval(
            0, 0,
            size, size,
            fill=self.EMPTY_COLOR,
            outline=self.HIGHLIGHT_COLOR,
            width=0
        )

    def set_piece_color(self, color):
        self.itemconfig(self.shape, fill=color)

    def set_winner(self, win_color):
        win_font = ('Arial', int(self.WIN_FONT_TO_PIECE_SIZE_RATIO * self.size))
        self.create_text(
            self.size // 2,
            self.size // 2,
            fill=win_color,
            text=self.WIN_SYMBOL,
            font=win_font
        )

    def mark_as_last_played(self):
        self.itemconfig(self.shape, width=5)

    def mark_as_normal(self):
        self.itemconfig(self.shape, width=0)
