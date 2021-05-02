import tkinter as tk


# All ratios are to the screen width
class OptionChooser(tk.Frame):

    FONT_NAME = "Georgia"
    FONT_COLOR = "black"
    FONT_SIZE = 0.04

    SPINBOX_EXTRA_ENTRY_SPACE = 2
    SPINBOX_BORDER_WIDTH = 3
    SPINBOX_BORDER_COLOR = "black"

    CENTER_GAP = 0.05

    def __init__(self, home_screen, name, y, height, values, default_value):
        tk.Frame.__init__(self, home_screen, bg=home_screen.BG)

        font_size = int(home_screen.width * self.FONT_SIZE)
        font = (self.FONT_NAME, font_size)

        label = tk.Label(
            self, text=name, bg=home_screen.BG, fg=self.FONT_COLOR, font=font
        )

        label.pack(side=tk.LEFT)

        default = tk.StringVar()

        self.spinbox = tk.Spinbox(
            self,
            values=values,
            textvariable=default,
            font=font,
            justify="center",
            wrap=True,
            highlightthickness=self.SPINBOX_BORDER_WIDTH,
            highlightcolor=self.SPINBOX_BORDER_COLOR,
            highlightbackground=self.SPINBOX_BORDER_COLOR,
            command=self.adjust_width,
        )

        default.set(default_value)
        self.default_value = default_value
        self.adjust_width()

        pad_x = home_screen.width * self.CENTER_GAP
        self.spinbox.pack(side=tk.RIGHT, padx=(pad_x, 0))

        w, h = home_screen.width / 2, y + height / 2
        home_screen.canvas.create_window(w, h, window=self, height=height)

    def set_to_default(self):
        self.spinbox.delete(0, "end")
        self.spinbox.insert(0, self.default_value)
        self.adjust_width()

    def adjust_width(self, event=None):
        chars = len(self.spinbox.get())
        self.spinbox.configure(width=chars + self.SPINBOX_EXTRA_ENTRY_SPACE)
