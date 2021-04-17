from game_screen import GameScreen


class User:

    def __init__(self, game: GameScreen, color: str, win_color: str) -> None:
        self.game = game
        self.color = color
        self.win_color = win_color
