from game_screen import GameScreen
from user import User


class Player(User):

    def __init__(self, game: GameScreen, color: str, win_color: str) -> None:
        User.__init__(self, game, color, win_color)

    def initiate_turn(self) -> None:
        self.game.enable_player_input()
