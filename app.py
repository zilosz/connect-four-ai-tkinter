import tkinter as tk
import ctypes
import pyautogui as gui
import win32api as win

from home_screen import HomeScreen
from game_screen import GameScreen
from player import Player
from ai import AI


class App(tk.Tk):

    BG = 'gray65'

    BORDER_COLOR = 'black'
    BORDER_WIDTH = 8

    MIN_BOARD_SIZE = 3
    MAX_BOARD_SIZE = 15
    DEFAULT_ROWS = 6
    DEFAULT_COLUMNS = 7

    MIN_CONNECT_AMOUNT = 3
    MAX_CONNECT_AMOUNT = 6
    DEFAULT_CONNECT_AMOUNT = 4

    DEFAULT_USER_1 = Player
    DEFAULT_USER_2 = AI

    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.state('zoom')
        self.title('Connect Four')
        self.configure(bg=self.BG)
        
        monitor_info = win.GetMonitorInfo(win.MonitorFromPoint((0, 0)))
        monitor_area = monitor_info.get("Monitor")
        work_area = monitor_info.get("Work")
        task_bar_height = monitor_area[3] - work_area[3]
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        window_title_height = ctypes.windll.user32.GetSystemMetrics(4)
        
        self.width, self.height = gui.size()
        self.height -= task_bar_height + window_title_height
        
        self.home_screen = HomeScreen(self)
        self.home_screen.draw()
        self.game_screen = None

    def go_home(self, event=None) -> None:
        self.game_screen.grid_forget()
        self.home_screen.draw()
        self.home_screen.set_options_to_default()

    def start_game(self, event=None) -> None:
        self.home_screen.grid_forget()
        self.game_screen = GameScreen(
            self, self.home_screen.get_row_input(),
            self.home_screen.get_column_input(),
            self.home_screen.get_connect_amount_input(),
            self.home_screen.get_user1_input(),
            self.home_screen.get_user2_input())
        self.game_screen.draw()
        self.game_screen.manage_turn()


if __name__ == "__main__":
    App().mainloop()
