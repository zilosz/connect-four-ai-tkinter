from user import User


class Player(User):
    
    CHOOSER_NAME = 'Player'

    def __init__(self, game, color, win_color):
        User.__init__(self, game, color, win_color)

    def initiate_turn(self):
        self.game.enable_player_input()
