import tkinter as tk

from home_screen import HomeScreen


class OptionChooser(tk.Frame):

    FONT_NAME = 'Georgia'
    FONT_SIZE_TO_SCREEN_WIDTH_RATIO = 0.04

    SPINBOX_EXTRA_ENTRY_SPACE = 2
    SPINBOX_BORDER_WIDTH = 2
    SPINBOX_BORDER_COLOR = 'black'

    CENTER_GAP_TO_SCREEN_WIDTH_RATIO = 0.05
    BOTTOM_PADDING_TO_HEIGHT_RATIO = 0.1

    TEXT_COLOR = 'black'

    def __init__(
            self,
            home_screen: HomeScreen,
            name: str,
            y: float,
            height: float,
            values: list[int, str],
            default_value: [str, int]
    ) -> None:

        tk.Frame.__init__(self, home_screen, bg=home_screen.BG)

        font_size = int(
            home_screen.width * self.FONT_SIZE_TO_SCREEN_WIDTH_RATIO)
        font = (self.FONT_NAME, font_size)

        label = tk.Label(
            self, text=name, bg=home_screen.BG, fg=self.TEXT_COLOR, font=font)
        label.pack(side=tk.LEFT)

        default = tk.StringVar()

        self.spinbox = tk.Spinbox(
            self,
            values=values,
            textvariable=default,
            font=font,
            justify='center',
            wrap=True,
            highlightthickness=self.SPINBOX_BORDER_WIDTH,
            highlightcolor=self.SPINBOX_BORDER_COLOR,
            highlightbackground=self.SPINBOX_BORDER_COLOR,
            command=self.adjust_width
        )

        default.set(default_value)
        self.adjust_width()

        pad_x = home_screen.width * self.CENTER_GAP_TO_SCREEN_WIDTH_RATIO
        self.spinbox.pack(side=tk.RIGHT, padx=(pad_x, 0))

        self.window = home_screen.canvas.create_window(
            home_screen.width / 2,
            y + height / 2,
            window=self,
            height=height
        )

        self.default_value = default_value

    def get_option(self) -> str:
        return self.spinbox.get()

    def set_to_default(self) -> None:
        self.spinbox.delete(0, 'end')
        self.spinbox.insert(0, self.default_value)
        self.adjust_width()

    def adjust_width(self, event=None) -> None:
        self.spinbox.configure(
            width=len(self.spinbox.get()) + self.SPINBOX_EXTRA_ENTRY_SPACE)
